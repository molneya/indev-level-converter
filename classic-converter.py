import nbtlib
from nbtlib import *
import gzip
import os
import io

#Find world

try:
    Worlds = [f for f in os.listdir() if f.endswith('.mine')]
    print(f'Found world {Worlds[0]}')

except:
    print('No worlds found! Check that the file extension is .mine and that you have placed something inside the folder.')
    input()
    exit()

#read world file

file = open(Worlds[0], 'rb').read()

#Decode level

print('Decoding level...')

Classic_file = gzip.decompress(file)[20630:4214934]

Blocks = []

for byte in Classic_file:
    Blocks.append(Byte(byte))

#Make *.mclevel

print('Creating indev level file...')

new_file = File({
    'MinecraftLevel': Compound({
        'Environment': Compound({
            'CloudColor': Int(16777215),
            'CloudHeight': Short(66),
            'FogColor': Int(16777215),
            'SkyBrightness': Byte(100),
            'SkyColor': Int(10079487),
            'SurroundingGroundHeight': Short(23),
            'SurroundingGroundType': Byte(2),
            'SurroundingWaterHeight': Short(32),
            'SurroundingWaterType': Byte(8),
            }),
        'Map': Compound({
            'Spawn': List[Short]([Short(128), Short(36), Short(128)]),
            'Height': Short(64),
            'Length': Short(256),
            'Width': Short(256),
            'Blocks': ByteArray(Blocks),
            'Data': ByteArray([Byte(15)] * 4194304)
            })
        })
    })

new_file.save('World1.mclevel', gzipped=True)

print(f'Converted world {Worlds[0]} to indev save format')
