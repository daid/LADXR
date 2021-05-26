local socketlib = require('socket.core')
local socket = nil
local poll_counter = 0
local connection_state = nil

-- Connector version
VERSION = 0x01

-- Memory locations of LADXR
ROMGameID = 0x0051 -- 4 bytes
ROMWorldID = 0x0055
ROMConnectorVersion = 0x0056
wGameplayType = 0xDB95 -- RO: We should only act if this is higher then 6, as it indicates that the game is running normally
wLinkSyncSequenceNumber = 0xDDF6 --RO: Starts at 0, increases every time an item is received from the server and processed
wLinkStatusBits = 0xDDF7 -- RW:
    -- Bit0: wLinkGive* contains valid data, set from script cleared from ROM.
    -- Bit1: wLinkSendItem* contains valid data, set from ROM cleared from lua
    -- Bit2: wLinkSendShop* contains valid data, set from ROM cleared from lua
wLinkGiveItem = 0xDDF8 --RW
wLinkGiveItemFrom = 0xDDF9 --RW
wLinkSendItemRoomHigh = 0xDDFA --RO
wLinkSendItemRoomLow = 0xDDFB --RO
wLinkSendItemTarget = 0xDDFC --RO
wLinkSendItemItem = 0xDDFD --RO
wLinkSendShopItem = 0xDDFE --RO, which item to send (1 based, order of the shop items)
wLinkSendShopTarget = 0xDDFF --RO, which player to send to, but it's just the X position of the NPC used, so 0x18 is player 0

POLL_SPEED = 60

if memory ~= nil and gui ~= nil then
    -- Running in bizhawk
    console.clear()
    if gameinfo.getromname() == "Null" then
        print("ROM must be loaded before executing script.\nExiting.")
        return
    end
    
    function memread(addr)
        return memory.readbyte(addr)
    end
    function memwrite(addr, data)
        memory.writebyte(addr, data)
    end
    function memwriteOR(addr, data)
        memwrite(addr, bit.bor(memread(addr), data))
    end
    function memwriteAND(addr, data)
        memwrite(addr, bit.band(memread(addr), data))
    end
    function drawtext(text)
        gui.drawText(0, 0, text, 0xFF000000)
    end
    function mainloop(f)
        event.unregisterbyname("LADXR")
        event.unregisterbyname("LADXR")
        event.onframeend(f, "LADXR")
    end
else
    --Assume we are the arduino connector

    local serial = nil

    -- Setup serial connection
    -- We do this differently under windows and unix-based systems because of a limiation in the lua-serial library:
    -- https://github.com/javalikescript/luaserial/blob/master/luaserial_linux.c#L224
    -- No support for setTimeout in Linux, which is necessary for the rest of the logic to function properly.
    local separatorFormat = package.config:sub(1,1)
    if separatorFormat == '/' then -- linux, mac os
        -- http://www.lua.org/manual/5.3/manual.html#pdf-package.config
        -- The first line is the directory separator string. Default is '\' for Windows and '/' for all other systems.
        --
        -- Time is in tenth of seconds
        -- Use dmesg to ensure the arduino is actually /dev/ttyUSB0.
        -- Accessing ttyUSB0 requires setting up permissions under linux (i.e. adding your user to the dialout group).
        os.execute("stty -F /dev/ttyUSB0 115200 raw min 0 time 1 -echo -echoe -echok -echoctl -echoke")
        serial = io.open("/dev/ttyUSB0", "w+")
    else -- windows
        local seriallib = require "serial"
        serial = io.open("\\\\.\\COM27", "w+")
        serial:setvbuf("no")
        seriallib.flush(serial)
        seriallib.setSerial(serial, 115200, 8, 1, 0)
        seriallib.setTimeout(serial, 100, 0)
    end


    print("Connecting to Arduino...")
    while true do
        serial:write("!")
        local res = serial:read(128)
        if res == "!" then break end
        socketlib.sleep(5) -- seconds
    end
    print("Waiting for gameboy connection...")
    while true do
        serial:write("?")
        local res = serial:read(128)
        if res == "K" then break end
    end

    function memread(addr)
        serial:write("R" .. string.char(bit.rshift(addr, 8), bit.band(addr, 0xFF)))
        local res = serial:read(128)
        if res == nil then res = serial:read(128) end
        res = tonumber(res, 16)
        if res > 256 then return memread(addr) end
        return res
    end
    function memwrite(addr, data)
        serial:write("W" .. string.char(bit.rshift(addr, 8), bit.band(addr, 0xFF), data))
        local res = serial:read(128)
        if res == nil then res = serial:read(128) end
        if res == "E" then return memwrite(addr, data) end
    end
    function memwriteOR(addr, data)
        serial:write("O" .. string.char(bit.rshift(addr, 8), bit.band(addr, 0xFF), data))
        local res = serial:read(128)
        if res == nil then res = serial:read(128) end
        if res == "E" then return memwrite(addr, data) end
    end
    function memwriteAND(addr, data)
        memwrite(addr, bit.band(memread(addr), data))
    end
    local lastdrawntext = nil
    function drawtext(text)
        if lastdrawntext ~= text and text ~= "" then
            lastdrawntext = text
            print(text)
        end
    end
    function mainloop(f)
        while true do
            f()
            socketlib.sleep(0.001)
        end
    end
    POLL_SPEED = 5
end
if bit == nil then
    -- no bit library, we need it for bizhawk compatibility, as lua5.1 cannot parse the file otherwise
    bit = load([[return {
        band=function(a, b) return a & b end,
        bor=function(a, b) return a | b end,
        rshift=function(a, b) return a >> b end,
        lshift=function(a, b) return a << b end,
    }]])()
