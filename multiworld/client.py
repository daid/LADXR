import evilemu
import struct


class Gameboy:
    def __init__(self):
        print("Waiting for emulator.")
        emus = []
        while len(emus) == 0:
            emus = list(evilemu.find_gameboy_emulators())
        self.__emu = emus[0]

    def memread(self, addr: int) -> int:
        if 0x0000 < addr < 0x8000:
            return self.__emu.read_rom8(addr)
        if 0xC000 < addr < 0xE000:
            return self.__emu.read_ram8(addr - 0xC000)
        return 0

    def memwrite(self, addr: int, data: int) -> None:
        if 0x0000 < addr < 0x8000:
            self.__emu.write_rom8(addr, data)
        if 0xC000 < addr < 0xE000:
            self.__emu.write_ram8(addr - 0xC000, data)

    def memwriteOR(self, addr, data):
         self.memwrite(addr, self.memread(addr) | data)

    def memwriteAND(self, addr, data):
         self.memwrite(addr, self.memread(addr) & data)

def setstate(name):
    print(name)


if __name__ == "__main__":
    import socket
    sock = None
    poll_counter = 0
    connection_state = None

    gb = Gameboy()

    # Connector version
    VERSION = 0x01
    #
    # Memory locations of LADXR
    ROMGameID = 0x0051 # 4 bytes
    ROMWorldID = 0x0055
    ROMConnectorVersion = 0x0056
    wGameplayType = 0xDB95            # RO: We should only act if this is higher then 6, as it indicates that the game is running normally
    wLinkSyncSequenceNumber = 0xDDF6  # RO: Starts at 0, increases every time an item is received from the server and processed
    wLinkStatusBits = 0xDDF7          # RW:
    #      Bit0: wLinkGive* contains valid data, set from script cleared from ROM.
    #      Bit1: wLinkSendItem* contains valid data, set from ROM cleared from lua
    #      Bit2: wLinkSendShop* contains valid data, set from ROM cleared from lua
    wLinkGiveItem = 0xDDF8 # RW
    wLinkGiveItemFrom = 0xDDF9 # RW
    wLinkSendItemRoomHigh = 0xDDFA # RO
    wLinkSendItemRoomLow = 0xDDFB # RO
    wLinkSendItemTarget = 0xDDFC # RO
    wLinkSendItemItem = 0xDDFD # RO
    wLinkSendShopItem = 0xDDFE # RO, which item to send (1 based, order of the shop items)
    wLinkSendShopTarget = 0xDDFF # RO, which player to send to, but it's just the X position of the NPC used, so 0x18 is player 0

    POLL_SPEED = 60

    def sendAll(data):
        global connection_state
        done = 0
        while done < len(data):
            try:
                done += sock.send(data[done:])
            except socket.error as err:
                print("Socket send error:", err)
                connection_state = stateError
                return

    print("Start")

    def stateInitialize():
        global sock, connection_state

        gameplayType = gb.memread(wGameplayType)
        if gameplayType <= 6:
            setstate("Waiting for savegame")
            return
        if gameplayType > 0x1A:
            print(f"Unknown gameplay type? {gameplayType:02x}")
            return
        version = gb.memread(ROMConnectorVersion)
        if version != VERSION:
            setstate(f"Wrong ROM/Connector version: {version:02x} != {VERSION:02x}")
            return

        setstate("Connecting...")
        connection_state = stateTryToConnect

    def stateTryToConnect():
        global sock, connection_state
        if sock is None:
            print("Creating socket")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)

        try:
            sock.connect(("daid.eu", 32032))
        except socket.error as e:
            print("Connection failed: ", e)
            connection_state = stateError
        else:
            sock.settimeout(0)
            sendAll(bytes([0x21, VERSION, gb.memread(ROMGameID), gb.memread(ROMGameID + 1), gb.memread(ROMGameID + 2), gb.memread(ROMGameID + 3), gb.memread(ROMWorldID)]))
            print("Connected as game: %02x%02x%02x%02x:%02x" % (gb.memread(ROMGameID), gb.memread(ROMGameID + 1), gb.memread(ROMGameID + 2), gb.memread(ROMGameID + 3), gb.memread(ROMWorldID)))
            connection_state = stateIdle
    connection_state = stateInitialize

    def stateIdle():
        global poll_counter, connection_state
        gameplayType = gb.memread(wGameplayType)
        if gameplayType <= 6:
            return

        poll_counter = poll_counter + 1
        if poll_counter == POLL_SPEED:
            poll_counter = 0

            if (gb.memread(wLinkStatusBits) & 0x01) == 0x00:
                sendAll(bytes([0, gb.memread(wLinkSyncSequenceNumber)]))

        if (gb.memread(wLinkStatusBits) & 0x02) == 0x02:
            room_h = gb.memread(wLinkSendItemRoomHigh)
            room_l = gb.memread(wLinkSendItemRoomLow)
            target = gb.memread(wLinkSendItemTarget)
            item = gb.memread(wLinkSendItemItem)
            sendAll(bytes([0x10, room_h, room_l, target, item]))
            print("Sending item: %01x%02x:%02x to %d" % (room_h, room_l, item, target))
            # TODO: We should wait till we have a confirm from the server that the item is handled by the server
            gb.memwriteAND(wLinkStatusBits, 0xFD)

        if (gb.memread(wLinkStatusBits) & 0x04) == 0x04:
            target = (gb.memread(wLinkSendShopTarget) - 0x18) // 0x10
            item = gb.memread(wLinkSendShopItem)

            #  Translate item from shop item to giving item
            if item == 1:
                item = 0xF0 #  zolstorm
            elif item == 2:
                item = 0xF1 #  cucco
            elif item == 3:
                item = 0xF2 #  piece of power
            elif item == 4:
                item = 0x0A #  bomb
            elif item == 5:
                item = 0x1D #  100 rupees
            elif item == 6:
                item = 0x10 #  medicine
            elif item == 7:
                item = 0xF3 #  health
            else:
                item = 0x1B

            sendAll(bytes([0x11, target, item]))
            print("Sending shop: %02x to %d" & (item, target))
            # TODO: We should wait till we have a confirm from the server that the item is handled by the server
            gb.memwriteAND(wLinkStatusBits, 0xFB)

        while True:
            try:
                result = sock.recv(1)
            except socket.error as err:
                if err.winerror == 10035: # Non blocking
                    return
                connection_state = stateError
                return

            if result == b'': return

            if result[0] == 0x01:
                result = sock.recv(3)

                seq_nr, item_id, source = result
                print("Got item: %02x from %d (%d)" % (item_id, source, seq_nr))

                if gb.memread(wLinkSyncSequenceNumber) != seq_nr:
                    print("Wrong seq number for item, ignoring.")
                else:
                    if (gb.memread(wLinkStatusBits) & 0x01) == 0x01:
                        print("Got item while previous was not yet handled by the game!")
                    else:
                        gb.memwrite(wLinkGiveItem, item_id)
                        gb.memwrite(wLinkGiveItemFrom, source)
                        gb.memwrite(wLinkSyncSequenceNumber, gb.memread(wLinkSyncSequenceNumber) + 1)
                        gb.memwriteOR(wLinkStatusBits, 0x01)
            elif result[0] == 0x02:
               result = sock.recv(2)
               item_id, source = result

               print("Go shop item: %02x from %d" % (item_id, source))

               if (gb.memread(wLinkStatusBits) & 0x01) == 0x01:
                   print("Cannot give shop item, as there is still an item waiting, dropping it. Sorry.")
               else:
                   gb.memwrite(wLinkGiveItem, item_id)
                   gb.memwrite(wLinkGiveItemFrom, source)
                   gb.memwriteOR(wLinkStatusBits, 0x01)

    def stateError():
        global sock
        if sock is not None:
            sock.close()
            sock = None

        setstate("Disconnected")

    import time
    while True:
        connection_state()
        time.sleep(0.1)
