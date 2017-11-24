# pyregreader

pyregreader is a self deployable set of individual python programs, used to extract and send registry information from multiple client
computers to a single host computer. pyregreader will also write all data extracted from client registries, to a .csv file generated on a host computer.

# Individual programs:

Distributer.py - Program which distributes Client.py to multiple client computers on a network.
Client.py - Program that reads, extracts and sends local registry data of machine it is running on.
Receiver.py - Program which receives the extracted registry data from Client.py and writes extracted data to a .csv file.
setup.py - Program used to generate a .exe from an individual python program

# Dependencies:

CX_Freeze and openpyxl

