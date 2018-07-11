from setuptools import setup, find_packages

setup(
    name = 'ganymede',
    version = '0.0.1',
    url = 'https://github.com/mmaz/ganymede.git',
    author = 'Mark Mazumder',
    author_email = 'mark@markmaz.com',
    description = 'Realtime grading server for in-class jupyter notebooks',
    packages = find_packages(),    
    install_requires = ['requests >= 2.10.0'],
)