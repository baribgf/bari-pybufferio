"""
# PyBufferIO v1.1
A python module which provides an efficient way to create buffers of objects.

Examples:
    - Import the base Buffer class

    >>> from pybuffer import Buffer

    - Dump (write) objects into buffer

    >>> buffer = Buffer('<buffer-path-to-dump-to>')
    >>> objects = [0, 'foo', (1, 2)]
    >>> buffer.dump(objects)

    - Load objects from buffer

    >>> buffer = Buffer('<buffer-path-to-load-from>')
    >>> for i in buffer.load():
    >>>     print(i, type(i))

This module is open source under the GNU licence.
- Developed by: Bari BGF
- Created on: Jan 29th, 2023
"""

from .core import Buffer
__version__ = '1.1'