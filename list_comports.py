"""
list_comports.py

List serial ports (windows 'COMx' ports).


(C) Felix Althaus

"""




import sys
import re
import serial.tools.list_ports




if __name__ == "__main__":

    ports = serial.tools.list_ports.comports()

    print()

    if not ports:
        print("No serial ports found.")
        sys.exit(0)


    print(" {:8s}{:32s}{:s}".format("Name", "Description", "Manufacturer"))

    print(" "+"-"*70)

    for port in ports:
        # remove anything within parentheses to keep things short
        description = re.sub(r"\(.*?\)", "", port.description)

        if port.manufacturer:
            manufacturer = re.sub(r"\(.*?\)", "", port.manufacturer)
        else:
            manufacturer = "n/a"

        print(" {:8s}{:32s}{:s}".format(port.name, description, manufacturer))