end
print("Start")

function stateInitialize()
    local gameplayType = memread(wGameplayType)
    if gameplayType <= 6 then
        drawtext("Waiting for savegame")
        return
    end
    if gameplayType > 0x1A then
        print(string.format("Unknown gameplay type? %02x", gameplayType))
        return
    end
    local version = memread(ROMConnectorVersion)
    if version ~= VERSION then
        drawtext(string.format("Wrong ROM/Connector version: %02x != %02x", version, VERSION))
        return
    end

    drawtext("Connecting...")
    connection_state = stateTryToConnect
end

function stateTryToConnect()
    if socket == nil then
        print("Creating socket")
        socket = socketlib.tcp()
        socket:settimeout(5)
    end
    local ret, err = socket:connect("daid.eu", 32032)
    if ret ~= 1 then
        print("Connection failed: " .. err)
        connection_state = stateError
    else
        socket:settimeout(0)
        sendAll(string.char(0x21, VERSION, memread(ROMGameID), memread(ROMGameID + 1), memread(ROMGameID + 2), memread(ROMGameID + 3), memread(ROMWorldID)))
        print(string.format("Connected as game: %02x%02x%02x%02x:%02x", memread(ROMGameID), memread(ROMGameID + 1), memread(ROMGameID + 2), memread(ROMGameID + 3), memread(ROMWorldID)))
        connection_state = stateIdle
    end
end
connection_state = stateInitialize

function stateIdle()
    local gameplayType = memread(wGameplayType)
    if gameplayType <= 6 then
        return
    end

    poll_counter = poll_counter + 1
    if poll_counter == POLL_SPEED then
        poll_counter = 0

        if bit.band(memread(wLinkStatusBits), 0x01) == 0x00 then
            sendAll(string.char(0, memread(wLinkSyncSequenceNumber)))
        end
    end
    
    if bit.band(memread(wLinkStatusBits), 0x02) == 0x02 then
        local room_h = memread(wLinkSendItemRoomHigh)
        local room_l = memread(wLinkSendItemRoomLow)
        local target = memread(wLinkSendItemTarget)
        local item = memread(wLinkSendItemItem)
        sendAll(string.char(0x10, room_h, room_l, target, item))
        print(string.format("Sending item: %01x%02x:%02x to %d", room_h, room_l, item, target))
        --TODO: We should wait till we have a confirm from the server that the item is handled by the server
        memwriteAND(wLinkStatusBits, 0xFD)
    end
    if bit.band(memread(wLinkStatusBits), 0x04) == 0x04 then
        local target = (memread(wLinkSendShopTarget) - 0x18) / 0x10
        local item = memread(wLinkSendShopItem)

        -- Translate item from shop item to giving item
        if item == 1 then item = 0xF0 -- zolstorm
        elseif item == 2 then item = 0xF1 -- cucco
        elseif item == 3 then item = 0xF2 -- piece of power
        elseif item == 4 then item = 0x0A -- bomb
        elseif item == 5 then item = 0x1D -- 100 rupees
        elseif item == 6 then item = 0x10 -- medicine
        elseif item == 7 then item = 0xF3 -- health
        else item = 0x1B end
        
        sendAll(string.char(0x11, target, item))
        print(string.format("Sending shop: %02x to %d", item, target))
        --TODO: We should wait till we have a confirm from the server that the item is handled by the server
        memwriteAND(wLinkStatusBits, 0xFB)
    end
    
    while true do
        local result, err = socket:receive(1)
        if err ~= nil and err ~= "timeout" then
            print("socket error:" .. err)
            connection_state = stateError
            return
        end
        if result == nil then return end
        
        if result:byte(1, 1) == 0x01 then
            result, err = socket:receive(3)
            if err == nil then
                seq_nr, item_id, source = result:byte(1, 3)
                print(string.format("Got item: %02x from %d (%d)", item_id, source, seq_nr))

                if memread(wLinkSyncSequenceNumber) ~= seq_nr then
                    print("Wrong seq number for item, ignoring.")
                else
                    if bit.band(memread(wLinkStatusBits), 0x01) == 0x01 then
                        print("Got item while previous was not yet handled by the game!")
                    else
                        memwrite(wLinkGiveItem, item_id)
                        memwrite(wLinkGiveItemFrom, source)
                        memwrite(wLinkSyncSequenceNumber, memread(wLinkSyncSequenceNumber) + 1)
                        memwriteOR(wLinkStatusBits, 0x01)
                    end
                end
            else
                print(err)
            end
        elseif result:byte(1, 1) == 0x02 then
           result, err = socket:receive(2)
           if err == nil then
               item_id, source = result:byte(1, 2)

               print(string.format("Go shop item: %02x from %d", item_id, source))

               if bit.band(memread(wLinkStatusBits), 0x01) == 0x01 then
                   print("Cannot give shop item, as there is still an item waiting, dropping it. Sorry.")
               else
                   memwrite(wLinkGiveItem, item_id)
                   memwrite(wLinkGiveItemFrom, source)
                   memwriteOR(wLinkStatusBits, 0x01)
               end
           else
               print(err)
           end
        end
    end
end

function stateError()
    if socket ~= nil then
        socket:close()
        socket = nil
    end

    drawtext("Disconnected")
end

function sendAll(data)
    local len = string.len(data);
    local done = 0
    while done < len do
        local err = nil
        done, err = socket:send(data, done)
        if err ~= nil then
            print("Socket send error:" .. err)
            connection_state = stateError
            return
        end
    end
end

mainloop(function()
    drawtext("") -- This is needed in some versions of bizhawk to clear the message from the screen
    connection_state()
end)
