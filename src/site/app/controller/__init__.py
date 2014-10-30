# -*- coding: utf-8 -*-

from os import listdir
from os.path import abspath, dirname, isfile, join


'''
cwd = abspath(join(dirname(__file__), '..'))

__all__ = [str(f)[:-3] for f in listdir(cwd) if isfile(join(cwd, f)) and f.endswith('.py')]
'''

__all__ = [
	'index',
	'lang',
	'blog',
	'static'
]
