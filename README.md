
# Indev Level Converter

## Setup

Download and install [Python](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads) if you haven't already.

Clone the repository:
```
git clone https://github.com/molneya/indev-level-converter
cd indev-level-converter
```

Install the dependencies:
```
python -m pip install -r requirements.txt
```

You can now run the program (this shows help):
```
python indev_converter.py --help
```

## Usage

To convert a world, run the script with a world as an argument (it should end in .mclevel):
```
python indev_converter.py your_world.mclevel
```

Once converted, move the resulting world save folder to your Minecraft saves. Worlds can be loaded in any version that supports alpha save format (Infdev 20100327 - Beta 1.2_01), but they will need to be renamed for them to show up. Alternatively, you can also use any version that converts alpha save format into mcregion file format (Beta 1.3 - 1.1), however this is untested.

<!--
**Some users may need to run the program as administrator to get it to work. You can do this on Windows by opening command prompt as administrator and running the program from there.**
Note from future me: check why this was needed again?
-->

### Options

For advanced users, there are some options to fine tune how you want to convert your world:

- `-o`, `--output`: Sets output directory of the world.
- `--x-offset CHUNKS`: Sets chunk offset of the converted world in the x direction.
- `--z-offset CHUNKS`: Sets chunk offset of the converted world in the z direction.
- `--y-offset BLOCKS`: Sets **block** offset of the converted world in the y direction.
- `--seed SEED`: Sets seed of converted world. Useful if you already scouted a seed you want to place the world into.
- `--fill-block BLOCK_ID`: The block to use to fill the world when used with `--y-offset`. Use 0 (air) for floating worlds.
- `--repopulate`: Sets the TerrainPopulated tag of chunks to false. Do this if you want to regenerate ores and trees.

## Other important information

### What this tool does

This tool converts the following into alpha save format:
- block data
- block value data
- block light data
- player data
- entity data (such as mobs)
- tile entity data (such as chests)

It also calculates the height map, which doesn't exist in the indev save format.

### Known issues/byproducts of updating

Deep worlds will not convert. They are too tall.

Worlds are repopulated in Infdev 20100327 regardless of the tag set. That means you will see more trees, ores and caves than you might expect.

If your world crashes when you load, you may have chunks with invalid IDs in that version (probably coloured cloths).

If your world crashes upon opening a chest, you definitely have invalid IDs in that chest (again, probably coloured cloths).

When loading the world for the first time, the world will take a while to be playable because it must recalculate the sky light data, as it is not converted with this tool.

Mobs will not load in versions before Infdev 20100415 because they did not save. Mobs will reload after this version, so if you placed a block where a pig used to be it will suffocate in that block.

Shot arrows will not load until late Infdev/early Alpha (version unknown).

Before Indev 20100212-1, how a torch attached to a block depended on what blocks surrounded it. That means if you convert a world before that version, torches will appear to be placed in mid-air. Breaking and replacing the torches in a version above this will fix this issue.
