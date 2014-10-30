# -*- coding: utf-8 -*-

from cms import *
from cms.fs import *
from cms.http import *
from cms.controller import *
from mako.template import Template

from datetime import *
import hashlib


def indexController(results, request):
	try:
		index = open(join(FS.pagedir, 'index.html'))

		data = {
			'site': {
				'root': request.root,
				'lang': 'en'
			}
		}

		html = Template(
			index.read(),
			lookup=FS.lookup
		).render_unicode(**data)

		res = Response(
			status=Status.OK,
			headers={'Content-Type': ContentType.HTML + '; charset=utf-8'},
			content=html
		)

		return res
	except Exception as e:
		return str(e)


ControllerSet.register(
	Controller(
		'^(|/(index|home|main)?/?)$',
		indexController
	)
)
