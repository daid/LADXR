local socketlib = require('socket.core')
local socket = nil
local poll_counter = 0
local connection_state = nil

console.clear()
print("Start")

-- Memory locations of LADXR
ROMGameID = 0x0051 -- 4 bytes
ROMWorldID = 0x0055
wGameplayType = 0xDB95 -- RO: We should only act if this is higher then 6, as it indicates that the game is running normally
wLinkSyncSequenceNumber = 0xDDF6 --RO: Starts at 0, increases every time an item is received from the server and processed
wLinkStatusBits = 0xDDF7 -- RW: Bit0: wLinkGive* contains valid data, set from script cleared from rom. Bit1: wLinkSendItem* contains valid data, set from ROM cleared from lua
wLinkGiveItem = 0xDDF8 --RW
wLinkGiveItemFrom = 0xDDF9 --RW
wLinkSendItemRoomHigh = 0xDDFA --RO
wLinkSendItemRoomLow = 0xDDFB --RO
wLinkSendItemTarget = 0xDDFC --RO
wLinkSendItemItem = 0xDDFD --RO

function stateInitialize()
    local gameplayType = memory.readbyte(wGameplayType)
    if gameplayType <= 6 then
        gui.drawText(0, 0, "Waiting for savegame", 0xFF000000)
        return
    end
    if gameplayType > 0x1A then
        print(string.format("Unknown gameplay type? %02x", gameplayType))
        return
    end

    gui.drawText(0, 0, "Connecting...", 0xFF000000)
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
        sendAll(string.char(0x20, memory.readbyte(ROMGameID), memory.readbyte(ROMGameID + 1), memory.readbyte(ROMGameID + 2), memory.readbyte(ROMGameID + 3), memory.readbyte(ROMWorldID)))
        print(string.format("Connected as game: %02x%02x%02x%02x:%02x", memory.readbyte(ROMGameID), memory.readbyte(ROMGameID + 1), memory.readbyte(ROMGameID + 2), memory.readbyte(ROMGameID + 3), memory.readbyte(ROMWorldID)))
        connection_state = stateIdle
    end
end
connection_state = stateInitialize

function stateIdle()
    poll_counter = poll_counter + 1
    if poll_counter == 60 then
        poll_counter = 0

        if bit.band(memory.readbyte(wLinkStatusBits), 0x01) == 0x00 then
            sendAll(string.char(0, memory.readbyte(wLinkSyncSequenceNumber)))
        end
    end
    
    if bit.band(memory.readbyte(wLinkStatusBits), 0x02) == 0x02 then
        local room_h = memory.readbyte(wLinkSendItemRoomHigh)
        local room_l = memory.readbyte(wLinkSendItemRoomLow)
        local target = memory.readbyte(wLinkSendItemTarget)
        local item = memory.readbyte(wLinkSendItemItem)
        sendAll(string.char(0x10, room_h, room_l, target, item))
        print(string.format("Sending item: %01x%02x:%02x to %d", room_h, room_l, item, target))
        --TODO: We should wait till we have a confirm from the server that the item is handled by the server
        memory.writebyte(wLinkStatusBits, bit.band(memory.readbyte(wLinkStatusBits), 0xFD))
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
            result, err = socket:receive(2)
            item_id, source = result:byte(1, 2)

            print(string.format("Go item: %02x from %d", item_id, source))

            memory.writebyte(wLinkGiveItem, item_id)
            memory.writebyte(wLinkGiveItemFrom, source)
            memory.writebyte(wLinkStatusBits, bit.bor(memory.readbyte(wLinkStatusBits), 0x01))
            memory.writebyte(wLinkSyncSequenceNumber, memory.readbyte(wLinkSyncSequenceNumber) + 1)
        end
    end
end

function stateError()
    if socket ~= nil then
        socket:close()
        socket = nil
    end

    gui.drawText(0, 0, "Disconnected", 0xFF000000)
end

event.unregisterbyname("LADXR")
event.unregisterbyname("LADXR")
event.onframeend(function()
    connection_state()
end, "LADXR")

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
