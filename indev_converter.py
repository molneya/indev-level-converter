
import argparse, nbtlib, os
import numpy as np
from nbtlib import File, Compound, List, Byte, Int, Short, Long, Double, ByteArray

class IndevToAlphaConverter:
    def __init__(self, indev_level_path, args):
        nbt_data = nbtlib.load(indev_level_path)
        self.about = nbt_data.root['About']
        self.environment = nbt_data.root['Environment']
        self.map = nbt_data.root['Map']
        self.entities = nbt_data.root['Entities']
        self.tile_entities = nbt_data.root['TileEntities']

        self.args = args
        self.data = None
        self.chunk_data = []

    def _create_level_dat(self):
        for entity in self.entities:
            if entity['id'] == 'LocalPlayer':
                player = entity
                break

        self.data = File({
            '': Compound({
                'Data': Compound({
                    'Player': Compound({
                        'Inventory': player['Inventory'],
                        'Motion': player['Motion'],
                        'Pos': player['Pos'],
                        'Rotation': player['Rotation'],
                        'Air': player['Air'],
                        'AttackTime': player['AttackTime'] if 'AttackTime' in player else Short(0),
                        'DeathTime': player['DeathTime'] if 'DeathTime' in player else Short(0),
                        'FallDistance': player['FallDistance'],
                        'Fire': player['Fire'],
                        'Health': player['Health'] if 'Health' in player else Short(10),
                        'HurtTime': player['HurtTime'] if 'HurtTime' in player else Short(0),
                        'OnGround': Byte(1),
                        'Score': player['Score'],
                    }),
                    'LastPlayed': self.about['CreatedOn'],
                    'SpawnX': Int(self.map['Spawn'][0] + self.args.x_offset * 16),
                    'SpawnY': Int(self.map['Spawn'][1] + self.args.y_offset),
                    'SpawnZ': Int(self.map['Spawn'][2] + self.args.z_offset * 16),
                    'Time': Long(self.environment['TimeOfDay']) if 'TimeOfDay' in self.environment else Long(0),
                })
            })
        })

        if self.args.seed:
            self.data['']['Data']['RandomSeed'] = Long(self.args.seed)

    def _create_chunks(self):
        x_chunks = self.map['Length'] // 16
        z_chunks = self.map['Width'] // 16
        total_chunks = x_chunks * z_chunks

        for index in range(total_chunks):
            current_z, current_x = divmod(index, z_chunks)

            entities = self._extract_entities(current_x, current_z)
            tile_entities = self._extract_tile_entities(current_x, current_z)
            blocks = self._extract_chunk_blocks(current_x, current_z)
            data, light = self._extract_chunk_data(current_x, current_z)
            height_map = self._calculate_height_map(blocks)

            data = File({
                '': Compound({
                    'Level': Compound({
                        'Entities': List[Compound](entities),
                        'TileEntities': List[Compound](tile_entities),
                        'LastUpdate': Long(200),
                        'xPos': Int(current_x + self.args.x_offset),
                        'zPos': Int(current_z + self.args.z_offset),
                        'Blocks': ByteArray(blocks),
                        'Data': ByteArray(data),
                        'BlockLight': ByteArray(light),
                        'SkyLight': ByteArray(np.zeros(16 * 16 * 64, dtype=int)),
                        'HeightMap': ByteArray(height_map),
                        'TerrainPopulated': Byte(not self.args.repopulate),
                    })
                })
            })

            self.chunk_data.append(data)

    def _convert_entities(self):
        for entity in self.entities:
            entity['Motion'] = List[Double]([Double(motion) for motion in entity['Motion']])
            entity['Pos'] = List[Double]([Double(motion) for motion in entity['Pos']])

            entity['Pos'][0] += self.args.x_offset * 16
            entity['Pos'][1] += self.args.y_offset
            entity['Pos'][2] += self.args.z_offset * 16

            if 'TileX' in entity:
                entity['TileX'] = Int(entity['TileX'] + self.args.x_offset * 16)
                entity['TileY'] = Int(entity['TileY'] + self.args.y_offset)
                entity['TileZ'] = Int(entity['TileZ'] + self.args.z_offset * 16)

            if 'xTile' in entity:
                entity['xTile'] = Int(entity['xTile'] + self.args.x_offset * 16)
                entity['yTile'] = Int(entity['yTile'] + self.args.y_offset)
                entity['zTile'] = Int(entity['zTile'] + self.args.z_offset * 16)

    def _convert_tile_entities(self):
        for tile_entity in self.tile_entities:
            tile_entity['x'] = Int(tile_entity['Pos'] % 1024 + self.args.x_offset * 16)
            tile_entity['y'] = Int((tile_entity['Pos'] >> 10) % 1024 + self.args.y_offset)
            tile_entity['z'] = Int((tile_entity['Pos'] >> 20) % 1024 + self.args.z_offset * 16)
            tile_entity.pop('Pos')

    def _extract_entities(self, chunk_x, chunk_z):
        entities = []
        for entity in self.entities:
            if entity['id'] == 'LocalPlayer':
                continue

            entity_x = entity['Pos'][0] + self.args.x_offset * 16
            entity_z = entity['Pos'][2] + self.args.z_offset * 16

            if not chunk_x * 16 <= entity_x < chunk_x * 16 + 16:
                continue
            if not chunk_z * 16 <= entity_z < chunk_z * 16 + 16:
                continue

            entities.append(entity)

        return entities

    def _extract_tile_entities(self, chunk_x, chunk_z):
        tile_entities = []
        for tile_entity in self.tile_entities:
            tile_entity_x = tile_entity['x'] + self.args.x_offset * 16
            tile_entity_z = tile_entity['z'] + self.args.z_offset * 16

            if not chunk_x * 16 <= tile_entity_x < chunk_x * 16 + 16:
                continue
            if not chunk_z * 16 <= tile_entity_z < chunk_z * 16 + 16:
                continue

            tile_entities.append(tile_entity)

        return tile_entities

    def _extract_chunk_blocks(self, chunk_x, chunk_z):
        blocks = np.zeros(16 * 16 * 128, dtype=int)
        i = 0

        for x in range(chunk_x * 16, chunk_x * 16 + 16):
            for z in range(chunk_z * 16, chunk_z * 16 + 16):

                for y in range(0, self.args.y_offset):
                    blocks[i] = self.args.fill_block
                    i += 1

                for y in range(0, self.map['Height']):
                    blocks[i] = self.map['Blocks'][(y * self.map['Length'] + z) * self.map['Width'] + x]
                    i += 1

                i += 128 - self.map['Height'] - self.args.y_offset

        return blocks

    def _extract_chunk_data(self, chunk_x, chunk_z):
        data = np.zeros(16 * 16 * 64, dtype=int)
        light = np.zeros(16 * 16 * 64, dtype=int)
        i = 0

        for x in range(chunk_x * 16, chunk_x * 16 + 16):
            for z in range(chunk_z * 16, chunk_z * 16 + 16):

                for y in range(0, self.args.y_offset, 2):
                    i += 1

                for y in range(0, self.map['Height'], 2):
                    upper = self.map['Data'][(y * self.map['Length'] + z) * self.map['Width'] + x]
                    lower = self.map['Data'][((y + 1) * self.map['Length'] + z) * self.map['Width'] + x]

                    data_byte = (upper >> 4) * 16 + lower >> 4
                    data_byte -= 256 * (data_byte > 127)

                    light_byte = (upper & 15) * 16 + lower & 15
                    light_byte -= 256 * (light_byte > 127)

                    data[i] = data_byte
                    light[i] = light_byte
                    i += 1

                i += (128 - self.map['Height'] - self.args.y_offset) // 2

        return data, light

    def _calculate_height_map(self, blocks):
        height_map = np.zeros(16 * 16, dtype=int)
        transparent_blocks = [0, 6, 20, 37, 38, 39, 40, 50, 51]

        for x in range(16):
            for z in range(16):
                for y in range(128):

                    height = 127 - y
                    current_block = blocks[z * 2048 + x * 128 + height]

                    if current_block not in transparent_blocks:
                        break

                height_map[x * 16 + z] = height + 1

        return height_map

    def convert(self):
        '''
        Converts indev level data to alpha save format.
        '''
        # Ensure sane arguments
        if not 0 <= self.args.y_offset <= 128:
            raise ValueError(f"invalid y offset: {self.args.y_offset} (expected value between 0 and 128)")
        if self.args.y_offset % 2:
            raise ValueError(f"invalid y offset: {self.args.y_offset} (expected multiple of 2)")
        if not 0 <= self.args.fill_block <= 255:
            raise ValueError(f"invalid fill block ID: {self.args.fill_block} (expected value between 0 and 255)")

        # Ensure sane level
        if self.map['Length'] % 16:
            raise ValueError(f"invalid level length: {self.map['Length']:g} (expected multiple of 16)")
        if self.map['Width'] % 16:
            raise ValueError(f"invalid level width: {self.map['Width']:g} (expected multiple of 16)")
        if self.map['Height'] % 2:
            raise ValueError(f"invalid level height: {self.map['Height']:g} (expected multiple of 2)")
        if self.map['Height'] + self.args.y_offset > 128:
            raise ValueError(f"converted level height is too tall: {self.map['Height'] + self.args.y_offset:g} (expected value no more than 128)")

        # Convert
        self._convert_entities()
        self._convert_tile_entities()
        self._create_chunks()
        self._create_level_dat()

    def save(self, world_name):
        '''
        Saves converted world to disk.
        '''
        os.makedirs(world_name, exist_ok=True)

        # Save level.dat
        level_path = os.path.join(world_name, "level.dat")
        self.data.save(level_path, gzipped=True)

        # Save chunks
        for chunk in self.chunk_data:
            x = chunk['']['Level']['xPos']
            z = chunk['']['Level']['zPos']

            chunk_dir = os.path.join(world_name, np.base_repr(x % 64, 36).lower(), np.base_repr(z % 64, 36).lower())
            os.makedirs(chunk_dir, exist_ok=True)

            chunk_path = os.path.join(chunk_dir, f"c.{np.base_repr(x, 36).lower()}.{np.base_repr(z, 36).lower()}.dat")
            chunk.save(chunk_path, gzipped=True)

