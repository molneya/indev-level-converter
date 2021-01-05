import nbtlib
from nbtlib import *
import os

#Find world

try:
    Worlds = [f for f in os.listdir() if f.endswith('.mclevel')]
    print(f'Found world {Worlds[0]}')
    
except:
    print('No worlds found! Check that the file extension is .mclevel and that you have placed something inside the folder.')
    input()
    exit()

#load nbt

nbt_file = nbtlib.load(Worlds[0])

#Make world folder

try:
    os.mkdir('World1')
    
except:
    print('World1 folder already exists, please delete or rename to proceed (or some other error occurred with making the file).')
    input()
    exit()

#Load root tags

About = nbt_file.root['About']
Environment = nbt_file.root['Environment']
Map = nbt_file.root['Map']
Entities = nbt_file.root['Entities']
TileEntities = nbt_file.root['TileEntities']

#Check world properties

if not(Map['Height'] == 64 and Map['Length'] == 256 and Map['Width'] == 256):
    
    print('Unsupported world size. Please recreate your world with the default size to convert')
    input()
    exit()

Type_floating = input('Floating world type? (y/N) ') in ['y', 'Y', 'yes', 'Yes', 'YES']

#Get Player data

print('getting player data...', end='\r')

for i in Entities:
    
    if 'Inventory' in i:
        
        Inventory = i['Inventory']
        Motion0 = Double(i['Motion'][0])
        Motion1 = Double(i['Motion'][1])
        Motion2 = Double(i['Motion'][2])
        Pos0 = Double(i['Pos'][0] - 128)
        Pos1 = Double(i['Pos'][1] + 33)
        Pos2 = Double(i['Pos'][2] - 128)
        Rotation = i['Rotation']
        Air = i['Air']
        try: AttackTime = i['AttackTime']
        except: AttackTime = Short(0)
        try: DeathTime = i['DeathTime']
        except: DeathTime = Short(0)
        FallDistance = i['FallDistance']
        Fire = i['Fire']
        try: Health = i['Health']
        except: Health = Short(10)
        try: HurtTime = i['HurtTime']
        except: HurtTime = Short(0)
        OnGround = Byte(1)
        Score = i['Score']
        
SpawnX = Int(Map['Spawn'][0] - 128)
SpawnY = Int(Map['Spawn'][1] + 32)
SpawnZ = Int(Map['Spawn'][2] - 128)
LastPlayed = About['CreatedOn']
try: Time = Long(Environment['TimeOfDay'])
except: Time = Long(0)

#Get entity data

print('getting entity data...      ', end='\r')

EntityList = []

for i in Entities:
    
    if 'Inventory' in i:
        continue

    motion_new = []
    
    for j in i['Motion']:
        motion_new.append(Double(j))
        
    i['Motion'] = List[Double](motion_new)

    pos_new = []
    t = 0
    
    for j in i['Pos']:
        
        if t == 1: pos_new.append(Double(j + 32))
        else: pos_new.append(Double(j - 128))
        t += 1
        
    i['Pos']= List[Double](pos_new)

    try:
        i['TileX'] = Int(i['TileX'] - 128)
        i['TileY'] = Int(i['TileY'] + 32)
        i['TileZ'] = Int(i['TileZ'] - 128)
        
    except:
        pass

    try:
        i['xTile'] = Short(i['xTile'] % 16)
        i['yTile'] = Short(i['yTile'] + 32)
        i['zTile'] = Short(i['zTile'] % 16)
        
    except:
        pass

    EntityList.append(i)
    
#Get tile entities

print('getting tile entity data...  ', end='\r')

TileList = []

for i in TileEntities:
    
    pos = int(i['Pos'])
    i['x'] = Int(pos % 1024 - 128)
    i['y'] = Int((pos >> 10) % 1024 + 32)
    i['z'] = Int((pos >> 20) % 1024 - 128)
    i.pop('Pos')
    TileList.append(i)

#Get blocks into format

Blocks = Map['Blocks']
Zeroes = [Byte(0)] * 32768

print('getting block ID data...       ', end='\r')

Blocks_new = Zeroes * 256
i = 0

