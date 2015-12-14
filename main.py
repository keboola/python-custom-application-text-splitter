import textSplitter
import sys
import traceback

try:
	app = textSplitter.App()
	app.run()
except ValueError as err:
	print(err, file=sys.stderr)
	sys.exit(1)
except Exception as err:
	print(err, file=sys.stderr)
	traceback.print_exc(file=sys.stderr)
	sys.exit(2)
