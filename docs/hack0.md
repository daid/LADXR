---
title: Hack0 - What the hack?
---

# Hack0 - What the hack?

I maintain [LADXR](https://daid.github.io/LADXR/). And every month, I hold a "special" kind of "race" within this randomizer.

It's just a for fun thing. Where I try out new things, new settings, or things that are not really something that can integrate well into the main randomizer, but still fun to try once.

Just to list things that we've done in these hacks:
* Money = life. You start with 300 rupees, every second, one rupees is subtraced. If you have zero rupees left, you die. Instead normal damage, damage goes to rupees as well.
* Easter egg hunt. Seashells where replaced with eggs. And you needed 20 eggs to open the windfish egg. This was introduced as a normal setting for "seashell hunt goal" after this.
* Fish-da-pond. Silly hack where you had to fish the fishing minigame empty to win.
* jenglish. All texts where pulled trough google translated to japanese, and then back to english.
* SuperHot. The game only advances while you hold a button.
* Superweapons, all items got really strong, you can put down tons of bombs, shoot arrows fast, etc. People enjoyed this so much that is became a setting.
* Bossrush, before the nightmare boss you first got to fight every other boss.
* Wrecking ball, you always have the D7 wrecking ball with you.

Not all of these work out great. But that's kinda the idea, just to try things. Sometimes is fun, sometimes it wack, sometimes it becomes a new setting.

One thing is sure. Each and every one of these is a huge **hack**.

And that brings us to the story of today...

# Final Fantasy Adventure.

As a side project, I've been reverse engineering the gameboy game Final Fantasy Adventure. You can read all about that at https://daid.github.io/FFA-Disassembly/

Now. I had the crazy idea. [Super Metroid + A link to the past](https://samus.link/) randomizer is a thing. Which combines two super nintendo games into one. Could I do the same for Links Awakening?

Cool idea. But is it actually workable?

![image](https://user-images.githubusercontent.com/964186/162227436-747aff94-0249-45ed-b5c8-0f064e74294e.png)

## Problem one... banking

Just append rom one rom to the other right? Simple. Done. Next!

Life is never this easy in gameboy development. First off, you have to understand a bit of how the gameboy hardware works. The gameboy CPU can only acces 32KByte of the cartridge. Which worked fine for tetris. But, for bigger games, like LADX and FFA, it no longer cuts it.

So ROM Banking was introduced. The 32KByte area is divided into two 16KByte areas. And the 2nd 16KByte area can be swapped out with different parts of the ROM at will. This swapping out is handled by [MBCs](https://gbdev.io/pandocs/MBCs.html).

So, just swap out LADX with FFA and you're done. No, wait... only the 2nd 16KByte area can be swapped out. And the first 16KByte is filled with really important stuff for both LADX and FFA... idea busted?

### Bring in... MBC1

[MBC1](https://gbdev.io/pandocs/MBC1.html) it's our saviour for this hack. It's the only MBC that allows swapping out the first 16KByte area. Still, it puts some heavy limits on what we can do:
1) The lower 16KByte area follows the selected part for the higher 16Byte area, as it's the selected bank number rounded down to multiple of `$20`
2) Only one SRAM bank can be used, as SRAM bank selection follows this low area ROM selection, and that would result in pure chaos otherwise
3) Switching ROM banks is two writes instead of one
4) Bank numbers that are multiples of $20 can only be used for the lower area
5) Writes to memory addresses `$4000-$7FFF` mess with this method, while generally harmless/ignored with other MBCs

LADX normally uses MBC5, which is more sane then MBC1. So our first challange is to make LADX work with MBC1.

#### LADX problem one, $40 banks

LADX is quite large, it has `$40` rom banks. Remember point 1? Every $20 banks we need the lower bank. Sadly, we cannot just ignore bank $20 of LADX, there is a lot of things in there. But, what we can do, is just move over bank `$20` and every bank after that to `$21+` and then copy over bank `$00` to bank `$20`.

Why can we do this? Well, the last two banks of LADX are empty, unused. So we can just ignore that we now would need a bank `$40`, as that is unused.

#### LADX problem two, switching banks

Next off, we need to fix our bank switching problem. Normally a bank switch happens with:
```asm
ld a, $XX ; XX=Bank number
ld [$2100], a
```
But, for MBC1, we need to write the lower 5 bits of the bank number in $2XXX and the upper bit in $4XXX. (Upper bit? not more? No. We only need one more bit to reach the full range of banks we need for LADX)

