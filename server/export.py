
# Overwrite export with the definition given in the program's entry point if applicable
try:
	from __main__ import export
except(ImportError):
    # Export to do nothing for local testing
    def export(route, methods):
        def decorator(function):	
            return function
        return decorator