for a in range(0, 16):
    for b in range(0, 16):
        for z in range(a*16, a*16+16):
            for x in range(b*16, b*16+16):
    
                for j in range(0, 32):
                    Blocks_new[i+j] = Byte(not(Type_floating))
                i += 32
                
                for y in range(0, 64):
                    Blocks_new[i] = Blocks[(y * 256 + x) * 256 + z]
                    i += 1

                for j in range(0, 32):
                    Blocks_new[i+j] = Byte(0)
                i += 32

#Get data into format

Data = Map['Data']
                
print('getting block DV data...       ', end='\r')

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
                    Data_new[i] = (Data[(y * 256 + x) * 256 + z] // 16) % 16
                    i += 1

                for j in range(0, 32):
                    Data_new[i+j] = 0
                i += 32

#get the bytes and convert them to nibbles

print('converting block DV data...     ', end='\r')

Data_nibbles = []

for i in range(0, 8388608, 2):
                                    
    byte = Data_new[i+1] * 16 + Data_new[i]
    byte -= 256 * (byte > 127)
    byte = Byte(byte)                                                    
    Data_nibbles.append(byte)

#Calculate height map

print('calculating height map...      ', end='\r')

HeightMap = []

for x in range(0, 256):
    for i in range(0, 16):
        for j in range(0, 16):

            n = x*32768 + j*128*16 + i*128
            blocks_height_test = Blocks_new[n:n+128]

            for j in range(127, -1, -1):
                
                if j == 0:
                    HeightMap.append(Byte(0))
                    break

                if blocks_height_test[j] != Byte(0):
                    HeightMap.append(Byte(j))
                    break

#make new level.dat
                
print('creating level.dat...        ', end='\r')

new_file = File({
    '': Compound({
        'Data': Compound({
            'Player': Compound({
                'Inventory': Inventory,
                'Motion': List[Double]([Motion0, Motion1, Motion2]),
                'Pos': List[Double]([Pos0, Pos1, Pos2]),
                'Rotation': Rotation,
                'Air': Air,
                'AttackTime': AttackTime,
                'DeathTime': DeathTime,
                'FallDistance': FallDistance,
                'Fire': Fire,
                'Health': Health,
                'HurtTime': HurtTime,
                'OnGround': OnGround,
                'Score': Score,
                }),
            'LastPlayed': LastPlayed,
            'SpawnX': SpawnX,
            'SpawnY': SpawnY,
            'SpawnZ': SpawnZ,
            'Time': Time
            })
        })
    })

new_file.save('World1/level.dat', gzipped=True)

#make c.*.*.dat

print('creating chunk files...       ')

base36list = ['1k', '1l', '1m', '1n', '1o', '1p', '1q', '1r', '0', '1', '2', '3', '4', '5', '6', '7']
base36signed = ['-8', '-7', '-6', '-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', '6', '7']

for i in range(0, 16):
    for j in range(0, 16):

        #calc TileEntity chunk positions
        tiles_new = []
        for k in TileList:
            if (k['x'] + 128) // 16 == i and (k['z'] + 128) // 16 == j:
                tiles_new.append(k)

        #calc Entity chunk positions
        entity_new = []
        for k in EntityList:
            if (k['Pos'][0] + 128) // 16 == i and (k['Pos'][2] + 128) // 16 == j:
                entity_new.append(k)
        
        n = 16*i + j
        
        new_file = File({
            '': Compound({
                'Level': Compound({
                    'Entities': List[Compound](entity_new),
                    'TileEntities': List[Compound](tiles_new),
                    'LastUpdate': Long(200),
                    'xPos': Int(base36signed[i]),
                    'zPos': Int(base36signed[j]),
                    'Blocks': ByteArray(Blocks_new[n*32768:n*32768+32768]),
                    'Data': ByteArray(Data_nibbles[n*16384:n*16384+16384]),
                    'BlockLight': ByteArray(Zeroes[0:16384]),
                    'SkyLight': ByteArray(Zeroes[0:16384]),
                    'HeightMap': ByteArray(HeightMap[n*256:n*256+256]),
                    })
                })
            })

        try: os.mkdir(f'World1/{base36list[i]}/')
        except: pass
        try: os.mkdir(f'World1/{base36list[i]}/{base36list[j]}/')
        except: pass
        new_file.save(f'World1/{base36list[i]}/{base36list[j]}/c.{base36signed[i]}.{base36signed[j]}.dat', gzipped=True)

print(f'Converted world {Worlds[0]} to alpha save format')
