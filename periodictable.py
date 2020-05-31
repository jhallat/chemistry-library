import os
from collections import namedtuple

## TODO Probaly need to put this in a shared library
from enum import Enum


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]



Element = namedtuple('Element', ['atomic_number', 'symbol', 'name', 'atomic_mass'])
Ion = namedtuple('Ion', ['symbol', 'charge'])

class PeriodicTable(object, metaclass=Singleton):

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "data/periodic-table.dat")
        with open(path, "r") as data_file:
            data = data_file.read()
            elements = [Element(*tuple(line.split(','))) for line in data.split('\n')]
            self._table_symbol = {element.symbol:element for element in elements}
            self._table_number = { element.atomic_number : element for element in elements }


    def __len__(self):
        return len(self._table_symbol)


    def __getitem__(self, item):
        if str(item).isnumeric():
            return self._table_number[str(item)]
        else:
            return self._table_symbol[item]


class Ions(object, metaclass=Singleton):

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "data/common-ions.dat")
        with open(path, "r") as data_file:
            data = data_file.read()
            ions = []
            for line in data.split('\n'):
                data_line = line.split(',')
                ions.append(Ion(data_line[0], int(data_line[1])))
            self._ions = {ion.symbol: ion for ion in ions}

    def __len__(self):
        return len(self._ions)

    def __getitem__(self, item):
        return self._ions[item]
