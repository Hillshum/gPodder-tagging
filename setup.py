#!/usr/bin/env python

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

import glob
import os
import re
import sys
from distutils.core import setup

# build targets
(DEFAULT, MAEMO) = range(2)

# import the gpodder module locally for module metadata
sys.path.insert(0, 'src')
import gpodder

# if we are running "setup.py sdist", include all targets (see below)
building_source = ('sdist' in sys.argv)

# build target
if 'TARGET' in os.environ:
    if os.environ['TARGET'].strip().lower() == 'maemo':
        target = MAEMO
else:
    target = DEFAULT

# search for translations, taking $LINGUAS into account
translation_files = []
linguas = os.environ.get('LINGUAS', None)
if linguas is not None:
    linguas = linguas.split()

for mofile in glob.glob('data/locale/*/LC_MESSAGES/gpodder.mo'):
    _, _, lang, _ = mofile.split('/', 3)

    # Only install if either $LINGUAS it not set or the
    # language is specified in the $LINGUAS variable
    if linguas is None or lang in linguas:
        modir = os.path.dirname(mofile).replace('data', 'share')
        translation_files.append((modir, [mofile]))

if not len(translation_files) and \
        'clean' not in sys.argv and \
        linguas not in (None, []):
    print >>sys.stderr, """
    Warning: No translation files. (Did you forget to run "make messages"?)
    """

# files to install
inst_manpages = glob.glob( 'doc/man/*.1')
inst_share_ui = glob.glob('data/ui/*.ui')
inst_share_ui_desktop = glob.glob('data/ui/desktop/*.ui')
inst_share_ui_maemo = glob.glob('data/ui/maemo/*.ui')
inst_share_ui_frmntl = glob.glob('data/ui/frmntl/*.ui')
inst_share_gpodder = [ 'data/credits.txt' ] + glob.glob('data/images/*.png')
inst_desktop = [ 'data/gpodder.desktop' ]
inst_desktop_maemo = [ 'data/maemo/gpodder.desktop' ]
inst_share_dbus_services = ['data/org.gpodder.service']

inst_icons    = [ 'data/gpodder.png' ]
inst_icons_64 = [ 'data/icons/64/gpodder.png' ]
inst_icons_40 = [ 'data/icons/40/gpodder.png' ]
inst_icons_26 = [ 'data/icons/26/gpodder.png' ]
inst_icons_24 = [ 'data/icons/24/gpodder.png' ]
inst_icons_22 = [ 'data/icons/22/gpodder.png' ]
inst_icons_16 = [ 'data/icons/16/gpodder.png' ]
inst_icons_svg = [ 'data/gpodder.svg' ]

data_files = [
  ('share/man/man1',       inst_manpages),
  ('share/gpodder/ui',     inst_share_ui),
  ('share/pixmaps',        inst_icons),
  ('share/gpodder',        inst_share_gpodder),
  ('share/dbus-1/services',inst_share_dbus_services),
]

packages = [
  'gpodder',
  'gpodder.gtkui',
  'gpodder.gtkui.interface',
]

# target-specific installation data files
if target == DEFAULT or building_source:
    data_files += [
      ('share/gpodder/ui/desktop', inst_share_ui_desktop),
      ('share/applications', inst_desktop),
      ('share/icons/hicolor/scalable/apps', inst_icons_svg),
      ('share/icons/hicolor/48x48/apps', inst_icons),
      ('share/icons/hicolor/24x24/apps', inst_icons_24),
      ('share/icons/hicolor/22x22/apps', inst_icons_22),
      ('share/icons/hicolor/16x16/apps', inst_icons_16),
    ]
    packages += [
      'gpodder.gtkui.desktop',
    ]
    additional_scripts = []

if target == MAEMO or building_source:
    data_files += [
      ('share/gpodder/ui/maemo', inst_share_ui_maemo),
      ('share/gpodder/ui/frmntl', inst_share_ui_frmntl),
      ('share/applications/hildon', inst_desktop_maemo),
      ('share/icons/hicolor/scalable/apps', inst_icons_64),
      ('share/icons/hicolor/40x40/apps', inst_icons_40),
      ('share/icons/hicolor/26x26/apps', inst_icons_26),
    ]
    packages += [
      'gpodder.gtkui.maemo',
      'gpodder.gtkui.frmntl',
    ]
    additional_scripts = [
      'data/maemo/gpodder-mplayer',
    ]

author, email = re.match(r'^(.*) <(.*)>$', gpodder.__author__).groups()

setup(
  name         = 'gpodder',
  version      = gpodder.__version__,
  package_dir  = { '':'src' },
  packages     = packages,
  description  = 'media aggregator',
  author       = author,
  author_email = email,
  url          = gpodder.__url__,
  scripts      = glob.glob('bin/*') + additional_scripts,
  data_files   = data_files + translation_files
)

