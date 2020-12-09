# indev level converter

## How to use
Download the .py file and place it in a folder with a .mclevel file. Run the python file and then wait for it to convert.
Requires NBTLib `python -m pip install nbtlib`.

#### What this tool does
This tool converts the block data, block value data, player data and tile entity data into alpha save format. It also recalculates the height map.
The world must be in the default size for this tool to work (256x256x64).

#### What this tool doesn't do
It doesn't convert mobs, light data or any indev data (such as skybox colour) that isn't used in alpha save format.
Older Indev saves may also have some data missing (such as health), so instead a dummy value is placed.
It cannot convert worlds that are not the default size, nor it cannot check whether the block IDs are compatible with the version you are upgrading to.
If your world crashes when you load, you may have chunks with invalid IDs in that version (probably old coloured cloths).
If your world crashes upon opening a chest, you probably have invalid IDs in that chest (again, probably coloured cloths).
