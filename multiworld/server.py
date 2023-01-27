import socketserver
import argparse
import sys
import binascii

VERSION = 0x01


class Connection(socketserver.StreamRequestHandler):
    def handle(self):
        print("Open", self)
        while True:
            data = self.rfile.read(1)
            if data == b'':
                break
            command = data[0]
            if command == 0x00:
                sync_nr = self.rfile.read(1)[0]

                player_info = self.server.getGame(self.game_id).getPlayer(self.player_id)
                if player_info.getItemCount() > sync_nr:
                    self.wfile.write(bytes([0x01, sync_nr, player_info.getItem(sync_nr), player_info.getItemSource(sync_nr)]))
                else:
                    shop_item = player_info.getShopItem()
                    if shop_item:
                        self.wfile.write(bytes([0x02, shop_item[0], shop_item[1]]))
                    else:
                        self.wfile.write(bytes([0x00]))
            elif command == 0x10:
                data = self.rfile.read(4)
                room_nr = (data[0] << 8) | data[1]
                target_player_id = data[2]
                item_id = data[3]

                self.server.getGame(self.game_id).gotItem(self.player_id, target_player_id, room_nr, item_id)
            elif command == 0x11:
                data = self.rfile.read(2)
                target_player_id = data[0]
                item_id = data[1]

                self.server.getGame(self.game_id).gotShopItem(self.player_id, target_player_id, item_id)
            elif command == 0x21:
                version = self.rfile.read(1)[0]
                self.game_id = self.rfile.read(4)
                self.player_id = self.rfile.read(1)[0]
                print("Player connected: %d (%s)" % (self.player_id, binascii.hexlify(self.game_id)))
                global VERSION
                if version != VERSION:
                    print("Player is using wrong version: %d != %d" % (version, VERSION))
                    break
            else:
                print("Unknown command from client: %02x" % (command))
                break
        print("Close", self)


class Game:
    def __init__(self, rom_id):
        self.__players = {}
        self.__rom_id = rom_id
        try:
            for line in open(binascii.hexlify(self.__rom_id).decode("ascii") + ".log", "rt"):
                source_player_id, target_player_id, room, item = map(int, line.strip().split(":"))
                if self.getPlayer(source_player_id).markRoomDone(room):
                    self.getPlayer(target_player_id).addItem(item, source_player_id)
        except FileNotFoundError:
            pass

    def getPlayer(self, player_id):
        if player_id not in self.__players:
            self.__players[player_id] = PlayerInfo(self)
        return self.__players[player_id]

    def gotItem(self, source_player_id, target_player_id, room, item):
        if self.getPlayer(source_player_id).markRoomDone(room):
            self.getPlayer(target_player_id).addItem(item, source_player_id)
            f = open(binascii.hexlify(self.__rom_id).decode("ascii") + ".log", "at")
            f.write("%d:%d:%d:%d\n" % (source_player_id, target_player_id, room, item))
            f.close()

    def gotShopItem(self, source_player_id, target_player_id, item):
        self.getPlayer(target_player_id).addShopItem(item, source_player_id)

class PlayerInfo:
    def __init__(self, game):
        self.__game = game
        self.__items = []
        self.__shop_items = []
        self.__done_rooms = set()

    def getItemCount(self):
        return len(self.__items)

    def getItem(self, index):
        return self.__items[index][0]
    
    def getShopItem(self):
        if self.__shop_items:
            return self.__shop_items.pop()
        return None

    def getItemSource(self, index):
        return self.__items[index][1]

    def addItem(self, item, source):
        self.__items.append((item, source))

    def addShopItem(self, item, source):
        self.__shop_items.append((item, source))

    def markRoomDone(self, room):
        if room in self.__done_rooms:
            return False
        self.__done_rooms.add(room)
        return True


class Server(socketserver.ThreadingTCPServer):
    block_on_close = False
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, port):
        super().__init__(("0.0.0.0", port), Connection)
        self.games = {}

    def getGame(self, game_id):
        if game_id not in self.games:
            self.games[game_id] = Game(game_id)
        return self.games[game_id]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Multiworld server')
    parser.add_argument('--port', type=int, default=3333)
    args = parser.parse_args()

    server = Server(args.port)
    server.serve_forever()
    sys.exit(0)
