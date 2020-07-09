import struct
import asyncio
import binascii


class BGBClient:
    CMD_VERSION = 1
    CMD_JOYPAD = 101
    CMD_SYNC1 = 104
    CMD_SYNC2 = 105
    CMD_SYNC3 = 106
    CMD_STATUS = 108
    CMD_DISCONNECT = 109

    def __init__(self, server, reader, writer):
        self.__server = server
        self.__reader = reader
        self.__writer = writer
        self.__time = 0
        self.__running = False
        self.__reply = asyncio.get_running_loop().create_future()
        self.__rom_id = None
        self.__player_id = None
        self.__player_info = None

    async def __readPacket(self):
        packet = b''
        while True:
            data = await self.__reader.read(8 - len(packet))
            if data == b'':
                self.__writer.close()
                raise ValueError()
            packet += data
            if len(packet) == 8:
                return struct.unpack("<BBBBI", packet)

    async def lowlevel(self):
        await self.__send(self.CMD_VERSION, 1, 4, 0, 0)
        while True:
            try:
                b1, b2, b3, b4, t = await self.__readPacket()
            except ValueError:
                self.__reply.set_exception(ValueError())
                return
            # print(b1, b2, b3, b4, t)
            if b1 == self.CMD_VERSION:  # When we get the version need to reply with our status.
                await self.__send(self.CMD_STATUS, 5, 0, 0, 0)
                #self.server.clients.add(self)
            elif b1 == self.CMD_JOYPAD:
                pass  # ignore JOYPAD commands
            elif b1 == self.CMD_SYNC1:
                pass  # link master transmit command
            elif b1 == self.CMD_SYNC2:  # link slave reply
                self.__reply.set_result(b2)
            elif b1 == self.CMD_SYNC3 and b2 == 1:
                self.__reply.set_result(-1)
            elif b1 == self.CMD_SYNC3 and b2 == 0:
                # Time sync, need to reply to keep emulator running
                await self.__send(self.CMD_SYNC3, 0, 0, 0, t)
                self.__time = t
            elif b1 == self.CMD_STATUS:
                self.__running = (b2 & 0x03) == 0x01
            elif b1 == self.CMD_DISCONNECT:
                pass

    async def __send(self, b1, b2, b3, b4, t=None):
        if t is None:
            t = self.__time
        self.__writer.write(struct.pack("<BBBBI", b1, b2, b3, b4, t))
        await self.__writer.drain()

    async def send(self, byte):
        await asyncio.sleep(0.1)
        self.__reply = asyncio.get_running_loop().create_future()
        await self.__send(self.CMD_SYNC1, byte, 0x87, 0)
        reply = await self.__reply
        if reply == -1:
            print(">%02x ---" % (byte))
            return await self.send(byte)
        # print(">%02x <%02x" % (byte, reply))
        return reply

    async def highlevel(self):
        await self.send(0xFF)
        await self.send(0xFF)
        await self.send(0xFF)
        while True:
            status_bits = await self.send(0xEE)
            seq_nr = await self.send(0xFF)
            print(self, status_bits, seq_nr)

            if (status_bits & 0x80) != 0:
                self.__rom_id = None
                self.__player_id = None
                self.__player_info = None
            elif self.__rom_id is None:
                await self.send(0xE2)
                self.__rom_id = bytes([await self.send(0xFF) for _ in range(4)])
                self.__player_id = await self.send(0xFF)
                self.__player_info = self.__server.getPlayerInfo(self.__rom_id, self.__player_id)
                print("Player connected:", binascii.hexlify(self.__rom_id), self.__player_id)
            elif (status_bits & 0x01) == 0 and seq_nr < self.__player_info.getItemCount():
                print("Sending item:", hex(self.__player_info.getItem(seq_nr)))
                await self.send(0xE0)
                await self.send(self.__player_info.getItem(seq_nr))
            elif (status_bits & 0x02) == 2:
                await self.send(0xE1)
                room_high = await self.send(0xFF)
                room_low = await self.send(0xFF)
                room = room_low | (room_high << 8)
                target = await self.send(0xFF)
                item = await self.send(0xFF)

                print("Got item:", target, hex(room), hex(item))
                self.__server.getPlayerInfo(self.__rom_id, target).addItem(item, room)


class Server:
    def __init__(self):
        self.clients = set()
        self.games = {}

    async def handleClient(self, reader, writer):
        client = BGBClient(self, reader, writer)
        print("new client")
        await asyncio.gather(client.lowlevel(), client.highlevel(), return_exceptions=True)
        print("del client")

    async def run(self):
        server = await asyncio.start_server(self.handleClient, "localhost", 3333)
        async with server:
            await server.serve_forever()

    def getPlayerInfo(self, rom_id, player_id):
        game = self.__getGame(rom_id)
        if player_id not in game:
            game[player_id] = PlayerInfo()
        return game[player_id]

    def __getGame(self, rom_id):
        if rom_id not in self.games:
            self.games[rom_id] = {}
        return self.games[rom_id]


class PlayerInfo:
    def __init__(self):
        self.__items = []
        self.__done_rooms = set()

    def getItemCount(self):
        return len(self.__items)

    def getItem(self, index):
        return self.__items[index]

    def addItem(self, item, room):
        if room in self.__done_rooms:
            return
        self.__items.append(item)
        self.__done_rooms.add(room)


if __name__ == "__main__":
    server = Server()
    asyncio.run(server.run())
