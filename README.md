# indev level converter

## How to use
Download the .py file and place it in a folder with a .mclevel (Indev) or .mine (classic) file. Run the python file and then wait for it to convert. 
All worlds will be converted to the name "World1".

Some users may need to run the program as administrator to get it to work. You can do this on Windows by opening command prompt as administrator and running the program from there.

For Indev converts, move this folder into your minecraft saves and then load any version that supports alpha save format (Infdev 20100327 - Beta 1.2_01).
Alternatively, you can also use any version that converts alpha save format into mcregion file format (Beta 1.3 - 1.1) (This is untested). 

For Classic converts, all you need to do is load the file through the file explorer in Minecraft.

Requires NBTLib: `python -m pip install nbtlib`

If you have any problems, you can contact me on discord `molneya#3078`. I'm usually pretty quick to reply assuming I'm awake.

## What this tool does
For Indev, this tool converts the block data, block value data, player data, tile entity data and entity data (mobs) into alpha save format. 
It also recalculates the height map.
Older Indev saves may also have some data missing (such as health), so instead a dummy value is used to allow conversion.
The world must have the shape and size set to Square and Normal to be able to be converted (256x256x64).

For Classic, it takes the raw block data and converts it into Indev level format.
It also adds Environment data (such as skybox color) to the default on a normal island world.

## What this tool doesn't do
It doesn't convert light data or any indev data (such as skybox colour) that isn't used in alpha save format.
It cannot convert worlds that are not the default size, nor it cannot check whether the block IDs are compatible with the version you are upgrading to.

## Recommendations
For the world type, choose Island, Flat or Inland. Floating looks quite ugly when converted.
Shape and size must be set to Square and Normal.
Theme is up to you, but Hell also looks quite ugly without the red skybox.
Some versions also have chests filled with almost every item in the game (including some unobtainables) so if you want extra blocks choose one of the versions where they are available.

## Known Issues
The world will not convert if the shape and size is not set to Square and Normal.
Other world shapes may be supported in the future.

Worlds are repopulated once updating. That means you will see more trees, ores and caves than you might expect.

If your world crashes when you load, you may have chunks with invalid IDs in that version (probably old coloured cloths).

If your world crashes upon opening a chest, you probably have invalid IDs in that chest (again, probably coloured cloths).

When loading the world for the first time, the world will take a while to be playable because it must recalculate the light data, as it is not converted with this tool.

Mobs will not load in versions before Infdev 20100415 because they did not save again before then.
The mobs will still be there after this version, so if you placed a block where a pig used to be it will suffocate in that block.

Shot arrows will not load until late Infdev/early Alpha (version unknown).

Before Indev 20100212-1, torches' attachment depended on what blocks surround them.
That means if you convert a world before that version, torches will appear to be placed in mid-air.
Breaking and replacing the torches in a version above this will fix this issue.
