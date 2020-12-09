# indev level converter

## How to use
Download the .py file and place it in a folder with a .mclevel file. Run the python file and then wait for it to convert.
Requires NBTLib `python -m pip install nbtlib`.

## What this tool does
This tool converts the block data, block value data, player data and tile entity data into alpha save format. It also recalculates the height map.
The world must be in the default size for this tool to work (256x256x64).

## What this tool doesn't do
It doesn't convert mobs, light data or any indev data (such as skybox colour) that isn't used in alpha save format.
Older Indev saves may also have some data missing (such as health), so instead a dummy value is placed.
It cannot convert worlds that are not the default size, nor it cannot check whether the block IDs are compatible with the version you are upgrading to.
If your world crashes when you load, you may have chunks with invalid IDs in that version (probably old coloured cloths).
If your world crashes upon opening a chest, you probably have invalid IDs in that chest (again, probably coloured cloths).

## Recommendations
For the world type, choose Island, Flat or Inland. Floating looks quite ugly when converted.
Shape and size must be set to Square and Normal.
Theme is up to you, but Hell also looks quite ugly without the red skybox.
It is also recommended to update all indev worlds to indev 20100223 first to make sure that there are no glaring issues in your world, such as weird torches.
You will need to replace all torches in infdev as the lighting only updates when you place them.
