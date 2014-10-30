# -*- coding: utf-8 -*-

from os.path import *
from mako.lookup import TemplateLookup


cwd = abspath(join(dirname(__file__), '..'))

# TO DO: Use config.json to fill these fields
class FS:
	cwd = cwd
	pubdir  = abspath(join(cwd, 'public'))
	tempdir = abspath(join(cwd, 'temp'))

	errdir  = abspath(join(cwd, 'public', 'error'))
	pagedir = abspath(join(cwd, 'public', 'page'))
	tmpldir = abspath(join(cwd, 'public', 'template'))
	sessdir = abspath(join(cwd, 'temp',   'session'))

	lookup = TemplateLookup(
		directories=[
			abspath(join(cwd, 'public'))
		]
	)
