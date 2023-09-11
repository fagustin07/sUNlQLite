import os

from modules.SunQLite import SunQLite
import sys

if len(sys.argv) < 2:
    print('Por favor ejecutar con el nombre del archivo de la DB')
    sys.exit(1)


data_file = sys.argv[1]

if data_file[-3:] != '.db':
    print('Extension de archivo incorrecta')
    sys.exit(1)

if not os.path.isfile(data_file):
    with open(data_file, 'w'):
        pass

SunQLite(data_file).start()
