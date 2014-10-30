# -*- coding: utf-8 -*-

import re

# Global controller registry
class ControllerSet:
	controllers = []

	# Add a controller to the registry
	# @param Controller ctrl
	# @return bool
	def register(ctrl):
		if isinstance(ctrl, Controller):
			ControllerSet.controllers.append(ctrl)
			return True
		return False

	# Get the index of the first controller matching the path
	# @param string path
	# @return int/bool
	def find(path):
		for i, controller in enumerate(ControllerSet.controllers):
			regex = re.compile(controller.pattern)
			match = regex.match(path)

			if match is not None:
				return i

		return False

	# Execute the controller at the given index
	def execute(i, request):
		try:
			controller = ControllerSet.controllers[i]
			regex = re.compile(controller.pattern)
			results = regex.findall(request.path)

			result = controller.callback(results, request)

			return result
		except:
			return False


class Controller:
	def __init__(self, pattern, callback, before=None, after=None):
		self.pattern = pattern
		self.callback = callback

		if before is not None and hasattr(before, '__call__'):
			self.before = before
		else:
			self.before = None

		if after is not None and hasattr(after, '__call__'):
			self.after = after
		else:
			self.after = None
