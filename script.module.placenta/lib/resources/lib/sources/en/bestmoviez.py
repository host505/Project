# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @Daddy_Blamo wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Placenta
# Addon id: plugin.video.placenta
# Addon Provider: Mr.Blamo

import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils

# Working: https://www.best-moviez.ws/deadpool-2-2018-1080p-web-dl-dd5-1-h264-cmrg/
# Working: https://www.best-moviez.ws/deadpool-2-2018
# Working: https://www.best-moviez.ws/deadpool-2
# Working: https://www.best-moviez.ws/deadpool--2--2018
# Failed:  https://www.best-moviez.ws/Deadpool+2+2018

class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['best-moviez.ws']
		self.base_link = 'http://www.best-moviez.ws'
		self.search_link = '/%s'


	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'title': title, 'year': year}
			url = urllib.urlencode(url)
			return url
		except:
			return

	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
			url = urllib.urlencode(url)
			return url
		except:
			return

	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if url == None: return

			url = urlparse.parse_qs(url)
			url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
			url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
			url = urllib.urlencode(url)
			return url
		except:
			return

	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []

			if url == None: return sources

			if debrid.status() == False: raise Exception()

			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

			hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

			query = '%s s%02de%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
			#query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
			query = re.sub('[\\\\:;*?"<>|/ \+\']', '-', query)

			url = self.search_link % urllib.quote_plus(query)
			url = urlparse.urljoin(self.base_link, url)
			log_utils.log('\n\n\n\n\n\nquery, url: %s, %s' % (query,url))
			r = client.request(url)

			#posts = client.parseDOM(r, 'article', attrs={'id': 'post-\d+'})
			#posts = client.parseDOM(posts, 'h1')
			#posts = zip(client.parseDOM(posts, 'a', ret= 'href'),(client.parseDOM(posts, 'a', attrs={'rel': 'bookmark'})))

			# grab the (only?) relevant div and cut off the footer
			r = client.parseDOM(r, "div", attrs={'class': 'entry-content'})[0]
			log_utils.log('~~~~~~~ parsed DOM')
			r = re.sub('shareaholic-canvas.+', '', r, flags=re.DOTALL)
			#log_utils.log(r)
			
			# check for actual <a> links then wipe them all
			a_txt = client.parseDOM(r, "a", attrs={'href': '.+?'})
			a_url = client.parseDOM(r, "a", ret = "href")
			r = re.sub('<a .+?</a>', '', r, flags=re.DOTALL)
			for url in a_url:
				log_utils.log('url: ' + url)
			
			# remove <img>
			r = re.sub('<img .+?>', '', r, flags=re.DOTALL)
			
			# get naked urls
			links = re.findall('https?://[^ <"\'\s]+', r, re.DOTALL)
			#links = re.compile('https?://[^ <"]+',re.DOTALL).findall(r)
			for url in links:
				log_utils.log('url: ' + url)
				
			pairs = zip(a_url,a_txt)
			pairs.append(zip(links,links))
			for pair in pairs:
				log_utils.log('pair: %s, %s' % (pair[1],pair[0]))

			
			for item in posts:

				try:
					name = item[1]
					name = client.replaceHTMLCodes(name)

					t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d+E\d+|S\d+|3D)(\.|\)|\]|\s|)(.+|)', '', name, re.I)

					if not cleantitle.get(t) == cleantitle.get(title): raise Exception()

					y = re.findall('[\.|\(|\[|\s](\d{4}|S\d+E\d+|S\d+)[\.|\)|\]|\s]', name, re.I)[-1].upper()

					if not y == hdlr: raise Exception()

					r = client.request(item[0], referer= self.base_link)
					r = client.parseDOM(r, 'article', attrs={'id': 'post-\d+'})
					#links = re.findall('>Single Links</b>(.+?)<p><b><span', data, re.DOTALL)
					links = [i for i in client.parseDOM(r, 'p') if 'Single Links' in i]
					links = zip(client.parseDOM(links, 'a', ret='href'),
								client.parseDOM(links, 'a', attrs={'href': '.+?'}))

					for item in links:
						try:
							quality, info = source_utils.get_release_quality(item[1], item[0])
							try:
								size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+) (?:GB|GiB|MB|MiB))', r[0], re.DOTALL)[0].strip()
								div = 1 if size.endswith(('GB', 'GiB')) else 1024
								size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
								size = '%.2f GB' % size
								info.append(size)
							except:
								pass

							info = ' | '.join(info)

							if any(x in item[0] for x in ['.rar', '.zip', '.iso']): raise Exception()
							url = client.replaceHTMLCodes(item[0])
							url = url.encode('utf-8')

							hostDict = hostDict + hostprDict

							valid, host = source_utils.is_host_valid(url, hostDict)
							if not valid: continue
							sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url,
											'info': info, 'direct': False, 'debridonly': True})
						except:
							pass

				except:
					pass

			return sources
		except:
			return sources

	def resolve(self, url):
		return url