def main():
    import pathlib, shutil, time

    parser = argparse.ArgumentParser()
    parser.add_argument("level", type=pathlib.Path, help="level to convert")
    parser.add_argument("-o", "--output", default=None, type=pathlib.Path, help="world output directory")
    parser.add_argument("--x-offset", default=0, type=int, help="level x chunk offset", metavar="CHUNKS")
    parser.add_argument("--z-offset", default=0, type=int, help="level z chunk offset", metavar="CHUNKS")
    parser.add_argument("--y-offset", default=32, type=int, help="level y offset", metavar="BLOCKS")
    parser.add_argument("--seed", default=None, type=int, help="seed of newly created world")
    parser.add_argument("--fill-block", default=1, type=int, help="fill block ID", metavar="BLOCK_ID")
    parser.add_argument("--repopulate", action="store_true", help="repopulates chunks")
    args = parser.parse_args()

    load_start = time.time()
    world = IndevToAlphaConverter(args.level, args)
    load_end = time.time()
    print(f"{args.level}: loaded level data in {load_end - load_start:.3f}s")

    convert_start = time.time()
    world.convert()
    convert_end = time.time()
    print(f"{args.level}: converted {len(world.chunk_data)} chunks in {convert_end - convert_start:.3f}s ({(convert_end - convert_start) / len(world.chunk_data):.3f}s per chunk)")

    output_path = args.output or str(args.level).rstrip(".mclevel")

    if os.path.isdir(output_path):
        if input(f"{output_path} already exists. Overwrite? [y/N] ").lower() == 'y':
            shutil.rmtree(output_path)
        else:
            return

    save_start = time.time()
    world.save(output_path)
    save_end = time.time()
    print(f"{args.level}: saved level to {output_path} in alpha save format in {save_end - save_start:.3f}s")

if __name__ == "__main__":
    main()
