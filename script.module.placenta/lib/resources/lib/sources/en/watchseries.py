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

import re,urllib,urlparse,json,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser
from resources.lib.modules import log_utils

# Working: https://seriesfree.to/episode/dawsons_creek_s6_e23.html

class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['watchseriesfree.to','seriesfree.to']
		self.base_link = 'https://seriesfree.to/'
		self.search_link = 'https://seriesfree.to/search/%s'
		self.ep_link = 'https://seriesfree.to/episode/%s.html'

	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
			url = urllib.urlencode(url)
			log_utils.log('tvshow url: %s' % url)
			return url
		except:
			failure = traceback.format_exc()
			log_utils.log('WATCHSERIES - Exception: \n' + str(failure))
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
			failure = traceback.format_exc()
			log_utils.log('WATCHSERIES - Exception: \n' + str(failure))
			return


	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			if url == None: return sources

			data = urlparse.parse_qs(url)		  
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])   
			
			
			# compile the query part of the episode-page url
			# keep only normal characters and use underscores for etc
			req	= '%s s%s e%s' % (data['tvshowtitle'], int(data['season']), int(data['episode']))
			req = req.replace('\'','').lower()
			req = self.ep_link % re.sub('\W+','_',req)
			#log_utils.log('req = %s' % req) ########
					
			
			# three attempts to pull up the episode-page, then bail
			for i in range(3):
				result = client.request(req, timeout=10)
				if not result == None: break
				
				
			# get the key div's contents
			# then get all the links along with preceding text hinting at host
			dom = dom_parser.parse_dom(result, 'div', attrs={'class':'links', 'id': 'noSubs'})
			result = dom[0].content		
			links = re.compile('<i class="fa fa-youtube link-logo"></i>([^<]+).*?href="([^"]+)"\s+class="watch',re.DOTALL).findall(result)


			
			# master list of hosts ResolveURL and placenta itself can resolve
			# we'll check against this list to not waste connections on unsupported hosts
			hostDict = hostDict + hostprDict
			
			conns = 0 
			for pair in links:
				if conns > 16: break	 # n sources could potentially cost n*range connections!!! 
				
				
				# the 2 groups from the link search = hoster name, episode page url
				host = pair[0].strip()	  
				link = pair[1]
				
				
				# check for valid hosts and jump to next loop if not valid
				valid, host = source_utils.is_host_valid(host, hostDict)
				#log_utils.log("\n\n** conn #%s: %s (valid:%s) %s" % (conns,host,valid,link)) #######
				if not valid: continue
				
				
				# two attempts per source link, then bail
				link = urlparse.urljoin(self.base_link, link)
				for i in range(2):
					result = client.request(link, timeout=3)
					conns += 1
					if not result == None: break	 
				
				
				# if both attempts failed, using the result will too, so bail to next loop
				try:
					link = re.compile('href="([^"]+)"\s+class="action-btn').findall(result)[0]
				except: 
					#log_utils.log(' ** failed to findall on result **') #######
					continue
					
					
				# I don't think this scraper EVER has direct links, but...
				#  (if nothing else, it sets the quality)
				try:
					u_q, host, direct = source_utils.check_directstreams(link, host)
				except:
					#log_utils.log('FAILED DS CHECK ~~~~~~~~~~~~~~') #######
					continue
					
				# check_directstreams strangely returns a list instead of a single 2-tuple
				link, quality = u_q[0]['url'], u_q[0]['quality']
				#log_utils.log('    checked host: %s' % host)
				#log_utils.log('    checked direct: %s' % direct)
				#log_utils.log('    quality, link: %s, %s' % (quality,link))
				#log_utils.log('    # of urls: %s' % len(u_q))

				
				sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'direct': direct, 'debridonly': False})
					
			return sources
		except:
			failure = traceback.format_exc()
			log_utils.log('WATCHSERIES - Exception: \n' + str(failure))
			return sources


	def resolve(self, url):
		return url