But we also need to offset for the "gap" at $20. So the whole code to switch a bank becomes:
```asm
        push af
        cp   $20
        jr   c, lowerBanks
        inc  a
        ld   [$2001], a
        ld   a, $01
        ld   [$4001], a
        jr   done
lowerBanks:
        ld   [$2001], a
        xor  a
        ld   [$4001], a
done:
        pop  af
```

We cannot jam this many instruction in the spot for normally two instructions. So, what I did was place the above code somewhere in the bank $00, so it is always accessible. (there is quite some space here in LADX)

After that, I replaced every `ld [$2100], a` with `call $00C0` ($00C0 is where I could place this new code). And when I say, all of them. I mean.. ALL OF THEM. There are so many of these, it's a bit insane.
```py
for addr in (0x080F, 0x0819, 0x0821, 0x082B, 0x08E2, 0x0919, 0x0939, 0x0974, 0x098D, 0x0A13, 0x0A2E, 0x0A35, 0x0A62, 0x0B1C, 0x0B2B, 0x0B58, 0x0B5D, 0x0B65, 0x0B6A, 0x0B92, 0x0BC8, 0x0BD3, 0x0BDA, 0x0BE3, 0x0BF2, 0x0C2F, 0x0C3C, 0x0C47, 0x0D20, 0x0EEF, 0x0EFE, 0x0F07, 0x1298, 0x1356, 0x137E, 0x1399, 0x14BF, 0x1824, 0x1833, 0x19A6, 0x1A35, 0x1A4C, 0x1E38, 0x1E65, 0x1E6E, 0x1E98, 0x1EAC, 0x1EC4, 0x1EDD, 0x1F43, 0x2050, 0x220B, 0x223E, 0x22BA, 0x22E7, 0x27DF, 0x2A03, 0x2A14, 0x2A32, 0x2A3C, 0x2A6B, 0x2A7F, 0x2A93, 0x2AB3, 0x2AC7, 0x2ADB, 0x2B06, 0x2B17, 0x2B39, 0x2B52, 0x2B63, 0x2B95, 0x2BA6, 0x2C3B, 0x2C79, 0x2C9F, 0x2CB3, 0x2CCE, 0x2CDD, 0x2D5D, 0x2E26, 0x2EF2, 0x2F21, 0x2F77, 0x2F91, 0x2FB2, 0x3058, 0x3084, 0x311B, 0x3126, 0x317E, 0x31B5, 0x3237, 0x3547, 0x3808, 0x38E6, 0x38ED, 0x38F8, 0x3911, 0x3F95, 0x3FAB, 0x3FCB, 0x3FDA, 0x3FEB, 0x1AD6, 0x1B2C, 0x1C0D, 0x1C62, 0x1C6C, 0x1C74, 0x1C7E, 0x1D0F, 0x1D1A, 0x1D2B, 0x1DF5, 0x1E25, 0x2908, 0x2910, 0x24B9, 0x24CF, 0x252B, 0x2573, 0x260D, 0x263E, 0x26C5, 0x3927, 0x3985, 0x39D7, 0x39E8, 0x3A14, 0x3A32, 0x3A59, 0x3A64, 0x3A89, 0x3A8F, 0x3AA6, 0x3B89, 0x3B9B, 0x3CDB, 0x3F55, 0x0414, 0x044F, 0x045A, 0x0566, 0x05B7, 0x05F3, 0x062A, 0x065B, 0x06F7, 0x07EF, 0x027E, 0x02B9): # 0x0764
    # replace ld [MBC], a
    rom.patch(0x00, addr, ASM("ld [$2100], a"), ASM("call $00C0"))
for addr in (0x0836, 0x0847, 0x0858, 0x0865, 0x08D7, 0x08E6, 0x08F0, 0x08FB, 0x0905, 0x090F, 0x092F, 0x0979, 0x0983, 0x09C9, 0x09D4, 0x09DF, 0x09EA, 0x09F6, 0x0A48, 0x0A54, 0x0A6C, 0x0A78, 0x0A84, 0x0A90, 0x0AB6, 0x0AC7, 0x0AD3, 0x0AEB, 0x0AF7, 0x0B02, 0x0B41, 0x0F1A, 0x0F6A, 0x0FD0, 0x100A, 0x10CB, 0x1165, 0x128D, 0x134B, 0x1373, 0x138E, 0x14B4, 0x1819, 0x1828, 0x1A22, 0x1A2A, 0x1A39, 0x1A41, 0x20BF, 0x20C7, 0x20EC, 0x2156, 0x2178, 0x2234, 0x2291, 0x22B0, 0x22DD, 0x27F7, 0x2802, 0x29ED, 0x29F8, 0x2A07, 0x2BC2, 0x2E79, 0x3023, 0x30FC, 0x3109, 0x3111, 0x328E, 0x3296, 0x329E, 0x32CD, 0x37FE, 0x38D4, 0x38DC, 0x38FC, 0x1C00, 0x1CFF, 0x1D1E, 0x3942, 0x394D, 0x3965, 0x3970, 0x397B, 0x39CE, 0x3A0A, 0x3B18, 0x3B23, 0x3B2E, 0x3B39, 0x3B44, 0x3B4F, 0x3B5A, 0x3B65, 0x3B70, 0x3B7B, 0x3C69, 0x3D47, 0x0177, 0x018F, 0x019D, 0x01C2, 0x01CF, 0x0409, 0x0431, 0x043D, 0x0445, 0x04DA, 0x0530, 0x054B, 0x055B, 0x0622, 0x06A9, 0x07B0, 0x025C, 0x026E, 0x02AA):
    # replace callsb
    rom.patch(0x00, addr + 2, ASM("ld [$2100], a"), ASM("call $00C0"))
for addr in (0x2319, 0x30EC, 0x3915, 0x391D, 0x1BC5, 0x236B, 0x23CA, 0x247D, 0x24AF, 0x27AF, 0x27BB):
    # replace jpsb
    rom.patch(0x00, addr + 2, ASM("ld [$2100], a"), ASM("call $00C0"))
```

