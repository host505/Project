'''
    USTVcatchup Add-on

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

from resources.lib import Addon
import sys, re, os, urllib, urllib2
from urllib2 import urlopen
import json, base64
import requests
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

from datetime import date
from datetime import time
from datetime import datetime

addon = xbmcaddon.Addon()
addonid = addon.getAddonInfo('id')
addonname = addon.getAddonInfo('name')
plugin_path = xbmcaddon.Addon(id=addonid).getAddonInfo('path')

Addon.plugin_url = sys.argv[0]
Addon.plugin_handle = int(sys.argv[1])
Addon.plugin_queries = Addon.parse_query(sys.argv[2][1:])

dlg = xbmcgui.Dialog()

addon_logo = xbmc.translatePath(os.path.join(plugin_path,'icon.png'))

brand_logo = xbmc.translatePath(os.path.join(plugin_path,'icon.png'))

mode = Addon.plugin_queries['mode']

##Begin HGTV##
def hgtv_main():
    url = 'http://www.hgtv.com/shows/full-episodes/'
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    matches = Addon.find_multiple_matches(link,'<div class="m-MediaBlock o-Capsule__m-MediaBlock m-MediaBlock--playlist">(.*?)</h4>')
    for entry in matches:
        name = Addon.find_single_match(entry,'title="(.+?)"').replace("&amp;", "&").replace("&#39;", "'").strip()
        description = ""
        url = "http:" + Addon.find_single_match(entry,'<a href="(.+?)"')
        iconimage = "http:" + Addon.find_single_match(entry,'data-src="(.+?)"')
        if ".jpg" not in iconimage:
            iconimage = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'hgtv_main.png'))
        videos = Addon.find_single_match(entry,'<span class="m-MediaBlock__a-AssetInfo">(.+?) Videos</span>')
        if videos != "0":
            Addon.addDir(name,description,url,1,iconimage)

def hgtv_episodes(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    matches = Addon.find_multiple_matches(link,'"id" : "(.*?)},')
    
    for entry in matches:
        name = Addon.find_single_match(entry,'"title" : "(.+?)"').replace("&amp;", "&").replace("&#39;", "'").strip()
        description = Addon.find_single_match(entry,'"description" : "(.+?)"').replace("<p>", "").replace("<\/p>", "")
        url = Addon.find_single_match(entry,'"releaseUrl" : "(.+?)"')
        iconimage = "http://hgtv.com/" + Addon.find_single_match(entry,'"thumbnailUrl" : "(.+?)"')
        if ".jpg" not in iconimage:
            iconimage = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'hgtv_main.png'))
        if "http" in url:
            Addon.addLink(name,description,url,2,iconimage)

def hgtv_stream(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()

    url = Addon.find_single_match(link,'<video src="(.*?)"')
    
    Addon.play(url)
##End HGTV##

##Begin Travel Channel##
def travel_main():
    url = 'http://www.travelchannel.com/shows/video/full-episodes'
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    matches = Addon.find_multiple_matches(link,'<div class="m-MediaBlock o-Capsule__m-MediaBlock m-MediaBlock--playlist">(.*?)</h4>')

    for entry in matches:
        name = Addon.find_single_match(entry,'title="(.+?)"').replace("&amp;", "&")
        description=""
        url = "http:" + Addon.find_single_match(entry,'<a href="(.+?)"')
        iconimage = "http:" + Addon.find_single_match(entry,'data-src="(.+?)"').replace("http://cook.home.sndimg.com", "http://travel.home.sndimg.com")
        if ".jpg" not in iconimage:
            iconimage = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'travel_main.png'))
        videos = Addon.find_single_match(entry,'<span class="m-MediaBlock__a-AssetInfo">(.+?) Videos</span>')
        if videos != "0":
            Addon.addDir(name,description,url,3,iconimage)

def travel_episodes(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    matches = Addon.find_multiple_matches(link,'"id" : "(.*?)},')
    
    for entry in matches:
        name = Addon.find_single_match(entry,'"title" : "(.+?)"').replace("&amp;", "&").replace("&#39;", "'")
        description = Addon.find_single_match(entry,'"description" : "(.+?)"').replace("<p>", "").replace("<\/p>", "")
        url = Addon.find_single_match(entry,'"releaseUrl" : "(.+?)"')
        iconimage = "http://travelchannel.com/" + Addon.find_single_match(entry,'"thumbnailUrl" : "(.+?)"')
        if ".jpg" not in iconimage:
            iconimage = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'travel_main.png'))
        if "http" in url:
            Addon.addLink(name,description,url,4,iconimage)

def travel_stream(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()

    url = Addon.find_single_match(link,'<video src="(.*?)"')
    
    Addon.play(url)
##End Travel Channel##

##Begin DIY Network##
def diy_main():
    url = 'http://www.diynetwork.com/shows/full-episodes'
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()

    matches = Addon.find_multiple_matches(link,'<div class="m-MediaBlock o-Capsule__m-MediaBlock m-MediaBlock--playlist">(.*?)</h4>')
    
    for entry in matches:
        name = Addon.find_single_match(entry,'title="(.+?)"').replace("&amp;", "&").replace("&#39;", "'")
        description = ""
        url = "http:" + Addon.find_single_match(entry,'<a href="(.+?)"')
        iconimage = "http:" + Addon.find_single_match(entry,'data-src="(.+?)"')
        if ".jpg" not in iconimage:
            iconimage = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'diy_main.png'))
        videos = Addon.find_single_match(entry,'<span class="m-MediaBlock__a-AssetInfo">(.+?) Videos</span>')
        if videos != "0":
            Addon.addDir(name,description,url,5,iconimage)

def diy_episodes(url):
    if url == "null":
        url = "http://www.diynetwork.com/shows/full-episodes"
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    matches = Addon.find_multiple_matches(link,'"id" : "(.*?)},')
    
    for entry in matches:
        name = Addon.find_single_match(entry,'"title" : "(.+?)"').replace("&amp;", "&").replace("&#39;", "'")
        description = Addon.find_single_match(entry,'"description" : "(.+?)"').replace("<p>", "").replace("<\/p>", "")
        url = Addon.find_single_match(entry,'"releaseUrl" : "(.+?)"')
        iconimage = "http://diynetwork.com/" + Addon.find_single_match(entry,'"thumbnailUrl" : "(.+?)"')
        if ".jpg" not in iconimage:
            iconimage = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'diy_main.png'))
        if "http" in url:
            Addon.addLink(name,description,url,6,iconimage)

def diy_stream(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()

    url = Addon.find_single_match(link,'<video src="(.*?)"')
    
    Addon.play(url)
##End DIY Network##

##Begin Cooking Channel##
def cooking_main():
    url = 'http://www.cookingchanneltv.com/videos/players/full-episodes-player'
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()

    matches = Addon.find_multiple_matches(link,'<html >(.*?)</html>')
    
    for entry in matches:
        name = Addon.find_single_match(entry,'<span class="m-VideoPlayer__a-HeadlineText">(.+?)</span>').replace("&amp;", "&").replace("&#39;", "'")
        description = ""
        url = "null"
        iconimage = "http://cookingchanneltv.com/" + Addon.find_single_match(entry,'"thumbnailUrl" : "(.+?)"')
        if ".jpg" not in iconimage:
            iconimage = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'cooking_main.png'))
        if name is not "":
            Addon.addDir(name,description,url,7,iconimage)

    matches = Addon.find_multiple_matches(link,'data-module="editorial-promo">(.*?)</div>')

    for entry in matches:
        name = Addon.find_single_match(entry,'title="(.+?)"').replace("&amp;", "&").replace("&#39;", "'")
        description = ""
        url = "http:" + Addon.find_single_match(entry,'<a href="(.+?)"')
        iconimage = "http:" + Addon.find_single_match(entry,'data-src="(.+?)"')
        if ".jpg" not in iconimage:
            iconimage = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'cooking_main.png'))
        if name is not "":
            Addon.addDir(name,description,url,7,iconimage)

def cooking_episodes(url):
    if url == "null":
        url = "http://www.cookingchanneltv.com/videos/players/full-episodes-player"
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    matches = Addon.find_multiple_matches(link,'"id" : "(.*?)},')

    for entry in matches:
        name = Addon.find_single_match(entry,'"title" : "(.+?)"').replace("&amp;", "&").replace("&#39;", "'")
        description = Addon.find_single_match(entry,'"description" : "(.+?)"').replace("<p>", "").replace("<\/p>", "")
        url = Addon.find_single_match(entry,'"releaseUrl" : "(.+?)"')
        iconimage = "http://cookingchanneltv.com" + Addon.find_single_match(entry,'"thumbnailUrl" : "(.+?)"')
        if ".jpg" not in iconimage:
            iconimage = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'cooking_main.png'))
        if "http" in url:
            Addon.addLink(name,description,url,8,iconimage)

def cooking_stream(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()

    url = Addon.find_single_match(link,'<video src="(.*?)"')
    
    Addon.play(url)
##End Cooking Channel##

##Begin Food Network##
def food_main():
    url = 'http://www.foodnetwork.com/videos/full-episodes'
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()

    matches = Addon.find_multiple_matches(link,'<div class="m-MediaBlock o-Capsule__m-MediaBlock m-MediaBlock--playlist">(.*?)</div>')
    
    for entry in matches:
        name = Addon.find_single_match(entry,'title="(.+?)"').replace("&amp;", "&").replace("&#39;", "'")
        description = ""
        url = "http:" + Addon.find_single_match(entry,'<a href="(.+?)"')
        iconimage = "http:" + Addon.find_single_match(entry,'data-src="(.+?)"')
        if ".jpg" not in iconimage:
            iconimage = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'food_main.png'))
        Addon.addDir(name,description,url,9,iconimage)

def food_episodes(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    matches = Addon.find_multiple_matches(link,'"id" : "(.*?)},')
    
    for entry in matches:
        name = Addon.find_single_match(entry,'"title" : "(.+?)"').replace("&amp;", "&").replace("&#39;", "'")
        description = Addon.find_single_match(entry,'"description" : "(.+?)"').replace("<p>", "").replace("<\/p>", "")
        url = Addon.find_single_match(entry,'"releaseUrl" : "(.+?)"')
        iconimage = "http://foodnetwork.com/" + Addon.find_single_match(entry,'"thumbnailUrl" : "(.+?)"')
        if ".jpg" not in iconimage:
            iconimage = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'food_main.png'))
        if "http" in url:
            Addon.addLink(name,description,url,10,iconimage)

def food_stream(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()

    url = Addon.find_single_match(link,'<video src="(.*?)"')
    
    Addon.play(url)
##End Cooking Channel##

##Begin Smithsonian Channel##
def smith_main():
    url = 'http://www.smithsonianchannel.com/full-episodes'
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    matches = Addon.find_multiple_matches(link,'<li class="mix free" data-premium="false">(.*?)</li>')
    
    for entry in matches:
        name = Addon.find_single_match(entry,'<h3 class="promo-series-name">(.+?)</h3>').replace("&amp;", "&").replace("&#39;", "'")
        description = Addon.find_single_match(entry,'<h2 class="promo-show-name">(.+?)</h2>').replace("&amp;", "&").replace("&#39;", "'")
        url = "http://www.smithsonianchannel.com/" + Addon.find_single_match(entry,'<a href="(.+?)"')
        iconimage = "http:" + Addon.find_single_match(entry,'<source srcset="(.+?)"')
        if len(name) > 0 and "http" in url:
            Addon.addLink(name,description,url,11,iconimage)

def smith_stream(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()

    url = Addon.find_single_match(link,'<meta name="twitter:player:stream" content="(.*?)"')
    
    Addon.play(url)
##End Smithsonian Channel##

##Begin Freeform##
def freeform_main():
    url = 'http://freeform.go.com/shows'
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    matches = Addon.find_multiple_matches(link,'<div class="col-xs-4 shows-grid">(.*?)/p>')
    for entry in matches:
        name = Addon.find_single_match(entry,'<h3>(.+?)</h3>').replace("&amp;", "&").replace("&#39;", "'")
        description = Addon.find_single_match(entry,'<p>(.+?)<').replace("&amp;", "&").replace("&#39;", "'")
        url = "http://freeform.go.com" + Addon.find_single_match(entry,'<a href="(.+?)"')
        iconimage = Addon.find_single_match(entry,'<img src="(.+?)"')
        if "http" in url:
            Addon.addDir(name,description,url,16,iconimage)

def freeform_episodes(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    matches = Addon.find_multiple_matches(link,'<hr />(.*?)<p class="m-t-1">')

    episodelist = []
    for entry in matches:
        name = Addon.find_single_match(entry,'<h1 class="text-hover">(.+?)</h1>').replace("&amp;", "&").replace("&#39;", "'").strip()
        description = Addon.find_single_match(entry,'"ResultDescription":(.+?)"').replace("<p>", "").replace("<\/p>", "").strip().replace("&#39;", "'").replace("&quot;", '"')
        url = "http://freeform.go.com" + Addon.find_single_match(entry,'<a href="(.+?)"')
        iconimage = Addon.find_single_match(entry,'<img src="(.+?)"')
        lock = Addon.find_single_match(entry,'data-sign-in-padlock data-requires-sign-in="(.+?)"').strip()
        if "http" in url and lock == "False":
            episodelist.append(name)
        if len(episodelist) > 0:
            Addon.addLink(name,description,url,17,iconimage)
        else:
            dlg.ok(addonname, "No episodes found.")
            exit()

def freeform_movies(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    matches = Addon.find_multiple_matches(link,'<div class="movies-grid col-xs-6 col-md-4 col-lg-3">(.*?)</a>')

    for entry in matches:
        name = Addon.find_single_match(entry,'<h3 class="m-b-0">(.+?)</h3>').replace("&amp;", "&").replace("&#39;", "'").strip()
        description = Addon.find_single_match(entry,'<p>(.+?)</p>').replace("<p>", "").replace("<\/p>", "").strip().replace("&#39;", "'").replace("&quot;", '"')
        url = "http://freeform.go.com" + Addon.find_single_match(entry,'<a href="(.+?)"')
        iconimage = Addon.find_single_match(entry,'<img src="(.+?)"')
        lock = Addon.find_single_match(entry,'data-sign-in-padlock data-requires-sign-in="(.+?)"').strip()
        if "http" in url and lock == "False":
            Addon.addLink(name,description,url,17,iconimage)

def freeform_stream(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    vd = Addon.find_single_match(link,"VDKA(.+?)\"")
    url = 'https://api.entitlement.watchabc.go.com/vp2/ws-secure/entitlement/2020/authorize.json'
    udata = 'video%5Fid=VDKA'+str(vd)+'&device=001&video%5Ftype=lf&brand=002'
    uheaders = Addon.defaultHeaders.copy()
    uheaders['Content-Type'] = 'application/x-www-form-urlencoded'
    uheaders['Accept'] = 'application/json'
    uheaders['X-Requested-With'] = 'ShockwaveFlash/24.0.0.194'
    uheaders['Origin'] = 'http://cdn1.edgedatg.com'
    uheaders['DNT'] = '1'
    uheaders['Referer'] = 'http://cdn1.edgedatg.com/aws/apps/datg/web-player-unity/1.0.6.13/swf/player_vod.swf'
    uheaders['Pragma'] = 'no-cache'
    uheaders['Connection'] = 'keep-alive'
    uheaders['Cache-Control'] = 'no-cache'
    html = Addon.getRequest(url, udata, uheaders)
    a = json.loads(html)
    if a.get('uplynkData', None) is None:
        return

    sessionKey = a['uplynkData']['sessionKey']
    oid = Addon.find_single_match(html,'&oid=(.+?)&')
    eid = Addon.find_single_match(html,'&eid=(.+?)&')
    url = 'http://content.uplynk.com/ext/%s/%s.m3u8?%s' % (oid, eid, sessionKey)

    Addon.play(url)
##End freeform##

##Begin ABC##
def abc_main():
    url = 'http://abc.go.com/shows'
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    matches = Addon.find_multiple_matches(link,'<li  data-sm-id=""(.*?)/li>')
    for entry in matches:
        name = Addon.find_single_match(entry,'<div class="tile-show-name truncate">(.+?)</div>').replace("&amp;", "&").replace("&#39;", "'")
        description = ""
        path = Addon.find_single_match(entry,'<a href="(.+?)"').replace("/index", "")
        if name == "The Neighbors":
            url = "http://abc.go.com" + path + "/episode-guide/season-01"
        else:
            url = "http://abc.go.com" + path + "/episode-guide"
        iconimage = Addon.find_single_match(entry,'srcset="(.+?) ')
        if "http" in url and name != "":
            Addon.addDir(name,description,url,19,iconimage)

def abc_seasons(url, iconimage):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    matches = Addon.find_multiple_matches(link,'<option(.*?)option>')

    if matches == []:
        abc_episodes(url)
    else:
        seasonlist = []

        for entry in matches:
            name = Addon.find_single_match(entry,'>(.+?)</').replace("&amp;", "&").replace("&#39;", "'").strip()
            description = ""
            path = Addon.find_single_match(entry,'value="(.+?)"').replace("/index", "")
            url = "http://abc.go.com" + path
            if len(path) > 0:
                seasonlist.append(path)
            if len(seasonlist) > 0:
                Addon.addDir(name,description,url,20,iconimage)
            else:
                dlg.ok(addonname, "No episodes found.")
                exit()

def abc_episodes(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    matches = Addon.find_multiple_matches(link,'<div class="m-episode-copy medium-8 large-6 columns nogutter ">(.*?)</picture>')

    if len(matches) > 0:
        episodelist = []

        for entry in matches:
            season = Addon.find_single_match(entry,'<span class="season-number light">(.+?)</span>').replace("&amp;", "&").replace("&#39;", "'").strip()
            season = re.sub('<[^<]+?>', '', season).strip()
            episode = Addon.find_single_match(entry,'<span class="episode-number">(.+?)</a>').replace("&amp;", "&").replace("&#39;", "'").strip()
            episode = re.sub('<[^<]+?>', '', episode).strip()
            name = season + " " + episode
            description = Addon.find_single_match(entry,'<p>(.+?)</p>').replace("&amp;", "&").replace("&#39;", "'").strip()
            description = re.sub('<[^<]+?>', '', description).strip()
            path = Addon.find_single_match(entry,'<a class="dark-text" href="(.+?)">Watch</a>')
            url = "http://abc.go.com" + path
            iconimage = Addon.find_single_match(entry,'srcset="(.+?) ')
            if len(path) > 0:
                episodelist.append(path)
            if len(episodelist) > 0:
                Addon.addLink(name,description,url,21,iconimage)
            else:
                dlg.ok(addonname, "No episodes found.")
                exit()
    else:
        dlg.ok(addonname, "No episodes found.")
        exit()

def abc_stream(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    vd = Addon.find_single_match(link,"VDKA(.+?)\"")
    url = 'https://api.entitlement.watchabc.go.com/vp2/ws-secure/entitlement/2020/authorize.json'
    udata = 'video%5Fid=VDKA'+str(vd)+'&device=001&video%5Ftype=lf&brand=001'
    uheaders = Addon.defaultHeaders.copy()
    uheaders['Content-Type'] = 'application/x-www-form-urlencoded'
    uheaders['Accept'] = 'application/json'
    uheaders['X-Requested-With'] = 'ShockwaveFlash/22.0.0.209'
    uheaders['Origin'] = 'http://cdn1.edgedatg.com'
    html = Addon.getRequest(url, udata, uheaders)
    a = json.loads(html)
    if a.get('uplynkData', None) is None:
        return

    sessionKey = a['uplynkData']['sessionKey']
    if not '&cid=' in sessionKey:
        oid = Addon.find_single_match(html,'&oid=(.+?)&')
        eid = Addon.find_single_match(html,'&eid=(.+?)&')
        url = 'http://content.uplynk.com/ext/%s/%s.m3u8?%s' % (oid, eid, sessionKey)
    else:
        cid = Addon.find_single_match(html,'&cid=(.+?)&')
        url = 'http://content.uplynk.com/%s.m3u8?%s' % (cid, sessionKey)

    Addon.play(url)
##End ABC##

##Begin NBC##
def nbc_main():
    req = urllib2.Request('http://www.nbc.com/shows/all')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    html = Addon.find_single_match(link,'<script>PRELOAD=(.*?)</script>')
    a = json.loads(html)
    a = a['lists']['allShows']['items']
    for b in a:
        if b['tuneIn'] != 'WATCH VIDEOS' and b['tuneIn'] != 'COMING SOON' and b['tuneIn'] != 'LEARN MORE' and b['tuneIn'] != 'WATCH HIGHLIGHTS' and b['tuneIn'] != 'WATCH VIDEO' and 'SERIES PREMIERE' not in str(b['tuneIn']):
            name = b['title']
            description = ""
            url = 'http://www.nbc.com/' + b['urlAlias'] + '?nbc=1'
            iconimage = b['image']['path']
            if "Coming Soon" not in name:
                Addon.addDir(name,description,url,22,iconimage)

def nbc_episodes(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    id = re.compile(',"listKey"\:\"(.+?)"', re.DOTALL).search(link)
    if id is not None:
        id = id.group(1)
        id = id.rsplit('-', 1)[0]

        req = urllib2.Request('https://api.nbc.com/v3.14/videos?fields%5Bvideos%5D=title%2Cdescription%2Ctype%2Cgenre%2CvChipRating%2CvChipSubRatings%2Cguid%2Cpublished%2CrunTime%2Cairdate%2Cavailable%2CseasonNumber%2CepisodeNumber%2Cexpiration%2Centitlement%2CtveAuthWindow%2CnbcAuthWindow%2CexternalAdId%2CuplynkStatus%2CdayPart%2CinternalId%2Ckeywords%2Cpermalink%2CembedUrl%2Ccredits%2CselectedCountries%2Ccopyright&fields%5Bshows%5D=active%2Ccategory%2Ccolors%2CcreditTypeLabel%2Cdescription%2Cfrontends%2Cgenre%2CinternalId%2CisCoppaCompliant%2Cname%2Cnavigation%2Creference%2CschemaType%2CshortDescription%2CshortTitle%2CshowTag%2Csocial%2CsortTitle%2CtuneIn%2Ctype%2CurlAlias&fields%5Bimages%5D=derivatives%2Cpath%2Cwidth%2Cattributes%2CaltText%2Clink&fields%5BaggregatesShowProperties%5D=videoEpisodeSeasons%2CvideoTypes&include=image%2Cshow.image%2Cshow.aggregates&filter%5Bpublished%5D=1&filter%5BsalesItem%5D=0&filter%5Bshow%5D='+id+'&filter%5Btype%5D%5Bvalue%5D=Full%20Episode&filter%5Btype%5D%5Boperator%5D=%3D&sort=airdate&page%5Bnumber%5D=1&page%5Bsize%5D=50')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        html = response.read()
        response.close()

        a = json.loads(html)
        episodelist = []

        for b in sorted(a['data']):
            entitlement = b['attributes'].get('entitlement')
            url = b['attributes'].get('embedUrl')
            url = url.split('guid/',1)[1]
            url = url.split('?',1)[0]
            url = 'http://link.theplatform.com/s/NnzsPC/media/guid/%s?format=preview' % url
            html = Addon.getRequest(url)
            if html == '':
                continue
            c = json.loads(html)
            name = c['title']
            description = c.get('description')
            iconimage = c.get('defaultThumbnailUrl')
            url = 'http://link.theplatform.com/s/NnzsPC/media/'+c['mediaPid']+'?policy=43674&player=NBC.com%20Instance%20of%3A%20rational-player-production&formats=m3u,mpeg4&format=SMIL&embedded=true&tracking=true'

            if b['attributes'].get('type') == "Full Episode" and entitlement == "free":
                episodelist.append(name)
            if len(episodelist) > 0:
                Addon.addLink(str(name),description,url,23,iconimage)
            else:
                dlg.ok(addonname, "No episodes found.")
                exit()
    else:
        dlg.ok(addonname, "No episodes found.")
        exit()

def nbc_stream(url):
    if not '&format=redirect' in url:
        html = Addon.getRequest(url)
        if 'video src="' in html:
            url = Addon.find_single_match(html,'video src="(.+?)"')
        else:
            url = Addon.find_single_match(html,'ref src="(.+?)"')
        if 'nbcvodenc' in url:
            html = Addon.getRequest(url)
            url = Addon.find_single_match(html,'http(.+?)\n')
            url = 'http'+url.strip()
        elif not (url.endswith(".mp4") or url.endswith(".flv")):
            headers = Addon.defaultHeaders.copy()
            headers['User-Agent']= 'Mozilla/5.0 (Linux; U; en-US) AppleWebKit/528.5+ (KHTML, like Gecko, Safari/528.5+) Version/4.0 Kindle/3.0 (screen 600X800; rotate)'
            html = Addon.getRequest(url, headers=headers)
            urls = Addon.find_multiple_matches(html,'BANDWIDTH=(.+?),.+?\n(.+?)\n')
            blast = 0
            for b,u in urls:
                b = int(b)
                if blast < b:
                    url = u
                    blast = b
            url += '|User-Agent='+urllib.quote(headers['User-Agent'])
        if "Unavailable.mp4" in url:
            dlg.ok(addonname, "Stream unavailable.")
            exit()
        else:
            Addon.play(url)
##End NBC##

##Begin PBS##
def pbs_main():
    req = urllib2.Request('http://pbskids.org/video/')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    pg = response.read()
    response.close()
    a = re.compile('<dd class="category-list-button.+?data-slug="(.+?)">(.+?)<.+?src="(.+?)".+?</dd', re.DOTALL).findall(pg)
    for url, name, thumb in a:
        url = 'https://cms-tc.pbskids.org/pbskidsvideoplaylists/%s.json' % url

        name = name.replace("&amp;", "&").replace("&#039;", "'")
        description = name
        iconimage = thumb
        Addon.addDir(str(name),str(description),str(url),24,str(iconimage))

def pbs_episodes(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    a = json.loads(link)
    a = a['collections']['episodes']['content']
    if len(a) > 0:
        for b in a:
            url = b.get('mp4')
            if not url is None:
                name = b.get('title', 'no title')
                iconimage = b.get('images', {'x': None}).get('mezzanine', addon_logo)

                description = b.get('description')
                Addon.addLink(str(name),str(description),str(url),25,str(iconimage))
    else:
        dlg.ok(addonname, "No episodes found.")
        exit()

def pbs_stream(url):
      html = Addon.getRequest('%s?format=json' % url)
      a = json.loads(html)
      url = a.get('url')
      if url is not None:
            Addon.play(url)
##End PBS##

if mode == 'main':
    Addon.add_directory({'mode': 'abc_main'}, 'ABC', img = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'abc_main.png')))
    Addon.add_directory({'mode': 'cooking_main'}, 'Cooking Channel', img = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'cooking_main.png')))
    Addon.add_directory({'mode': 'diy_main'}, 'DIY Network', img = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'diy_main.png')))
    Addon.add_directory({'mode': 'food_main'}, 'Food Network', img = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'food_main.png')))
    Addon.add_directory({'mode': 'freeform_main'}, 'Freeform', img = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'freeform_main.png')))
    Addon.add_directory({'mode': 'hgtv_main'}, 'HGTV', img = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'hgtv_main.png')))
    Addon.add_directory({'mode': 'nbc_main'}, 'NBC', img = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'nbc_main.png')))
    Addon.add_directory({'mode': 'pbs_main'}, 'PBS Kids', img = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'pbs_main.png')))
    Addon.add_directory({'mode': 'smith_main'}, 'Smithsonian Channel', img = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'smith_main.png')))
    Addon.add_directory({'mode': 'travel_main'}, 'Travel Channel', img = xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'travel_main.png')))

    if len(Addon.get_setting('notify')) > 0:
        Addon.set_setting('notify', str(int(Addon.get_setting('notify')) + 1))  
    else:
        Addon.set_setting('notify', "1")        
    if int(Addon.get_setting('notify')) == 1:
        dlg.notification(addonname + ' is provided by:','Mr.Blamo',brand_logo,5000,False)
    elif int(Addon.get_setting('notify')) == 9:
        Addon.set_setting('notify', "0")

    #VPN Message
    if int(Addon.get_setting('vpn')) != 1:
        dlg.ok(addonname, "If you are outside the USA, you might want to consider subscribing to a VPN service in order to take full advantage of this addon.[/COLOR]")
        Addon.set_setting('vpn', "1") 

elif mode == 'refresh':
    xbmc.executebuiltin('Container.Refresh')

elif mode == 'hgtv_main':
    hgtv_main()

elif mode == 'travel_main':
    travel_main()

elif mode == 'diy_main':
    diy_main()

elif mode == 'cooking_main':
    cooking_main()

elif mode == 'food_main':
    food_main()

elif mode == 'smith_main':
    smith_main()

elif mode == 'freeform_main':
    freeform_main()

elif mode == 'abc_main':
    abc_main()

elif mode == 'nbc_main':
    nbc_main()

elif mode == 'pbs_main':
    pbs_main()

elif mode == 'settings':
    Addon.show_settings()
           
def get_params():
                param=[]
                paramstring=sys.argv[2]
                if len(paramstring)>=2:
                                params=sys.argv[2]
                                cleanedparams=params.replace('?','')
                                if (params[len(params)-1]=='/'):
                                    params=params[0:len(params)-2]
                                pairsofparams=cleanedparams.split('&')
                                param={}
                                for i in range(len(pairsofparams)):
                                    splitparams={}
                                    splitparams=pairsofparams[i].split('=')
                                    if (len(splitparams))==2:
                                        param[splitparams[0]]=splitparams[1]
                                                                
                return param
                                            
params=get_params()
url = None
name = None
mode = None
iconimage = None
description = None
group = None

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    iconimage = urllib.unquote_plus(params["iconimage"])
except:
    pass
try:        
    mode = int(params["mode"])
except:
    pass
try:        
    description = urllib.unquote_plus(params["description"])
except:
    pass
try:        
    group = urllib.unquote_plus(params["group"])
except:
    pass               

##This is for the HGTV stuff##
if mode == 1: hgtv_episodes(url)

##This is for the HGTV stuff##
elif mode == 2: hgtv_stream(url)

##This is for the Travel Channel stuff##
elif mode == 3: travel_episodes(url)

##This is for the Travel Channel stuff##
elif mode == 4: travel_stream(url)

##This is for the DIY Network stuff##
elif mode == 5: diy_episodes(url)

##This is for the DIY Network stuff##
elif mode == 6: diy_stream(url)

##This is for the Cooking Channel stuff##
elif mode == 7: cooking_episodes(url)

##This is for the Cooking Channel stuff##
elif mode == 8: cooking_stream(url)

##This is for the Food Network stuff##
elif mode == 9: food_episodes(url)

##This is for the Food Network stuff##
elif mode == 10: food_stream(url)

##This is for the Smithsonian Channel stuff##
elif mode == 11: smith_stream(url)

##This is for the Freeform stuff##
elif mode == 16: freeform_episodes(url)

##This is for the Freeform stuff##
elif mode == 17: freeform_stream(url)

##This is for the Freeform stuff##
elif mode == 18: freeform_movies(url)

##This is for the ABC stuff##
elif mode == 19: abc_seasons(url, iconimage)

##This is for the ABC stuff##
elif mode == 20: abc_episodes(url)

##This is for the ABC stuff##
elif mode == 21: abc_stream(url)

##This is for the NBC stuff##
elif mode == 22: nbc_episodes(url)

##This is for the NBC stuff##
elif mode == 23: nbc_stream(url)

##This is for the PBS stuff##
elif mode == 24: pbs_episodes(url)

##This is for the PBS stuff##
elif mode == 25: pbs_stream(url)
                
Addon.end_of_directory()
