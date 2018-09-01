'''
    TVcatchup Add-on

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

import urllib, pickle, cgi
import os, sys, re, string, random
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs

import urllib
import urllib2

reload(sys)  
sys.setdefaultencoding('utf8')

addon = xbmcaddon.Addon(id='script.module.catchuptv')
plugin_path = addon.getAddonInfo('path')
ICON = os.path.join(plugin_path, 'icon.png')
FANART = os.path.join(plugin_path, 'fanart.jpg')

def log(msg, err=False):
    if err:
        xbmc.log(addon.getAddonInfo('name') + ': ' + msg.encode('utf-8'), 
                 xbmc.LOGERROR)    
    else:
        xbmc.log(addon.getAddonInfo('name') + ': ' + msg.encode('utf-8'), 
                    xbmc.LOGDEBUG)    
          
def ascii(string):
    if isinstance(string, basestring):
        if isinstance(string, unicode):
           string = string.encode('ascii', 'ignore')
    return string
    
def getProperty(str):
    return xbmcgui.Window(10000).getProperty(str)

def setProperty(str1, str2):
    xbmcgui.Window(10000).setProperty(str1, str2)

def clearProperty(str):
    xbmcgui.Window(10000).clearProperty(str)

def cleanChannel(string):
    string = string.replace('AETV','A&E').replace('Discovery Channel','Discovery').replace('Fox News Channel','Fox News').replace('National Geographic Channel','National Geographic')
    return string.strip()

def show_dialog(details, title='USTVcatchup', is_error=False):
    error = ['', '', '']
    text = ''
    for k, v in enumerate(details):
        error[k] = v
        text += v + ' '
    log(text, is_error)
    dialog = xbmcgui.Dialog()
    ok = dialog.ok(title, error[0], error[1], error[2])
    
def get_setting(setting):
    return addon.getSetting(setting)
    
def set_setting(setting, string):
    return addon.setSetting(setting, string)
    
def get_string(string_id):
    return addon.getLocalizedString(string_id)   

def add_directory(url_queries, title, img=ICON, fanart=FANART, total_items=0):
    url = build_plugin_url(url_queries)
    log('adding dir: %s' % (title))
    listitem = xbmcgui.ListItem(decode(title), iconImage=img, thumbnailImage=img)
    if not fanart:
        fanart = addon.getAddonInfo('path') + '/fanart.jpg'
    listitem.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(plugin_handle, url, listitem, 
                                isFolder=True, totalItems=total_items)

def end_of_directory():
    xbmcplugin.endOfDirectory(plugin_handle, cacheToDisc=False)

def build_query(queries):
    return '&'.join([k+'='+urllib.quote(str(v)) for (k,v) in queries.items()])
                                
def build_plugin_url(queries):
    url = plugin_url + '?' + build_query(queries)
    return url

def parse_query(query, clean=True):
    queries = cgi.parse_qs(query)
    q = {}
    for key, value in queries.items():
        q[key] = value[0]
    if clean:
        q['mode'] = q.get('mode', 'main')
        q['play'] = q.get('play', '')

    return q

def get_input(title='', default=''):
    kb = xbmc.Keyboard(default, title, False)
    kb.doModal()
    if (kb.isConfirmed()):
        return kb.getText()
    else:
        return False

def show_settings():
    addon.openSettings()
    # workaround to return to main section. silent error is thrown
    exit()

#http://stackoverflow.com/questions/1208916/decoding-html-entities-with-python/1208931#1208931
def _callback(matches):
    id = matches.group(1)
    try:
        return unichr(int(id))
    except:
        return id

def decode(data):
    return re.sub("&#(\d+)(;|(?=\s))", _callback, data).strip()

def decode_dict(data):
    for k, v in data.items():
        if type(v) is str or type(v) is unicode:
            data[k] = decode(v)
    return data

def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def addLink(name,description,url,mode,iconimage):
    cm=[('Refresh', 'XBMC.RunPlugin(%s/?mode=refresh)' % (plugin_url))]
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
    liz.setProperty('fanart_image', addon.getAddonInfo('path') + '/fanart.jpg')
    liz.setProperty("IsPlayable","true")
    liz.addContextMenuItems(cm, 1)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

def addDir(name,description,url,mode,iconimage):
        cm=[('Refresh', 'XBMC.RunPlugin(%s/?mode=refresh)' % (plugin_url))]
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        liz.setProperty('fanart_image', addon.getAddonInfo('path') + '/fanart.jpg')
        liz.addContextMenuItems(cm, 1)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def cleanHex(text):
	def fixup(m):
		text = m.group(0)
		if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
		else: return unichr(int(text[2:-1])).encode('utf-8')
	try :return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
	except:return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))

def openURL(url):
	req      = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link     = response.read()
	link     = cleanHex(link)
	response.close()
	return link
		
def play(url):
	resolved = url
	item     = xbmcgui.ListItem(path=resolved)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)	

# Parse string and extracts multiple matches using regular expressions
def find_multiple_matches(text,pattern):
    
    matches = re.findall(pattern,text,re.DOTALL)

    return matches

# Parse string and extracts first match as a string
def find_single_match(text,pattern):
    result = ""
    try:    
        matches = re.findall(pattern,text, flags=re.DOTALL)
        result = matches[0]
    except:
        result = ""

    return result

USERAGENT   = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'

httpHeaders = {'User-Agent': USERAGENT,
                        'Accept':"application/json, text/javascript, text/html,*/*",
                        'Accept-Encoding':'gzip,deflate,sdch',
                        'Accept-Language':'en-US,en;q=0.8'
                       }

UTF8 = 'utf-8'

defaultHeaders = httpHeaders

def getRequest(url, udata=None, headers = httpHeaders, dopost = False, rmethod = None):
    req = urllib2.Request(url.encode(UTF8), udata, headers)  
    if dopost == True:
       rmethod = "POST"
    if rmethod is not None: req.get_method = lambda: rmethod
    try:
      response = urllib2.urlopen(req, timeout=60)
      page = response.read()
      if response.info().getheader('Content-Encoding') == 'gzip':
         page = zlib.decompress(page, zlib.MAX_WBITS + 16)
    except:
      page = ""
    return(page)
