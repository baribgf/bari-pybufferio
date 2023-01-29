from setuptools import setup, find_packages

VERSION = '1.1'
DESCRIPTION = 'PyBufferIO'
LONG_DESCRIPTION = 'A python module which provides an efficient way to create buffers of objects.'

setup(
    name = "pybufferio", 
    version = VERSION,
    author = "Bari Bgf",
    author_email = "baribgf.2023@gmail.com",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = [],
    keywords =['python', 'pybuffer', 'buffers', 'pickle'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)