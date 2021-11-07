# indev level converter

## How to use
This program requires NBTLib, which can be installed using this command: `python -m pip install nbtlib==1.12.1`. This is an older version of nbtlib because some things in 2.0 broke this program, so make sure to use this version if you are seeing "'File' object has no attribute 'root'" errors.

Download the files from **Releases** and place it in a folder with a `.mclevel` (Indev) file. Run the python file and then wait for it to convert. Use the settings in the `config.yml` file to adjust how the converter will process the world.

Once converted, move the resulting world save folder to your minecraft saves. All worlds will be converted to the name of the original file. 

This can be loaded in any version that supports alpha save format (Infdev 20100327 - Beta 1.2_01).
Alternatively, you can also use any version that converts alpha save format into mcregion file format (Beta 1.3 - 1.1) (This is untested). 

**Some users may need to run the program as administrator to get it to work. You can do this on Windows by opening command prompt as administrator and running the program from there.**

## What this tool does
This tool converts the following into alpha save format:
* block data
* block value data
* player data
* tile entity data 
* entity data (mobs)

It also recalculates the height map.

Older Indev saves may also have some data missing (such as health), so instead a defaultt value is used to allow conversion.

## What this tool doesn't do
It doesn't convert light data or any indev data (such as skybox colour) that isn't used in alpha save format.
It cannot check whether the block IDs are compatible with the version you are upgrading to.
Deep worlds will not convert due to them being too tall.

## Recommendations
The world dimensions, type and theme are all up to you.
Some versions also have chests filled with almost every item in the game (including some unobtainables) so if you want extra blocks choose one of the versions where they are available.

## Known Issues/Byproducts of updating
Worlds are repopulated in Infdev 20100327 regardless of the tag set. That means you will see more trees, ores and caves than you might expect.

If your world crashes when you load, you may have chunks with invalid IDs in that version (probably old coloured cloths).

If your world crashes upon opening a chest, you probably have invalid IDs in that chest (again, probably coloured cloths).

When loading the world for the first time, the world will take a while to be playable because it must recalculate the light data, as it is not converted with this tool.

Mobs will not load in versions before Infdev 20100415 because they did not save again before then. The mobs will still be there after this version, so if you placed a block where a pig used to be it will suffocate in that block.

Shot arrows will not load until late Infdev/early Alpha (version unknown).

Before Indev 20100212-1, torches' attachment depended on what blocks surround them. That means if you convert a world before that version, torches will appear to be placed in mid-air. Breaking and replacing the torches in a version above this will fix this issue.
