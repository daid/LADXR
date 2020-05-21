# Legend Of Zelda: Link's Awakening DX: Randomizer
Or, Lozlar for short.

## What is this?

TODO: Add website&link

## Usage

The only requirement to use is python3, and a proper Links Awakening ROM.

Basic usage:
`python3 main.py zelda.gbc`

The script will generate a new rom with item locations shuffled. There are many options, see `-h` on the script for details.

## Development

This is still in the early stage of development. Important bits are:
* `randomizer.py`: Contains the actual logic to randomize the rom, and checks to make sure it can be solved.
* `logic/*.py`: Contains the logic definitions of what connects to what in the world and what it requires to access that part.
* `locations/*.py`: Contains definitions of location types, and what items can be there. As well as the code on how to place an item there. For example the Chest class has a list of all items that can be in a chest. And the needed rom patch to put that an item in a specific chest.
* `patches/*.py`: Various patches on the code that are not directly related to a specific location. But more general fixes 
