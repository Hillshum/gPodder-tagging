# -*- coding: utf-8 -*-
#
# gPodder - A media aggregator and podcast client
# Copyright (c) 2005-2010 Thomas Perl and the gPodder Team
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

import gtk

import gpodder

_ = gpodder.gettext
N_ = gpodder.ngettext

from gpodder import util

from gpodder.gtkui.interface.common import BuilderWidget
from gpodder.gtkui.interface.common import Orientation
from gpodder.gtkui.frmntl.portrait import FremantleRotation

import hildon

class gPodderPreferences(BuilderWidget):
    UPDATE_INTERVALS = (
            (0, _('Manually')),
            (20, N_('Every %d minute', 'Every %d minutes', 20) % 20),
            (60, _('Hourly')),
            (60*6, N_('Every %d hour', 'Every %d hours', 6) % 6),
            (60*24, _('Daily')),
    )

    DOWNLOAD_METHODS = (
            ('quiet', _('Do nothing')),
            ('never', _('Show episode list')),
            ('queue', _('Add to download list')),
#            ('wifi', _('Download when on Wi-Fi')),
            ('always', _('Download immediately')),
    )

    AUDIO_PLAYERS = (
            ('default', _('Media Player')),
            ('panucci', _('Panucci')),
    )

    VIDEO_PLAYERS = (
            ('default', _('Media Player')),
            ('mplayer', _('MPlayer')),
    )

    def new(self):
        # Store the current configuration options in case we cancel later
        self._config_backup = self._config.get_backup()
        self._do_restore_config = True
        self.main_window.connect('destroy', self.on_destroy)

        self.save_button = self.main_window.add_button(gtk.STOCK_SAVE, 1)
        self.save_button.connect('clicked', self.on_save_button_clicked)

        self.touch_selector_orientation = hildon.TouchSelector(text=True)
        for caption in FremantleRotation.MODE_CAPTIONS:
            self.touch_selector_orientation.append_text(caption)
        self.touch_selector_orientation.set_active(0, self._config.rotation_mode)
        self.picker_orientation.set_selector(self.touch_selector_orientation)

        if not self._config.auto_update_feeds:
            self._config.auto_update_frequency = 0

        # Create a mapping from minute values to touch selector indices
        minute_index_mapping = dict((b, a) for a, b in enumerate(x[0] for x in self.UPDATE_INTERVALS))

        self.touch_selector_interval = hildon.TouchSelector(text=True)
        for value, caption in self.UPDATE_INTERVALS:
            self.touch_selector_interval.append_text(caption)
        interval = self._config.auto_update_frequency
        if interval in minute_index_mapping:
            self._custom_interval = 0
            self.touch_selector_interval.set_active(0, minute_index_mapping[interval])
        else:
            self._custom_interval = self._config.auto_update_frequency
            self.touch_selector_interval.append_text(N_('Every %d minute', 'Every %d minutes', interval) % interval)
            self.touch_selector_interval.set_active(0, len(self.UPDATE_INTERVALS))
        self.picker_interval.set_selector(self.touch_selector_interval)

        # Create a mapping from download methods to touch selector indices
        download_method_mapping = dict((b, a) for a, b in enumerate(x[0] for x in self.DOWNLOAD_METHODS))

        self.touch_selector_download = hildon.TouchSelector(text=True)
        for value, caption in self.DOWNLOAD_METHODS:
            self.touch_selector_download.append_text(caption)

        if self._config.auto_download not in (x[0] for x in self.DOWNLOAD_METHODS):
            self._config.auto_download = self.DOWNLOAD_METHODS[0][0]

        self.touch_selector_download.set_active(0, download_method_mapping[self._config.auto_download])
        self.picker_download.set_selector(self.touch_selector_download)

        # Determine possible audio and video players (only installed ones)
        self.audio_players = [(c, l) for c, l in self.AUDIO_PLAYERS if c == 'default' or util.find_command(c)]
        self.video_players = [(c, l) for c, l in self.VIDEO_PLAYERS if c == 'default' or util.find_command(c)]

        # Create a mapping from audio players to touch selector indices
        audio_player_mapping = dict((b, a) for a, b in enumerate(x[0] for x in self.audio_players))

        self.touch_selector_audio_player = hildon.TouchSelector(text=True)
        for value, caption in self.audio_players:
            self.touch_selector_audio_player.append_text(caption)

        if self._config.player not in (x[0] for x in self.audio_players):
            self._config.player = self.audio_players[0][0]

        self.touch_selector_audio_player.set_active(0, audio_player_mapping[self._config.player])
        self.picker_audio_player.set_selector(self.touch_selector_audio_player)

        # Create a mapping from video players to touch selector indices
        video_player_mapping = dict((b, a) for a, b in enumerate(x[0] for x in self.video_players))

        self.touch_selector_video_player = hildon.TouchSelector(text=True)
        for value, caption in self.video_players:
            self.touch_selector_video_player.append_text(caption)

        if self._config.videoplayer not in (x[0] for x in self.video_players):
            self._config.videoplayer = self.video_players[0][0]

        self.touch_selector_video_player.set_active(0, video_player_mapping[self._config.videoplayer])
        self.picker_video_player.set_selector(self.touch_selector_video_player)

        self.update_button_mygpo()

        # Fix the styling and layout of the picker buttons
        for button in (self.picker_orientation, \
                       self.picker_interval, \
                       self.picker_download, \
                       self.picker_audio_player, \
                       self.picker_video_player, \
                       self.button_mygpo):
            # Work around Maemo bug #4718
            button.set_name('HildonButton-finger')
            # Fix alignment problems (Maemo bug #6205)
            button.set_alignment(.0, .5, 1., 0.)
            child = button.get_child()
            child.set_padding(0, 0, 12, 0)

        self.check_view_all_episodes = hildon.CheckButton(gtk.HILDON_SIZE_FINGER_HEIGHT)
        self.check_view_all_episodes.set_label(_('Show "All episodes" view'))
        self.check_view_all_episodes.set_active(self._config.podcast_list_view_all)
        self.pannable_vbox.add(self.check_view_all_episodes)
        self.pannable_vbox.reorder_child(self.check_view_all_episodes, 2)

        self.gPodderPreferences.show_all()

    def on_picker_orientation_value_changed(self, *args):
        self._config.rotation_mode = self.touch_selector_orientation.get_active(0)

    def on_picker_interval_value_changed(self, *args):
        active_index = self.touch_selector_interval.get_active(0)
        if active_index < len(self.UPDATE_INTERVALS):
            new_frequency = self.UPDATE_INTERVALS[active_index][0]
        else:
            new_frequency = self._custom_interval

        if new_frequency == 0:
            self._config.auto_update_feeds = False
        self._config.auto_update_frequency = new_frequency
        if new_frequency > 0:
            self._config.auto_update_feeds = True

    def on_picker_download_value_changed(self, *args):
        active_index = self.touch_selector_download.get_active(0)
        new_value = self.DOWNLOAD_METHODS[active_index][0]
        self._config.auto_download = new_value

    def on_picker_audio_player_value_changed(self, *args):
        active_index = self.touch_selector_audio_player.get_active(0)
        new_value = self.audio_players[active_index][0]
        self._config.player = new_value

    def on_picker_video_player_value_changed(self, *args):
        active_index = self.touch_selector_video_player.get_active(0)
        new_value = self.video_players[active_index][0]
        self._config.videoplayer = new_value

    def update_button_mygpo(self):
        if self._config.mygpo_username:
            self.button_mygpo.set_value(self._config.mygpo_username)
        else:
            self.button_mygpo.set_value(_('Not logged in'))

    def on_button_mygpo_clicked(self, button):
        self.mygpo_login()
        self.update_button_mygpo()

    def on_destroy(self, window):
        if self._do_restore_config:
            self._config.restore_backup(self._config_backup)
        else:
            self._config.podcast_list_view_all = self.check_view_all_episodes.get_active()

        self.callback_finished()

    def on_save_button_clicked(self, button):
        self._do_restore_config = False
        self.main_window.destroy()

