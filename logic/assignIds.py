import os
import re

files = (
    "overworld.py",
    "dungeon1.py",
    "dungeon2.py",
    "dungeon3.py",
    "dungeon4.py",
    "dungeon5.py",
    "dungeon6.py",
    "dungeon7.py",
    "dungeon8.py",
    "dungeonColor.py",
)

fileDir = os.path.dirname(os.path.abspath(__file__))

def base36encode(number):
    number = abs(number)

    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    base36 = ""

    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36

    return base36 or alphabet[0]

def base36decode(number):
    return int(number, 36)

def readIds(filename):
    ids = set()

    path = os.path.join(fileDir, filename)
    
    with open(path, "r") as iFile:
        for line in iFile:
            matches = re.findall(r"id=\"([0-9a-z]+)\"", line)

            for id in matches:
                if id in ids:
                    raise Exception(f"Duplicate ID found", id)
                
                ids.add(id)
    
    return ids

def setEmptyIds(filename, highest):
    id = highest + 1

    path = os.path.join(fileDir, filename)
    lines = []
    with open(path, "r") as iFile:
        lines = iFile.readlines()

    idStr = "id=\"\""
    newIdStr = "id=\"{}\""
    with open(path, "w") as oFile:
        for line in lines:
            newLine = line
            while idStr in newLine:
                newLine = line.replace(idStr, newIdStr.format(base36encode(id)))
                id += 1
            
            oFile.write(newLine)
    
    return id

def insertMissingIds(filename, highest):
    id = highest + 1

    # This is wrong if .connect is not the last call on the line or if it spans multiple lines
    # Seems to work okay enough though
    pattern = re.compile(r"(\.connect\([^#]+)\)")

    path = os.path.join(fileDir, filename)
    lines = []
    with open(path, "r") as iFile:
        lines = iFile.readlines()

    with open(path, "w") as oFile:
        for line in lines:
            newLine = line
            
            if ", id=" not in newLine and re.search(pattern, newLine):
                newLine = re.sub(pattern, f"\\1, id=\"{base36encode(id)}\")", newLine)
                id += 1

            oFile.write(newLine)
    
    return id

def main():
    # This whole thing is bad. Use with extreme caution.
    # It got the job done, but could easily mangle different files horribly
    allIds = set()

    for file in files:
        ids = readIds(file)
        dupes = allIds.intersection(ids)

        if dupes:
            raise Exception('Duplicate ID(s) found', dupes)
        
        allIds = allIds.union(ids)
    
    highest = max([base36decode(x) for x in allIds]) if allIds else 0
    
    # for file in files:
    #     highest = setEmptyIds(file, highest)

    for file in files:
        highest = insertMissingIds(file, highest)
    
    pass

main()