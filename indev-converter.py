import nbtlib
from nbtlib import *
import numpy
import os

#Make world folder
try: os.mkdir('World1')
except:
    print('World folder already exists, please delete or rename to proceed')
    input()
    exit()

#load world and datas
worlds = [f for f in os.listdir() if f.endswith('.mclevel')]
nbt_file = nbtlib.load(worlds[0])

About = nbt_file.root['About']
Map = nbt_file.root['Map']
Entities = nbt_file.root['Entities'] #Does this need to be implemented? early infdev doesnt save entities anyway.
TileEntities = nbt_file.root['TileEntities']

#Get data
for i in Entities:
    if "Inventory" in i:
        Inventory = i["Inventory"]
        Motion0 = float(i["Motion"][0])
        Motion1 = float(i["Motion"][1])
        Motion2 = float(i["Motion"][2])
        Pos0 = float(i["Pos"][0])
        Pos1 = float(i["Pos"][1]+32)
        Pos2 = float(i["Pos"][2])
        Rotation = i["Rotation"]
        Air = i["Air"]
        FallDistance = i["FallDistance"]
        Fire = i["Fire"]
        id = i["id"]
        Score = i["Score"]
        
SpawnX = int(Map["Spawn"][0])
SpawnY = int(Map["Spawn"][1]+32)
SpawnZ = int(Map["Spawn"][2])

LastPlayed = About["CreatedOn"]

Blocks = Map['Blocks']
Data = Map['Data']
Zeroes = [Byte(0)] * 32768

print("getting tile entities...")
#Get tile entities
Tiles = []
for i in TileEntities:
    pos = int(i['Pos'])
    i['x'] = Int(pos % 1024)
    i['y'] = Int((pos >> 10) % 1024 + 32)
    i['z'] = Int((pos >> 20) % 1024)
    i.pop('Pos')
    Tiles.append(i)

print("getting data values...")
#Get data into format
Data_new = Zeroes * 256
i = 0
for a in range(0, 16):
    for b in range(0, 16):
        for z in range(a*16, a*16+16):
            for x in range(b*16, b*16+16):

                for j in range(0, 32):
                    Data_new[i+j] = 0
                i += 32
                
                for y in range(0, 64):
                    Data_new[i] = (int(Data[(y * 256 + x) * 256 + z]) // 16) % 16
                    i += 1

                for j in range(0, 32):
                    Data_new[i+j] = 0
                i += 32


print("converting data values...")
Data_nibbles = []
for i in range(0, 8388608, 2):
                                    
    byte1 = Data_new[i] * 16 + Data_new[i]
    byte1 -= 256 * (byte1 > 127)
    byte1 = Byte(byte1)                        
                                    
    Data_nibbles.append(byte1)

    
print("getting block values...")
#Get blocks into format
Blocks_new = Zeroes * 256
i = 0
for a in range(0, 16):
    for b in range(0, 16):
        for z in range(a*16, a*16+16):
            for x in range(b*16, b*16+16):

                for j in range(0, 32):
                    Blocks_new[i+j] = Byte(1)
                i += 32
                
                for y in range(0, 64):
                    Blocks_new[i] = Blocks[(y * 256 + x) * 256 + z]
                    i += 1

                for j in range(0, 32):
                    Blocks_new[i+j] = Byte(0)
                i += 32

print("calculating height map...")
#Calculate height map
HeightMap = []
for i in range(0, 8388608, 128):
    blocks_height_test = Blocks_new[i:i+128]
    for j in range(127, 0, -1):
        if blocks_height_test[j] != Byte(0):
            HeightMap.append(Byte(j))
            break
                
print("making level.dat...")
#make new level.dat
new_file = File({
    '': Compound({
        'Data': Compound({
            'Player': Compound({
                "Inventory": Inventory,
                "Motion": List[Double]([Double(Motion0), Double(Motion1), Double(Motion2)]),
                "Pos": List[Double]([Double(Pos0), Double(Pos1), Double(Pos2)]),
                "Rotation": Rotation,
                "Air": Air,
                "FallDistance": FallDistance,
                "Fire": Fire,
                "id": id,
                "Score": Score
                }),
            'LastPlayed': LastPlayed,
            'SpawnX': Int(SpawnX),
            'SpawnY': Int(SpawnY),
            'SpawnZ': Int(SpawnZ),
            })
        })
    })
new_file.save('World1/level.dat', gzipped=True)

n = 0

print("making chunk files...")
#make c.*.*.dat
for i in range(0, 16):
    for j in range(0, 16):

        #calc TileEntity chunk positions
        tiles_new = []
        for k in Tiles:
            if k['x'] // 16 == i and k['z'] // 16 == j:
                tiles_new.append(k)
        
        n = 16*i + j
        new_file = File({
            '': Compound({
                'Level': Compound({
                    'TileEntities': List[Compound](tiles_new),
                    'LastUpdate': Long(200),
                    'xPos': Int(i),
                    'zPos': Int(j),
                    'Blocks': ByteArray(Blocks_new[n*32768:n*32768+32768]),
                    'Data': ByteArray(Data_nibbles[n*16384:n*16384+16384]),
                    'BlockLight': ByteArray(Zeroes[0:16384]),
                    'SkyLight': ByteArray(Zeroes[0:16384]),
                    'HeightMap': ByteArray(HeightMap[0:256])
                    })
                })
            })

        i_hex = str(hex(i))[-1]
        j_hex = str(hex(j))[-1]
        try: os.mkdir(f'World1/{i_hex}/')
        except: pass
        try: os.mkdir(f'World1/{i_hex}/{j_hex}/')
        except: pass
        new_file.save(f'World1/{i_hex}/{j_hex}/c.{i_hex}.{j_hex}.dat', gzipped=True)

print("converted world", worlds[0], "to alpha save format")
