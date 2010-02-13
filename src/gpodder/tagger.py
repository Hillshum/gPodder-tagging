#This file is a track tagger for gPodder. It will correct the tags on poorly-
#tagged comment files.

#insert fancy header stuff here


import gpodder
from gpodder import config
import tagpy

class Tagger(object):
	"""This class accepts a path to a file and updates the tags for it based 
	on the attributes of the file (name of podcast, episode number, etc) and 
	also the user's config.
	"""

	def __init___(self,config):
		self._config = config	
		

	def update_tag(self, episode):
		filename = episode.local_filename(create=False)
		if filename is None:
			raise Exception('cannot update tag of non-existing file')

		tag = tagpy.FileRef().tag()
		tag.title = title
		tag.genre = genre
		tag.album = album
		tag.artist = artist

	# Figure out how to get metadata from the episode objects, also figure out
	# a config schema
