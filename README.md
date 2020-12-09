# indev level converter

## How to use
Download the .py file and place it in a folder with a .mclevel file. Run the python file and then wait for it to convert.
Requires NBTLib `python -m pip install nbtlib`.

#### What this tool does
This tool converts the block data, block value data, player data and spawn into alpha save format. It also calculates a new height map (although buggy).
The world must be in the default size for this tool to work (256x256x64).

#### What this tool doesn't do
It doesn't convert mobs, light data or any indev data (such as skybox colour, about) that isn't used in alpha save format.
It cannot convert worlds that are not the default size.

#### Bugs
Block data and height map seem to bee buggy, although they do work.
I have tested on indev versions 20100128 and 20100218 converting to infdev 20100327.
