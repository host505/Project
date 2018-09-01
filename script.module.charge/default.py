'''
    Charge! Add-on

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
'''

import sys,re,os,urllib,urllib2
from urllib2 import urlopen
import xbmc,xbmcgui,xbmcplugin,xbmcaddon

dlg = xbmcgui.Dialog()
addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')
addon_id = addon.getAddonInfo('id')
plugin_path = xbmcaddon.Addon(id=addon_id).getAddonInfo('path')
addon_logo = xbmc.translatePath(os.path.join(plugin_path,'icon.png'))
stream_url = "https://watchcharge.com/watch-live/"
match_string = 'file: "(.+?)"'

def find_single_match(text,pattern):
    result = ""
    try:    
        matches = re.findall(pattern,text,flags=re.DOTALL)
        result = matches[0]
    except:
        result = ""
    return result

if __name__ == '__main__':
    req = urllib2.Request(stream_url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    stream = find_single_match(link,match_string)
    if stream is not "":
        xbmc.executebuiltin('Activatewindow(home)')
        li = xbmcgui.ListItem(addon_name)
        xbmc.Player().play(stream,li,False)
    else:
        dlg.ok(addon_name, "Unable to get stream. Please try again later.")
        xbmc.executebuiltin('Activatewindow(home)')