Next! problem... there is also this:
```asm
ld hl, $2100
ld [hl], $XX ; XX=Bank number
```
It's done like that the preserve A. So we have to call the above code, and preserve A. And all that in 5 bytes (first instruction is 3 bytes, second is 2 bytes). Seems impossible? Saving A is two bytes, calling the function is 3. That's our 5 instruction budget gone. Project dead? No. As there is a lot more text after this.

We have the `rst` instruction it's a function call of only 1 byte. And it's our save in this case:
```asm
push af
ld   a, $XX
rst  $30
pop  af
```
Fits within the 5 byte limit. And at $0030 we have a tiny bit of room to add `jp $00C0` (there isn't enough room to put our normal function there)

Yay, we can switch banks properly.

### LADX problem three, LADX fights back.

Game seems to boot, run, and then crash. What's happening? Did I miss a bank switch? No. I missed something else. I missed:
```asm
ld hl, $4000
ld [hl], $00
```
It's switching to RAM bank `$00`, but for MBC1, this also switches out the high bank bit. Suddenly switching rom banks pretty much brings down the house.

Lucky for us, it's only doing this for classic gameboy (DMG) support, where it uses the other SRAM bank. But on the GBC, it doesn't use other SRAM banks, it uses WRAM banks instead. Doesn't make sense? No idea. But it does. Don't worry about it. Only thing you need to know, we can just remove those instructions and be happy.

Game boots, doesn't crash, and I can start a... damn it. Links sprite is corrupt. What why? The game otherwise runs perfectly, except for occasional corruption of link.

Why does that happen? Well, remember replacing one instruction with a call to a whole bunch? That affects timing. And timing is a thing. Especially for updating graphics. The gameboy has a limited amount of time available to update graphics memory. If you try to access that memory while rendering is happening, you cannot, and writes will fail silently. Which is what was happening. Updating links sprite was too late now, and only partially happening.

How to fix this? Well, this code that updates links sprite needs to copy 64 bytes to update link, and it does so in two steps of 32bytes. The [copy loop](https://github.com/zladx/LADX-Disassembly/blob/91e2ebb9b81982dc7404114442506811122b7cf9/src/code/home/animated_tiles.asm#L422) that does this is realtively small, but not very efficient. It takes 10 cycles per byte.

Luckily for us, we only target the GBC, and that has DMA. It can copy 16 bytes in 32 cycles, which is a lot faster. So updating this code to use DMA fixes that issue. DMA has some limitations, it can only copy from/to addresses that are 16 byte aligned and only blocks that are multiple of 16, but that all isn't an issue here.

So now the game runs, with MBC1.

### Or, wait, remember this thing?

Remember that we dropped of the last bank from LADX, as we didn't "need" it. Guess who needs it. I do for LADXR. I use it to store some extra code. So while the base game runs, I broke the randomizer. I moved this code from bank `$3F` to `$0C`. `$0C`? Yes. `$0C`. It's a bank with graphics, graphics for the classic gameboy variant. And as we are GBC only anyhow with the patches we already have, it's safe to abuse that bank for our code.

## Problem two... FFA?

Now, running FFA with MBC1. FFA is using [MBC2](https://gbdev.io/pandocs/MBC2.html), which has a different control scheme for banking. But, luck shines on us. FFA is written in a way that also works with MBC1. We can just switch to a different MBC and it works. We could use some luck in this project for once.

I guess this is why you see address `$2100` being used for bank switching. It switches banks on all MBCs.

As I didn't want people to play the whole game of FFA (as it's too long for something like this) I patched the script where you exit after defeating the first boss twice. Normally you jump out of the castle. Instead, I just made it jump to the ending credits instead. This was relatively straightforward.

## Problem three... CGB

Final problem before we can start putting this all together. LADX is running in GBC mode. FFA normally runs in classic mode. If we run FFA in GBC mode we get...

![image](https://user-images.githubusercontent.com/964186/162275000-7fc0cca6-dd0a-424a-bea8-b06fe855e912.png)

Which makes perfect sense. With GBC support enabled, we need to load colors. And the default colors for the background are all white, while those for sprites are undefined and random. So lets load some default palette, there is a bit of free room in FFA before the interrupt vectors. So we use that to store some code, jump to it from the start and then jump to the actual start of the rom.

```asm
PreInit:
    ld  a, $80
    ldh [rBCPS], a
    ldh [rOCPS], a
    ld  hl, Pal
    ld  c, $08
:   ld  a, [hl+]
    ldh [rBCPD], a
    ldh [rOCPD], a
    dec c
    jr  nz, :-
    jp  Init
Pal:
    dw $7fff, $3def, $1ce7, $0000
```
![image](https://user-images.githubusercontent.com/964186/162277109-91d08967-879d-42a7-9814-f761d4c95cc2.png)

That is a lot better, but far from perfect. There are a few obvious problems. Sprites are darker then then expected, and various animation effects don't work. For example screen transitions:

![animation](https://user-images.githubusercontent.com/964186/162278393-9ca53b83-faf1-4a72-ab63-b6b663f07939.gif)

The reason for this is simple. FFA is updating the [rBGP](https://gbdev.io/pandocs/Palettes.html) and [rOBPx](https://gbdev.io/pandocs/Palettes.html) registers to get the gray scales it wants, and also to black or white out the screen.
As bonus, it's updating this while the frame is drawing so it does not black out the status bar, while it does black out the rest of the screen.

So, new plan. Depending on the value of `rBGP` and `rOBP0` update the CGB palette data at each VBLANK or LCDC interrupt (End of frame, or special interrupt on a specific line)
We need a bit more code in this case:
```asm
PaletteData:
MACRO RGB
    dw (\1) | (\2) << 5 | (\3) << 10
ENDM
    RGB 29, 31, 25
    RGB 21, 26, 18
    RGB 10, 17, 14
    RGB 2, 5, 7

updatePal:
    xor a
    ld  h, a
    ld  l, a
    ld  a, $80
    ldh [rBCPS], a
    ldh [rOCPS], a
    ld c, LOW(rBCPD)
    ld a, [rBGP]
    call updatePalFunc
    ld c, LOW(rOCPD)
    ld a, [rOBP0]
    call updatePalFunc
    ret

updatePalFunc:
    ld e, a
    ld b, 4
:
    ld a, e
    rr e
    rr e
    and $03
    add a, a
    ld  l, a
    ld  a, [hl+]
    ldh [c], a
    ld  a, [hl+]
    ldh [c], a
    dec b
    jr  nz, :-
    ret
 ```

![animation](https://user-images.githubusercontent.com/964186/162280644-c89fc948-0361-4053-a31d-ee3c9a820952.gif)

 Well, that works for some effects. But it doesn't work for some others. At this point, I'm not sure why. But it's 22:00, friday, and I always host these specials starting on saturday. So, screw it. Don't let perfect be the enemy of good enough in this case.
 
 Biggest issue is that the boss doesn't flash when you hit it. I traced this later to "why", the boss uses `rBGP1` instead of `rBGP0`, and the game just inverts `rBGP1` when the boss is hit. Small change to use `rBGP1` instead of `rBGP0` in the palette update code confirms this, as now all sprites flash when you hit the boss. This is most certainly something that can be fixed/improved, but it requires a lot more work.
 
## Problem four, putting it all together.
 
 Now. As this is just a "quick" hack (quick is relative...), I can cheat in a whole bunch of ways:
 * I don't care that people cannot finish LADX
 * I only want to go from LADX to FFA
 * I shorten the game of FFA to a "gimic", as requiring people to finish a whole game that they don't even know would be brutal especially...
 * Saving in FFA will corrupt the LADX save, and the other way around.

So, the plan is simple:
* Start with the LADX rom
* Append the customized FFA rom
* Use the MBC1 higher rom bits to switch to FFA at some point, and start that game from scratch

The whole switch code isn't that complex:
* I need to clear some GBC VRAM, because, well, else some things are messed up, as FFA doesn't touch it.
* Load some code into ram, so we can safely switch games
* Jump to that code to switch games, and that code will start up FFA from the entry point at `$0100`

```
    ; Disable interrupts, as that can mess up things quite quick
    xor a
    di
    ldh [$FF], a
    ldh [$0F], a
    ldh [$40], a ;LCD off
; Clear 2nd vram bank
clearVRAM:
    ld  a, $01
    ldh [$4F], a
    ld  hl, $8000
    ld  bc, $2000
    xor a
.loop:
    ldi [hl], a
    dec c
    jr  nz, .loop
    dec b
    jr  nz, .loop
    ldh [$4F], a    
    
    ld  a, $91
    ldh [$40], a ;LCD on
    
SwitchROM:
    ; Load code into RAM and jump to RAM
    ld   de, switchRomCode
    ld   hl, $C000
    ld   c, $20
.loop:
    ld   a, [de]
    inc  de
    ldi  [hl], a
    dec  c
    jr   nz, .loop
    jp   $C000
switchRomCode:
    ld   a, $00
    ld   [$2000], a
    ld   a, $02
    ld   [$4000], a
    ld   a, $11
    jp   $0100
.end:
```

# Succes... AH FUCK.

Yay, that all worked. I called this code from the code that handles getting an instrument, and all seemed good...

It's now 23:50. I upload my patch, setup the generator for the race. And download a generated rom to see if everything goes right.
Generator worked fine. I playtest a bit and.... crash. Bombing a bombable wall crashes the whole game in LADX. Shit. Somewhere it's writting to the `$6XXX` area.

I did the only thing I could at that point, and just remove that specific instruction, and left the comment `(hope this doesn't break the game)`. As I was tired, it was late, and, well, what's the worst that could happen.

Next morning. Yes. That did break the game. Key doors would now open only one side of the door in dungeons. Pretty heavy bug, as you can waste keys and get locked out of areas that way.

# And for my next magic trick.

```asm
ld a, [bc]
or [hl]
ld [bc], a
```
This was the offending code. `bc` would point at the "room status" in WRAM in case you are in a dungeon, but it would point in ROM outside of dungeons. So, this simply becomes a call to:
```asm
ld a, b
and $E0
cp $C0
ld a, [bc]
ret nz
or [hl]
ld [bc], a
ret
```
First, we check if we are pointing at RAM or not, and if not, then we return from this function early. We had some free space in this bank, so all is well now.


In total, I have about 200 lines of python code that patches LADX. And the whole thing feels a big fragile.

Reactions on it however, where... [GREAT](https://clips.twitch.tv/NeighborlyMoldyDaikonPJSalt-cnVVx5sMrgDAXT9_)

## Hindsight 2020

In hindsight, I should have made the credits warp after you drop down the waterfall, that would have shown off FFA a tiny bit more. I also shouldn't have been trying to put this together in the last hour. It's kinda lucky that not more bugs happened.

What's next? Not sure yet. I'm still working on reverse engineering more of FFA. But not sure if it makes for a decent game for a randomizer, unless I make quite a few modifications to make that work.
