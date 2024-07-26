#import os

class Test():
	"""docstring for Test"""

	def run(self):
		# get the current path.
		curpath = os.dirname(__file__)
		print(curpath)