'''
EXAMPLE: <a> links after "Single Link" (note no "S")
<div class="entry-content">
<div style="text-align:center"><img src="https://i103.fastpic.ru/big/2018/0808/81/371ccc697bd9da5d664322cee07a1581.jpg" /></div>
<div style="text-align:center"><span style="font-weight:bold">Deadpool 2 (2018) 720p BluRay x264 DTS-HDC</span><br />
<span style="font-weight:bold">Language(s)</span>: English<br />
01:59:00 | 1280&#215;536 @ 6200 kb/s | 23.98 fps(r) | DTS, 44100 Hz, 6CH, 1509 kb/s | 6.42 GB<br />
<span style="font-weight:bold">Genre(s)</span>: Action, Adventure, Comedy<br />
<a href="https://www.imdb.com/title/tt5463162/"><span style="font-weight:bold">IMDB</span></a></div>
<p><span id="more-75092"></span></p>
<div style="text-align:center"> Foul-mouthed mutant mercenary Wade Wilson (AKA. Deadpool), brings together a team of fellow mutant rogues to protect a young boy with supernatural abilities from the brutal, time-traveling cyborg, Cable.</p>
...
<span style="font-weight:bold"><span style="color:#FF0000">Download</span></span></p>
<p><span style="font-weight:bold"><span style="color:#00BF00">Single Link</span></span></p>
<p>http://nitroflare.com/view/4424F59C04B5172/Deadpool.2.2018.720p.BluRay.x264.DTS-HDC.mkv</p>
<p><span style="font-weight:bold"><span style="color:#0080FF">NitroFlare</span></span></p>
<p>http://nitroflare.com/view/F8885D081E8036B/Deadpool.2.2018.720p.BluRay.x264.DTS-HDC.part1.rar<br />


EXAMPLE: <a> links after "Single Links" (note now there is an "S")
<div class="entry-content">
...
<p><b><span style="color: #ff0000">DownLoad</b></span></p>
<p><b><span style="color: #ff0000">Single Links</b></span><br />
<a href="https://nitroflare.com/view/B79F3390ED3305B/Avengers.Infinity.War.2018.2160p.UHD.BluRay.x265-SWTYBLZ.mkv">Avengers.Infinity.War.2018.2160p.UHD.BluRay.x265-SWTYBLZ.mkv</a></p>
<p><a href="https://uploadgig.com/file/download/f8e5B103e779F0a4/Avengers.Infinity.War.2018.2160p.UHD.BluRay.x265-SWTYBLZ.mkv">Avengers.Infinity.War.2018.2160p.UHD.BluRay.x265-SWTYBLZ.mkv</a></p>
<p><b><span style="color: #ff0000">NitroFlare</b></span><br />
<a href="https://nitroflare.com/view/9EACE029F149096/Avengers.Infinity.War.2018.2160p.UHD.BluRay.x265-SWTYBLZ.part01.rar">Avengers.Infinity.War.2018.2160p.UHD.BluRay.x265-SWTYBLZ.part01.rar</a><br />
<a href="https://nitroflare.com/view/5F167E50AFBCDD7/Avengers.Infinity.War.2018.2160p.UHD.BluRay.x265-SWTYBLZ.part02.rar">Avengers.Infinity.War.2018.2160p.UHD.BluRay.x265-SWTYBLZ.part02.rar</a><br />


EXAMPLE: <a> link but to a .iso file
<div class="entry-content">
...
<p><b><span style="color: #ff0000">DownLoad</b></span></p>
<p><b><span style="color: #ff0000">Single Link</b></span><br />
<a href="https://nitroflare.com/view/D0ADAE9780B6340/Avengers.Age.Of.Ultron.UHDBD-TERMiNAL.iso">Avengers.Age.Of.Ultron.UHDBD-TERMiNAL.iso</a></p>
<p><a href="https://uploadgig.com/file/download/5c02b57c909968cf/Avengers.Age.Of.Ultron.UHDBD-TERMiNAL.iso">Avengers.Age.Of.Ultron.UHDBD-TERMiNAL.iso</a></p>
<p><b><span style="color: #ff0000">NitroFlare</b></span><br />
<a href="https://nitroflare.com/view/435E34B243AEEC1/Avengers.Age.Of.Ultron.UHDBD-TERMiNAL.part01.rar">Avengers.Age.Of.Ultron.UHDBD-TERMiNAL.part01.rar</a><br />
<a href="https://nitroflare.com/view/D11B2E1CEEB4D00/Avengers.Age.Of.Ultron.UHDBD-TERMiNAL.part02.rar">Avengers.Age.Of.Ultron.UHDBD-TERMiNAL.part02.rar</a><br />


EXAMPLE: Plain text inside (shared) <p>
<div class="entry-content">
...
<span style="font-weight:bold"><span style="color:#FF0000">Download</span></span></p>
<p><span style="font-weight:bold"><span style="color:#00BF00">Single Link</span></span></p>
<p>http://nitroflare.com/view/FBBCB2B4E2FE486/The.Death.of.Superman.2018.1080p.BluRay.DTS.x264-TayTO.mkv</p>
<p>
<span style="font-weight:bold"><span style="color:#0080FF">NitroFlare</span></span></p>
<p>http://nitroflare.com/view/EAF5BF83036A8DE/The.Death.of.Superman.2018.1080p.BluRay.DTS.x264-TayTO.part1.rar<br />
http://nitroflare.com/view/290A3D1480AD822/The.Death.of.Superman.2018.1080p.BluRay.DTS.x264-TayTO.part2.rar<br />



EXAMPLE: tv episode text links in <pre>, by type/quality
<div class="entry-content">
...
<span style="font-weight:bold">[LiNKs]</span></p>
<pre style="background:#BBBBBB"><br />
===================================================<br />
➡ Better.Call.Saul.S04E01.HDTV.x264-SVA<br />
===================================================<br /><br />
http://nitroflare.com/view/8E5BBDBD5378EB2/Better.Call.Saul.S04E01.HDTV.x264-SVA.mkv<br />
https://rapidgator.net/file/b1abba0d3fac85c7b4adecf2b194734d/Better.Call.Saul.S04E01.HDTV.x264-SVA.mkv.html<br />
https://uploadgig.com/file/download/e5c4bf10a454144A/Better.Call.Saul.S04E01.HDTV.x264-SVA.mkv<br />
https://k2s.cc/file/1e8490e210630/Better.Call.Saul.S04E01.HDTV.x264-SVA.mkv<br /><br />
===================================================<br />
➡ Better.Call.Saul.S04E01.720p.HDTV.x264-AVS<br />
===================================================<br /><br />
http://nitroflare.com/view/338D7D912CF954E/Better.Call.Saul.S04E01.720p.HDTV.x264-AVS.mkv<br />
https://rapidgator.net/file/f016b7ef0aed23a7eda75b459567a46a/Better.Call.Saul.S04E01.720p.HDTV.x264-AVS.mkv.html<br />
https://uploadgig.com/file/download/d671D3e4dD7e9385/Better.Call.Saul.S04E01.720p.HDTV.x264-AVS.mkv<br />
https://k2s.cc/file/9622e3c5abda5/Better.Call.Saul.S04E01.720p.HDTV.x264-AVS.mp4<br /><br />
===================================================<br />
➡ Better.Call.Saul.S04E01.HDTV.XviD-AFG [P2P]<br />
===================================================<br /><br />
http://nitroflare.com/view/DC7D1E0637F69DE/Better.Call.Saul.S04E01.XviD-AFG.avi<br />
https://rapidgator.net/file/e07a34e09bf8fa8490096a556106c7a3/Better.Call.Saul.S04E01.XviD-AFG.avi.html<br />
https://uploadgig.com/file/download/939Ddb7e78ba3994/Better.Call.Saul.S04E01.XviD-AFG.avi<br />
https://k2s.cc/file/7511e23d723cc/Better.Call.Saul.S04E01.XviD-AFG.mp4<br />
</pre>
'''
