#This file is a track tagger for gPodder. It will correct the tags on poorly-
#tagged comment files.

#insert fancy header stuff here


import gpodder
import tagpy

class Tagger():
	"""This class accepts a path to a file and updates the tags for it based 
	on the attributes of the file (name of podcast, episode number, etc) and 
	also the user's config.
	"""

	def __init___(self, filename, config):
		self.tags = tagpy.FileRef(filename).tag
	
	def get_config():
		pass # ToDo: Implement reading the config object to extract details
		# Should this be mostly handled outside of this class?
