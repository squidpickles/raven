import xml.etree.ElementTree as ET

kEpochSeconds = 946684800  # Number of seconds between UNIX epoch (1970-01-01) and device epoch (2000-01-01)

kValueMap = {
    "InstantaneousDemand": "Demand",
    "CurrentSummationDelivered": "SummationDelivered",
}


class RavenMessage(dict):
    def __init__(self, name, **values):
        self.name = name
        dict.__init__(self, **values)

    def __str__(self):
        return self.name + ": " + dict.__str__(self)

    def value(self):
        return self.calculate_number(kValueMap[self.name])

    def calculate_number(self, tag):
        if tag in self and "Divisor" in self and "Multiplier" in self:
            return self[tag] * self["Multiplier"] / self["Divisor"]


class RavenMessageParser:
    @classmethod
    def parse(cls, message):
        root = ET.fromstring(message)
        msg = RavenMessage(root.tag)
        for child in root:
            text = child.text
            if text.startswith("0x"):
                text = int(text, 16)
                if text & 0x80000000:
                    text -= 0x100000000
            if child.tag == "TimeStamp":
                text += kEpochSeconds
            msg[child.tag] = text
        return msg


class RavenCommand(object):
    @classmethod
    def dump(cls, command):
        cmd = ET.Element("Command")
        name = ET.SubElement(cmd, "Name")
        name.text = command
        return ET.tostring(cmd)
