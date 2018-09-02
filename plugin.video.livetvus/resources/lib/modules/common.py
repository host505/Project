"""
    Live TV Add-on
    Developed by Mr.Blamo

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import urllib
import urllib2
import re
import xbmcplugin
import xbmcgui
import os
import sys
import string
import xbmcaddon
import xbmc
import random

dlg = xbmcgui.Dialog()
addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')
addon_id = addon.getAddonInfo('id')
plugin_path = xbmcaddon.Addon(id=addon_id).getAddonInfo('path')

icon = xbmc.translatePath(os.path.join(plugin_path, 'icon.png'))
fanart = xbmc.translatePath(os.path.join(plugin_path, 'fanart.jpg'))

def play(url):
    resolved = url + '|User-Agent=TVCatchup/1.0.1 (samsung/SM-J7008; Android 4.4.2/KOT49H)'
    item = xbmcgui.ListItem(path=resolved)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


def play_youtube(id):
    url = 'plugin://plugin.video.youtube/play/?video_id=%s' % id
    item = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


def get_playable_url(id):
    url = 'plugin://plugin.video.youtube/play/?video_id=%s' % id
    return url


def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
    response = urllib2.urlopen(req)
    link = response.read()
    link = clean_hex(link)
    response.close()
    return link


def add_link(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&rand=" + random_generator()
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setProperty('fanart_image', fanart)
    liz.setProperty("IsPlayable", "true")
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok


def add_dir(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setProperty('fanart_image', fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def clean_hex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x":
            return unichr(int(text[3:-1], 16)).encode('utf-8')
        else:
            return unichr(int(text[2:-1])).encode('utf-8')

    try:
        return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
    except:
        return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))


# Parse string and extracts multiple matches using regular expressions
def find_multiple_matches(text, pattern):
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


# Parse string and extracts first match as a string
def find_single_match(text, pattern):
    result = ""
    try:
        matches = re.findall(pattern, text, flags=re.DOTALL)
        result = matches[0]
    except:
        result = ""

    return result


def get_setting(setting):
    return addon.getSetting(setting)


def set_setting(setting, string):
    return addon.setSetting(setting, string)


def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

