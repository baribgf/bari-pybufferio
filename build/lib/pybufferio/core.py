import shelve
from typing import NewType
from collections.abc import Iterable

class Buffer:
    """
    The base Buffer class
    """

    __FromType = NewType('_from', int)
    __ToType = NewType('_to', int)
    __states = {'PENDING': '[*]', 'from-start': '[+]', 'from-end': '[-]', 'WARNING': '[!]', 'ERROR': '[!!]'}
    directions = {'from-start': 1, 'from-end': -1}

    def __init__(self, buffer_path: str, verbose = True):
        """
        The main Buffer class constructor.

        Args:
            - `buffer_path` -> (`str`): The buffer file path.
            - `verbose` -> (`bool`): If `True`, logs will be reported.
        """

        self.__buffer_path = buffer_path
        self.__verbose = verbose

    def report(self, *args):
        if self.__verbose:
            print(*args)

    def __serial_index(self, index):
        """Serialize index with a serialized representation"""
        return hex(index).replace('0x', '')

    def dump(self, __objects_array: Iterable):
        """
        Dump (write) the objects array into buffer.
        
        Args:
            - `__objects_array` -> (`Iterable`): A 'supports-iteration' object which contains the objects to dump (write) into buffer.

        Returns:
            * This class instance (`Self`)
        """

        if not isinstance(__objects_array, Iterable):
            raise TypeError(f'__objects_array must be an iterable instance, got: {__objects_array}')
            
        from os import remove
        try:
            remove(self.__buffer_path + '.db')
            self.report(self.__states['WARNING'], f"File: '{self.__buffer_path}' replaced")
        except FileNotFoundError:
            pass

        with shelve.open(self.__buffer_path) as db:
            self.report(self.__states['PENDING'], f"Writing to: '{self.__buffer_path}'")
            index = 0
            for item in __objects_array:
                db[self.__serial_index(index)] = item
                index += 1

        self.report(self.__states['from-start'], f"File: {self.__buffer_path} written successfully")
        return self

    def load(self, interval: tuple[__FromType, __ToType] = None, direction: int = directions['from-start']):
        """
        Load the buffer items.

        Args:
            - `interval` -> (`tuple` [`__from`, `__to`]): The loading interval (`from` item index `to` another).
            - `direction` -> (`int`): The loading direction ( `1` for `from-start`, `-1` for `from-end` ).
        
        Returns:
            * A generator which yields all the buffered items.
        """

        if not direction in self.directions.values():
            raise ValueError(f'Invalid direction, got: {direction}\ndirection must be either 1 (Positive) -1 (Negative)')

        if not isinstance(interval, tuple):
            if interval is None and direction == self.directions['from-start']:
                interval = (0, -1)

            elif isinstance(interval, int):
                if direction == self.directions['from-start']:
                    interval = (0, interval)

                else:
                    interval = (interval, -1)
            else:
                raise ValueError(f'Invalid interval, got: {interval}')
        elif len(interval) != 2:
                raise ValueError(f'Invalid interval, got: {interval}')

        _from = interval[0]
        _to = interval[1]

        if not (0 <= _from <= _to) and _to != -1:
            raise ValueError(f"'_from', '_to' values are invalid, got {interval}")

        self.report(self.__states['PENDING'], f"Loading from: '{self.__buffer_path}' on: {interval}")
        try:
            with shelve.open(self.__buffer_path) as db:
                if _to == -1:
                    if direction == self.directions['from-start']:
                        index = _from
                    else:
                        index = len(db) - _from
                    item = db.get(self.__serial_index(index))
                    while item is not None:
                        yield item
                        item = db.get(self.__serial_index(index + 1))
                        index += 1
                else:
                    if direction == self.directions['from-start']:
                        f, t = _from, _to
                    else:
                        f, t = len(db) - _from, len(db) - _to

                    for i in range(f, t):
                        yield db.get(str(i))
                
            self.report(self.__states['from-start'], f"File: '{self.__buffer_path}' loaded successfully")
        except FileNotFoundError:
            self.report(self.__states['ERROR'], f"File: '{self.__buffer_path}' not found!")

    # Not really useful !!
    def __load_raw(self, interval: tuple[__FromType, __ToType] = None, direction: int = directions['from-start']):
        if not direction in self.directions.values():
            raise ValueError(f'Invalid direction, got: {direction}\ndirection must be either 1 (Positive) -1 (Negative)')

        if not isinstance(interval, tuple):
            if interval is None and direction == self.directions['from-start']:
                interval = (0, -1)

            elif isinstance(interval, int):
                if direction == self.directions['from-start']:
                    interval = (0, interval)

                else:
                    interval = (interval, -1)
            else:
                raise ValueError(f'Invalid interval, got: {interval}')
        elif len(interval) != 2:
                raise ValueError(f'Invalid interval, got: {interval}')

        _from = interval[0]
        _to = interval[1]

        if not (0 <= _from <= _to) and _to != -1:
            raise ValueError(f"'_from', '_to' values are invalid, got {interval}")

        self.report(self.__states['PENDING'], f"Loading from: '{self.__buffer_path}' on: {interval}")
        try:
            with open(self.__buffer_path + '.db', 'rb') as f:
                if direction == self.directions['from-start']:
                    f.seek(_from)
                else:
                    f.seek(0, 2)
                    for _ in range(_from):
                        f.seek(f.tell() - 1)

                if _to == -1:
                    while True:
                        char = f.read(1)
                        if char == '':
                            break
                        yield char

                else:
                    if direction == self.directions['from-start']:
                        while True:
                            if f.tell() == _to:
                                break

                            char = f.read(1)
                            yield char
                    else:
                        i = _from
                        while True:
                            if i == _to:
                                break
                            
                            char = f.read(1)
                            yield char
                            i += 1
                
            self.report(self.__states['from-start'], f"File: '{self.__buffer_path}' loaded successfully")
        except FileNotFoundError:
            self.report(self.__states['ERROR'], f"File: '{self.__buffer_path}' not found!")

    def head(self, n: int = 10):
        """
        Load first `n` buffered items.

        Args:
            * `n` -> (`int`): Number of first items to load.

        Returns:
            * A generator which yields first `n` buffered items.
        """

        return self.load((0, n), self.directions['from-start'])

    def tail(self, n: int = 10):
        """
        Load last `n` buffered items.

        Args:
            * `n` -> (`int`): Number of last items to load.

        Returns:
            * A generator which yields last `n` buffered items.
        """

        return self.load((n, -1), self.directions['from-end'])

"""
Todo:
    - Progress
"""
