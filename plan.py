

# Helper class to read and store planomizer data
class Plan:
    def __init__(self, filename):
        self.forced_items = {}

        for line in open(filename, "rt"):
            line = line.strip()
            if ";" in line:
                line = line[:line.find(";")]
            if "#" in line:
                line = line[:line.find("#")]
            if ":" not in line:
                continue
            entry_type, params = map(str.strip, line.upper().split(":", 1))

            if entry_type == "LOCATION" and ":" in params:
                location, item = map(str.strip, params.split(":", 1))
                if item == "":
                    continue
                self.forced_items[location] = item
