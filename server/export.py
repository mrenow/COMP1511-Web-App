"""
Author: Ezra Hui

"""
# Overwrite export with the definition given in the program's entry point if applicable
# If testing, __main__ will not contain export. 
try:
	from __main__ import export # dodgy: importing from __main__
except(ImportError):
	# Export to do nothing for local testing
	def export(route, methods):     # dodgy: Different definitions depending on which file is __main__
		def decorator(function):
			return function
		return decorator
