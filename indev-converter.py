import nbtlib
from nbtlib import *
import numpy
import os

#Find world
worlds = [f for f in os.listdir() if f.endswith('.mclevel')]
try: nbt_file = nbtlib.load(worlds[0])
except:
    print("No worlds found! Check that the file extension is .mclevel and that you have placed something inside the folder.")
    input()
    exit()

#Make world folder
try: os.mkdir('World1')
except:
    print('World folder already exists, please delete or rename to proceed.')
    input()
    exit()

#Load root tags
About = nbt_file.root['About']
Environment = nbt_file.root['Environment']
Map = nbt_file.root['Map']
Entities = nbt_file.root['Entities'] #Does this need to be implemented? early infdev doesnt save entities anyway.
TileEntities = nbt_file.root['TileEntities']

print("getting inventory data...")
#Get data
for i in Entities:
    if "Inventory" in i:
        Inventory = i["Inventory"]
        Motion0 = Double(i["Motion"][0])
        Motion1 = Double(i["Motion"][1])
        Motion2 = Double(i["Motion"][2])
        Pos0 = Double(i["Pos"][0])
        Pos1 = Double(i["Pos"][1]+32)
        Pos2 = Double(i["Pos"][2])
        Rotation = i["Rotation"]
        Air = i["Air"]
        try: AttackTime = i["AttackTime"]
        except: AttackTime = Short(0)
        try: DeathTime = i["DeathTime"]
        except: DeathTime = Short(0)
        FallDistance = i["FallDistance"]
        Fire = i["Fire"]
        try: Health = i["Health"]
        except: Health = Short(10)
        try: HurtTime = i["HurtTime"]
        except: HurtTime = Short(0)
        OnGround = Byte(0)
        Score = i["Score"]
        
SpawnX = Int(Map["Spawn"][0])
SpawnY = Int(Map["Spawn"][1]+32)
SpawnZ = Int(Map["Spawn"][2])
LastPlayed = About["CreatedOn"]
try: Time = Long(Environment["TimeOfDay"])
except: Time = Long(0)

Blocks = Map['Blocks']
Data = Map['Data']
Zeroes = [Byte(0)] * 32768

print("getting tile entity data...")
#Get tile entities
Tiles = []
for i in TileEntities:
    pos = int(i['Pos'])
    i['x'] = Int(pos % 1024)
    i['y'] = Int((pos >> 10) % 1024 + 32)
    i['z'] = Int((pos >> 20) % 1024)
    i.pop('Pos')
    Tiles.append(i)

print("getting block ID data...")
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

print("getting block DV data...")
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
                    if Blocks_new[i] in [Byte(6), Byte(8), Byte(9), Byte(10), Byte(11), Byte(50), Byte(51), Byte(55), Byte(59), Byte(60), Byte(61), Byte(62)]:
                        Data_new[i] = (int(Data[(y * 256 + x) * 256 + z]) // 16) % 16
                    else:
                        Data_new[i] = Byte(0)
                    i += 1

                for j in range(0, 32):
                    Data_new[i+j] = 0
                i += 32

print("converting data...")
Data_nibbles = []
for i in range(0, 8388608, 2):
                                    
    byte1 = Data_new[i] * 16 + Data_new[i]
    byte1 -= 256 * (byte1 > 127)
    byte1 = Byte(byte1)                        
                                    
    Data_nibbles.append(byte1)

print("calculating height map...")
#Calculate height map
HeightMap = []
for x in range(0, 256):
    for i in range(0, 16):
        for j in range(0, 16):

            n = x*32768 + j*128*16 + i*128
            blocks_height_test = Blocks_new[n:n+128]

            for j in range(127, 0, -1):
                if blocks_height_test[j] != Byte(0):
                    HeightMap.append(Byte(j))
                    break
                
print("creating level.dat...")
#make new level.dat
new_file = File({
    '': Compound({
        'Data': Compound({
            'Player': Compound({
                "Inventory": Inventory,
                "Motion": List[Double]([Motion0, Motion1, Motion2]),
                "Pos": List[Double]([Pos0, Pos1, Pos2]),
                "Rotation": Rotation,
                "Air": Air,
                "AttackTime": AttackTime,
                "DeathTime": DeathTime,
                "FallDistance": FallDistance,
                "Fire": Fire,
                "Health": Health,
                "HurtTime": HurtTime,
                "OnGround": OnGround,
                "Score": Score,
                }),
            'LastPlayed': LastPlayed,
            'SpawnX': SpawnX,
            'SpawnY': SpawnY,
            'SpawnZ': SpawnZ,
            'Time': Time,
            })
        })
    })
new_file.save('World1/level.dat', gzipped=True)

n = 0

print("creating chunk files...")
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
                    'HeightMap': ByteArray(HeightMap[n*256:n*256+256])
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
