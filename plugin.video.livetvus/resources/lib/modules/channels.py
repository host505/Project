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

from common import *
import json
import base64


class Channel():

    @staticmethod
    def play_247retro():
        site_url = "http://www.247retro.com/"
        match_string = 'src: "(.+?)"'
        req = open_url(site_url)
        stream = find_single_match(req, match_string)
        if "m3u8" in stream:
            play(stream)
        else:
            dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_aljazeera():
        site_url = "https://www.aljazeera.com/live/"
        channel_match_string = '<iframe width="100%" src="(.+?)\&'
        video_match_string = '\'VIDEO_ID\': "(.+?)"'

        # Ensure YouTube addon MPEG-DASH setting is enabled and if not prompt user to set it
        yt_addon = xbmcaddon.Addon('plugin.video.youtube')
        if yt_addon.getSetting('kodion.video.quality.mpd') != 'true':
            dlg.ok(addon_name,
                   "This addon requires MPEG-DASH to be enabled in the YouTube addon. Once enabled try again.")
            yt_settings = xbmcaddon.Addon('plugin.video.youtube').openSettings()
            xbmc.executebuiltin("yt_settings")

        else:
            # Get A Jazerra YouTube Channel
            req = open_url(site_url)
            channel_url = find_single_match(req, channel_match_string)

            # Get Stream
            req = open_url(channel_url)
            id = find_single_match(req, video_match_string)
            if id is not "":
                play_youtube(id)
            else:
                dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_bloomberg():
        youtube_id = "Ga3maNZ0x0w"

        # Ensure YouTube addon MPEG-DASH setting is enabled and if not prompt user to set it
        yt_addon = xbmcaddon.Addon('plugin.video.youtube')
        if yt_addon.getSetting('kodion.video.quality.mpd') != 'true':
            dlg.ok(addon_name,
                   "This addon requires MPEG-DASH to be enabled in the YouTube addon. Once enabled try again.")
            yt_settings = xbmcaddon.Addon('plugin.video.youtube').openSettings()
            xbmc.executebuiltin("yt_settings")

        else:
            # Get Stream
            id = youtube_id
            if id is not "":
                play_youtube(id)
            else:
                dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_buzzr():
        site_url = "http://buzzrplay.com/watch"
        match_string = '<source src="(.+?)"'

        req = open_url(site_url)
        stream = find_single_match(req, match_string) + "?rebase=on"
        if "m3u8" in stream:
            play(stream)
        else:
            dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_catholic_tv():
        site_url = "http://www.catholictv.org/watch-live"
        player_match_string = '<iframe src="(.*?)"'
        stream_match_string = 'tp:releaseUrl="(.*?)\?'

        # Get Player
        req = open_url(site_url)
        url = find_single_match(req, player_match_string)

        # Get Stream
        req = open_url(url)
        stream = find_single_match(req, stream_match_string) + "?formats=m3u"

        if stream is not "":
            play(stream)
        else:
            dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_cbs_news():
        site_url = "https://www.cbsnews.com/live/"
        match_string = '"video":"(.+?)"'

        req = open_url(site_url)
        stream = find_single_match(req, match_string) + "?rebase=on"
        if "m3u8" in stream:
            play(stream)
        else:
            dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_charge():
        site_url = "https://watchcharge.com/watch-live/"
        match_string = 'file: "(.+?)"'

        req = open_url(site_url)
        stream = find_single_match(req, match_string)
        if stream is not "":
            play(stream)
        else:
            dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_cheddar():
        # Channel Selection
        source = xbmcgui.Dialog().select("Choose Channel", [
            "[COLOR blue]Cheddar[/COLOR]",
            "[COLOR blue]Cheddar Big News[/COLOR]"
        ])
        if source == 0:
            stream = "https://content.uplynk.com/channel/4ee18bd581dc4d3b90303e0cb9beeb0f.m3u8"
        if source == 1:
            stream = "https://wowzaprod124-i.akamaihd.net/hls/live/505691/261805b7/playlist.m3u8"
        if source < 0:
            exit()

        # Play Cheddar stream depending on Channel Selection
        play(stream)

    @staticmethod
    def play_comet():
        site_url = "https://www.comettv.com/watch-live/"
        match_string = '	file: "(.+?)"'

        req = open_url(site_url)
        stream = find_single_match(req, match_string)
        if stream is not "":
            play(stream)
        else:
            dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_hsn():
        hsn1_url = "https://hsn.com/watch/live"
        hsn2_url = "https://hsn.com/watch/live?network=4"
        stream_id_match_string = "watchTemplate.PlayLiveYoutubeVideo\('(.+?)'"
        program_match_string = '<span class="show-title" id="show-title" tabindex="0">(.+?)</span>'

        # Ensure YouTube addon MPEG-DASH setting is enabled and if not prompt user to set it
        yt_addon = xbmcaddon.Addon('plugin.video.youtube')
        if yt_addon.getSetting('kodion.video.quality.mpd') != 'true':
            dlg.ok(addon_name,
                   "This addon requires MPEG-DASH to be enabled in the YouTube addon. Once enabled try again.")
            yt_settings = xbmcaddon.Addon('plugin.video.youtube').openSettings()
            xbmc.executebuiltin("yt_settings")

        else:
            # Get HSN TV current program info
            req = open_url(hsn1_url)
            hsn1_program = find_single_match(req, program_match_string).replace("&amp;", "&")

            # Get HSN2 TV current program info
            req = open_url(hsn2_url)
            hsn2_program = find_single_match(req, program_match_string).replace("&amp;", "&")

            # Channel Selection
            source = xbmcgui.Dialog().select("Choose Channel", [
                "[COLOR blue]HSN TV:[/COLOR] " + hsn1_program,
                "[COLOR blue]HSN2 TV:[/COLOR] " + hsn2_program
            ])
            if source == 0:
                channel_url = hsn1_url
            if source == 1:
                channel_url = hsn2_url
            if source < 0:
                exit()

            # Get HSN TV or HSN2 TV stream depending on Channel Selection
            req = open_url(channel_url)
            id = find_single_match(req, stream_id_match_string)
            if id is not "":
                play_youtube(id)
            else:
                dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_light_tv():
        site_url = "http://www.lighttv.com/"
        embed_match_string = 'frameborder="0" scrolling="no" src="(.+?)"'
        tokens_match_string = 'tokens=(.+?)"'
        stream_match_string = 'src: "(.+?)"'

        # Get embed url
        req = open_url(site_url)
        embed_url = find_single_match(req, embed_match_string)

        # Get tokens
        req = open_url(site_url)
        tokens = find_single_match(req, tokens_match_string)

        # Get stream url
        req = open_url(embed_url)
        stream = find_single_match(req, stream_match_string) + tokens

        if "m3u8" in stream:
            play(stream)
        else:
            dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_newsmax_tv():
        site_url = "https://www.newsmaxtv.com/"
        embed_match_string = '"embedUrl": "(.+?)"'
        stream_match_string = 'hlsStreamUrl(.+?)",'

        # Get embed url
        req = open_url(site_url)
        embed_url = find_single_match(req, embed_match_string)

        # Get stream url
        req = open_url(embed_url)
        stream = find_single_match(req, stream_match_string).replace('\\":\\"', '').replace('\\\\\\', '').replace('\\',
                                                                                                                  '')

        if "m3u8" in stream:
            play(stream)
        else:
            dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_pbs_kds():
        json_url = 'http://pbskids.org/api/video/v1/livestream'

        # Get stream url
        req = open_url(json_url)
        pbs_kids_json = json.loads(req)
        stream = pbs_kids_json["livestream"] + "?rebase=on"

        if "m3u8" in stream:
            play(stream)
        else:
            dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_qvc():
        site_url = "http://www.qvc.com/content/shop-live-tv.html"
        json_match_string = "var oLiveStreams=(.+?),\n"

        # Get QVC json
        req = open_url(site_url)
        qvc_json = json.loads(find_single_match(req, json_match_string))

        qvc_url = qvc_json["QVC"]["url"]
        qvc2_url = qvc_json["2CH"]["url"]
        iq_url = qvc_json["STA"]["url"]

        # Channel Selection
        source = xbmcgui.Dialog().select("Choose Channel", [
            "[COLOR blue]QVC[/COLOR]",
            "[COLOR blue]QVC2[/COLOR]",
            "[COLOR blue]Beauty IQ[/COLOR]"
        ])
        if source == 0:
            channel_url = qvc_url
        if source == 1:
            channel_url = qvc2_url
        if source == 2:
            channel_url = iq_url
        if source < 0:
            exit()

        # Play QVC stream depending on Channel Selection
        stream = "http:" + channel_url + "?rebase=on"
        if "m3u8" in channel_url:
            play(stream)
        else:
            dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_revn_tv():
        site_url = "http://www.revntv.com/watch/watch-online/"
        embed_match_string = '<iframe src="(.+?)"'
        tokens_match_string = '<script id="(.+?)"'
        json_url_main = 'http://json.dacast.com/b/'

        # Get embed url
        req = open_url(site_url)
        embed_url = "http:" + find_single_match(req, embed_match_string)

        # Get tokens
        req = open_url(embed_url)
        tokens = find_single_match(req, tokens_match_string).replace("_", "/")

        # Build json url
        json_url = json_url_main + tokens

        # Get stream url
        req = open_url(json_url)
        revn_json = json.loads(req)
        stream = "http:" + revn_json["hls"] + "?rebase=on"

        if "m3u8" in stream:
            play(stream)
        else:
            dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_rt():
        rt_url = "https://www.rt.com/on-air/"
        rtus_url = "https://www.rt.com/on-air/rt-america-air/"
        rtuk_url = "https://www.rt.com/on-air/rt-uk-air/"
        rtfr_url = "https://francais.rt.com/en-direct"
        rtar_url = "https://arabic.rt.com/live/"
        rtesp_url = "https://actualidad.rt.com/en_vivo"
        rtdoc_url = "https://rtd.rt.com/on-air/"
        stream_id_match_string = "file: '(.+?)'"
        stream_france_id_match_string = 'file: "(.+?)"'
        stream_arabic_id_match_string = "file': '(.+?)'"
        stream_spanish_id_match_string = "embed/(.+?)\?"
        stream_doc_id_match_string = 'url: "(.+?)"'

        # Ensure YouTube addon MPEG-DASH setting is enabled and if not prompt user to set it
        yt_addon = xbmcaddon.Addon('plugin.video.youtube')
        if yt_addon.getSetting('kodion.video.quality.mpd') != 'true':
            dlg.ok(addon_name,
                   "This addon requires MPEG-DASH to be enabled in the YouTube addon. Once enabled try again.")
            yt_settings = xbmcaddon.Addon('plugin.video.youtube').openSettings()
            xbmc.executebuiltin("yt_settings")

        else:
            # Channel Selection
            source = xbmcgui.Dialog().select("Choose Channel", [
                "[COLOR blue]RT Global[/COLOR]",
                "[COLOR blue]RT America[/COLOR]",
                "[COLOR blue]RT UK[/COLOR]",
                "[COLOR blue]RT France[/COLOR]",
                "[COLOR blue]RT Arabic[/COLOR]",
                "[COLOR blue]RT Spanish[/COLOR]",
                "[COLOR blue]RT Documentary[/COLOR]"
            ])
            if source == 0:
                channel_url = rt_url
                match_string = stream_id_match_string
                vid_name = "RT Global"
            if source == 1:
                channel_url = rtus_url
                match_string = stream_id_match_string
                vid_name = "RT America"
            if source == 2:
                channel_url = rtuk_url
                match_string = stream_id_match_string
                vid_name = "RT UK"
            if source == 3:
                channel_url = rtfr_url
                match_string = stream_france_id_match_string
                vid_name = "RT France"
            if source == 4:
                channel_url = rtar_url
                match_string = stream_arabic_id_match_string
                vid_name = "RT Arabic"
            if source == 5:
                channel_url = rtesp_url
                match_string = stream_spanish_id_match_string
            if source == 6:
                channel_url = rtdoc_url
                match_string = stream_doc_id_match_string
                vid_name = "RT Documentary"
            if source < 0:
                exit()

            # Get RT stream depending on Channel Selection
            req = open_url(channel_url)

            # Use YouTube for RT Spanish Streams
            if source == 5:
                id = find_single_match(req, match_string)
                if id is not "":
                    play_youtube(id)
                else:
                    dlg.ok(addon_name, "Unable to get stream. Please try again later.")

            # Stream direct for streams other than RT Spanish
            else:
                stream = find_single_match(req, match_string)
                if "m3u8" in stream:
                    play(stream)
                else:
                    dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_sky_news():
        site_url = "https://news.sky.com/watch-live"
        match_string = 'embed/(.+?)\?'

        yt_addon = xbmcaddon.Addon('plugin.video.youtube')
        if yt_addon.getSetting('kodion.video.quality.mpd') != 'true':
            dlg.ok(addon_name,
                   "This addon requires MPEG-DASH to be enabled in the YouTube addon. Once enabled try again.")
            yt_settings = xbmcaddon.Addon('plugin.video.youtube').openSettings()
            xbmc.executebuiltin("yt_settings")

        else:
            req = open_url(site_url)
            id = find_single_match(req, match_string)
            if id is not "":
                play_youtube(id)
            else:
                dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_stadium():
        # Get stream
        req = open_url(base64.b64decode(
            'aHR0cDovL21oYW5jb2M3LnNvdXJjZWNvZGUuYWcvbGl2ZXR2X2RpcmVjdC92MS9nZXRfc3RyZWFtLnBocD9pZD1zdGFkaXVt'))
        stadium_json = json.loads(req)
        stream = stadium_json["results"][0]["stream"]

        if "m3u8" in stream and stream != "null":
            play(stream)
        else:
            dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_tbd():
        site_url = "http://tbd.com/"
        match_string = '\'file\': "(.+?)"'

        req = open_url(site_url)
        stream = find_single_match(req, match_string)
        if stream is not "":
            play(stream)
        else:
            dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_the_country_network():
        site_url = "http://tcncountry.net/watch-live.htm"
        embed_match_string = '<iframe src="(.+?)"'
        tokens_match_string = '<script id="(.+?)"'
        json_url_main = 'http://json.dacast.com/b/'

        # Get embed url
        req = open_url(site_url)
        embed_url = find_single_match(req, embed_match_string)

        # Get tokens
        req = open_url(embed_url)
        tokens = find_single_match(req, tokens_match_string).replace("_", "/")

        # Build json url
        json_url = json_url_main + tokens

        # Get stream url
        req = open_url(json_url)
        tcn_json = json.loads(req)
        stream = "http:" + tcn_json["hls"] + "?rebase=on"

        if "m3u8" in stream:
            play(stream)
        else:
            dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_campfire(channel):
        if channel == 'tuff_tv':
            id = 'woo'
        elif channel == 'radiou':
            id = 'XDc'
        elif channel == 'spirit_tv':
            id = 'bqg'

        site_url = "http://player.campfyre.tv/{id}".format(id=id)
        match_string = '"file": "(.+?)"'

        req = open_url(site_url)
        stream = "http:" + find_single_match(req, match_string)
        if "m3u8" in stream:
            play(stream)
        else:
            dlg.ok(addon_name, "Unable to get stream. Please try again later.")

    @staticmethod
    def play_tvcatchup(url):
        site_url = url
        match_string = '<source src="(.+?)"'

        req = open_url(site_url)
        stream = find_single_match(req, match_string) + "?rebase=on"
        if "m3u8" in stream:
            play(stream)
        else:
            dlg.ok(addon_name, "Unable to get stream. Please try again later.")
