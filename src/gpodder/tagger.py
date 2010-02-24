#This file is a track tagger for gPodder. It will correct the tags on poorly-
#tagged comment files.

#insert fancy header stuff here


from gpodder import config


import tagpy

class Tagger(object):
	"""This class accepts a path to a file and updates the tags for it based 
	on the attributes of the file (name of podcast, episode number, etc) and 
	also the user's config.
	"""

	def __init___(self,config):
		self.config = config	

	def update_tag(self, episode):
		filename = episode.local_filename(create=False)
		if filename is None:
			raise Exception('Cannot update tag of non-existing file')

		self.artist = self.config.tag_artist
		self.album = self.config.tag_album
		self.genre = self.config.tag_genre
		self.title = self.config.tag_title
		tagvalues = {'channel.title': None,'episode.title':None,'artist':None}
		tagvalues['channel.title'] = episode.channel.title
		tagvalues['episode.title'] = episode.title
		#tagvalues['artist'] =  #Figure this out too


		tag = tagpy.FileRef(filename).tag()
		tag.title = self.title % tagvalues
		tag.genre = self.genre % tagvalues
		tag.album = self.album % tagvalues
		#tag.artist = self.artist % tagvalues # Don't know what to use for this yet
