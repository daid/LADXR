import socket
import requests

response = requests.post("http://daid.eu:32032/game/register", json={
    "name": "TestGame",
    "game_name": "LADXR",
    "game_version": "1",
    "secret_hash": "",
    "public": True,
    "address": [],
    "port": "-1",
})

server_data = response.json()
print("KEY:", server_data["key"])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("daid.eu", 32032))
s.send(b"""GET /game/master HTTP/1.1
Host: daid.eu
Connection: upgrade
Upgrade: raw
Game-Key: %s
Game-Secret: %s

""" % (server_data["key"].encode("ascii"), server_data["secret"].encode("ascii")))
print(s.recv(1024))
