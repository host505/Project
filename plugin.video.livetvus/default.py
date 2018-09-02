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

from resources.lib.modules.channels import *


def main():
    # VPN Message
    if int(get_setting('vpn_notify')) != 1:
        dlg.ok(addon_name, "If you are outside the USA, you might want to consider subscribing to a VPN service in order to take full advantage of this addon.")
        set_setting('vpn_notify', "1")

    add_dir("US TV", "", 1, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'ustv.png')))
    add_dir("UK TV", "", 2, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'uktv.png')))


def uktv():
    url = 'http://tvcatchup.com/'
    req = open_url(url)

    pattern = ""
    matches = find_multiple_matches(req, '<p class="channelsicon" style.+?>(.*?)</div>')

    for entry in matches:
        getchannel = find_single_match(entry, 'alt="Watch (.+?)"')
        gettitle = find_single_match(entry, '<br/> (.+?) </a>').replace("&#039;", "'")
        name = "{channel}-{title}".format(channel=getchannel, title=gettitle)
        url = "{url}{path}".format(url='http://tvcatchup.com', path=find_single_match(entry, '<a href="(.+?)"'))
        image = find_single_match(entry, 'src="https://www.tvcatchup.com/channel-images/(.+?)"')

        add_link(name, url, 3, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', image)))


def ustv():
    add_link("24/7 Retro", "", 4, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', '247Retro.png')))
    add_link("Aljazeera", "", 5, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'aljazeera-us.png')))
    add_link("Bloomberg", "", 6, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'bloomberg.png')))
    add_link("Buzzr", "", 7, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'buzzr.png')))
    add_link("CatholicTV Network", "", 8, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'catholic_tv.png')))
    add_link("CBS News", "", 9, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'cbsnews.png')))
    add_link("Charge!", "", 10, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'charge.png')))
    add_link("Cheddar", "", 11, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'cheddar.png')))
    add_link("Comet", "", 12, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'comet.png')))
    add_link("HSN", "", 13, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'hsn.png')))
    add_link("Light TV", "", 14, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'lighttv.png')))
    add_link("Newsmax TV", "", 15, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'newsmax.png')))
    add_link("QVC", "", 18, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'qvc-us.png')))
    add_link("RadioU TV", "", 19, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'radiou.png')))
    add_link("Rev'n TV", "", 20, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'revn.png')))
    add_link("RT News", "", 21, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'rt-us.png')))
    add_link("Sky News", "", 22, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'skynews-us.png')))
    add_link("Spirit TV", "", 23, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'spirittv.png')))
    add_link("Stadium", "", 24, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'stadium.png')))
    add_link("TBD TV", "", 25, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'tbd.png')))
    add_link("The Country Network", "", 26, xbmc.translatePath(os.path.join(plugin_path, 'resources', 'images', 'thecountrynetwork.png')))

def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


params = get_params()
url = None
name = None
mode = None

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass

if mode is None:
    main()

elif mode == 1:
    ustv()

elif mode == 2:
    uktv()

elif mode == 3:
    Channel().play_tvcatchup(url)

elif mode == 4:
    Channel().play_247retro()

elif mode == 5:
    Channel().play_aljazeera()

elif mode == 6:
    Channel().play_bloomberg()

elif mode == 7:
    Channel().play_buzzr()

elif mode == 8:
    Channel().play_catholic_tv()

elif mode == 9:
    Channel.play_cbs_news()

elif mode == 10:
    Channel().play_charge()

elif mode == 11:
    Channel().play_cheddar()

elif mode == 12:
    Channel().play_comet()

elif mode == 13:
    Channel().play_hsn()

elif mode == 14:
    Channel().play_light_tv()

elif mode == 15:
    Channel().play_newsmax_tv()

elif mode == 18:
    Channel().play_qvc()

elif mode == 19:
    Channel().play_campfire('radiou')

elif mode == 20:
    Channel().play_revn_tv()

elif mode == 21:
    Channel().play_rt()

elif mode == 22:
    Channel().play_sky_news()

elif mode == 23:
    Channel().play_campfire('spirit_tv')

elif mode == 24:
    Channel().play_stadium()

elif mode == 25:
    Channel().play_tbd()

elif mode == 26:
    Channel().play_the_country_network()

elif mode == 27:
    Channel().play_campfire("tuff_tv")

xbmcplugin.endOfDirectory(int(sys.argv[1]))
