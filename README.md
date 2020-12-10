# indev level converter

## How to use
Download the .py file and place it in a folder with a .mclevel file. Run the python file and then wait for it to convert. 
All worlds will be converted to the name "World1". 
Move this folder into your minecraft saves and then load any version that supports alpha save format (Infdev 20100327 - Beta 1.2_01).
Alternatively, you can also use any version that converts alpha save format into mcregion file format (Beta 1.3 - 1.1). [Untested]

Requires NBTLib `python -m pip install nbtlib`.

## What this tool does
This tool converts the block data, block value data, player data, tile entity data and entity data (mobs) into alpha save format. 
It also recalculates the height map.
The world must have the shape and size set to Square and Normal to be able to be converted (256x256x64).

## What this tool doesn't do
It doesn't convert light data or any indev data (such as skybox colour) that isn't used in alpha save format.
Older Indev saves may also have some data missing (such as health), so instead a dummy value is placed.
It cannot convert worlds that are not the default size, nor it cannot check whether the block IDs are compatible with the version you are upgrading to.
If your world crashes when you load, you may have chunks with invalid IDs in that version (probably old coloured cloths).
If your world crashes upon opening a chest, you probably have invalid IDs in that chest (again, probably coloured cloths).

## Recommendations
For the world type, choose Island, Flat or Inland. Floating looks quite ugly when converted.
Shape and size must be set to Square and Normal.
Theme is up to you, but Hell also looks quite ugly without the red skybox.
Some versions also have chests filled with almost every item in the game (including some unobtainables) so if you want extra blocks choose one of the versions where they are available.

## Known Issues
When loading the world for the first time, the world will take a while to be playable because it must recalculate the light data, as it is not converted with this tool.

Mobs will not load in versions before Infdev 20100415 because they did not save again before then.
The mobs will still be there after this version, so if you placed a block where a pig used to be it will suffocate in that block.

Shot arrows will not load until late Infdev/early Alpha (version unknown).

Before Indev 20100212-1, torches' attachment depended on what blocks surround them.
That means if you convert a world before that version, torches will appear to be placed in mid-air.
Breaking and replacing the torches in a version above this will fix this issue.

Farmland dehydrates upon conversion. This is probably due to the difference in how farmland worked.
