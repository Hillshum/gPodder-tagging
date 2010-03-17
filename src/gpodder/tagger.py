# gPodder - A media aggregator and podcast client
# Copyright (c) 2010 Hilton Shumway
#
# gPodder is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# gPodder is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#This file is a track tagger for gPodder. It will correct the tags on poorly-
#tagged comment files.




from gpodder.liblogger import log


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
            log('Cannot update tag of non-existing file')
            return False
        try: 
            fileref = tagpy.FileRef(filename.encode('utf-8'))
            tag = fileref.tag()
        except ValueError:
            log('Unable to read tag')
            return False

        self.artist = self.config.tag_artist
        self.album = self.config.tag_album
        self.genre = self.config.tag_genre
        self.title = self.config.tag_title
        tagvalues = {'channel.title': None,'episode.title':None,'artist':None}
        tagvalues['channel.title'] = episode.channel.title
        tagvalues['episode.title'] = episode.title
        #tagvalues['artist'] =  #Figure this out too


        tag.title = self.title % tagvalues
        tag.genre = self.genre % tagvalues
        tag.album = self.album % tagvalues
        #tag.artist = self.artist % tagvalues # Don't know what to use for this yet
        fileref.save()
        return True
