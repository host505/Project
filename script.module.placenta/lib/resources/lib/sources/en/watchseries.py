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

import re,urllib,urlparse,json,base64, random

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
		self.max_conns = 10 #set to 10 bc that = how many the prev scraper might hit
		self.min_srcs = 3

	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		log_utils.log('\n\n~~~ inside tvshow()')

		try:
			
			query = self.search_link % urllib.quote_plus(cleantitle.query(tvshowtitle))
			#result = client.request(query)
			
			for i in range(3):
				result = client.request(query, timeout=3)
				if not result == None: break
			
			
			
			t = [tvshowtitle] + source_utils.aliases_to_array(aliases)
			t = [cleantitle.get(i) for i in set(t) if i]
			result = re.compile('itemprop="url"\s+href="([^"]+).*?itemprop="name"\s+class="serie-title">([^<]+)', re.DOTALL).findall(result)
			for i in result:
				if cleantitle.get(cleantitle.normalize(i[1])) in t and year in i[1]: url = i[0]

			url = url.encode('utf-8')
			
			url = {'show_url': url,'show_title': tvshowtitle}
			
			log_utils.log('\n\n~~~ outgoing tvshow() url')
			log_utils.log(url)
			
			return url
		except:
			return


	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		log_utils.log('\n\n~~~ inside episode()')

		try:
		
			if url == None: return
			
			tvshowtitle = url['show_title']
			url = url['show_url']


			log_utils.log('\n\n~~~ tvshowtitle: %s' % tvshowtitle)
			log_utils.log('\n\n~~~ incomingish episode() url')
			log_utils.log(url)

			url = urlparse.urljoin(self.base_link, url)
			log_utils.log('\n\n~~~ baselink-joined url')
			log_utils.log(url)
			
			# this should probably get multiple passes like the first request in sources()
			#result = client.request(url)
			
			for i in range(3):
				result = client.request(url, timeout=3)
				if not result == None: break
			
				
			title = cleantitle.get(title)

			
			# assume seriesfree has YYYY-MM-DD listed in ep index
			#  (this appears to not always be the case though)
			premiered = re.compile('(\d{4})-(\d{2})-(\d{2})').findall(premiered)[0]
			premiered = '%s/%s/%s' % (premiered[2], premiered[1], premiered[0])
			items = dom_parser.parse_dom(result, 'a', attrs={'itemprop':'url'})

			url = [i.attrs['href'] for i in items if bool(re.compile('<span\s*>%s<.*?itemprop="episodeNumber">%s<\/span>' % (season,episode)).search(i.content))][0]
			
			# if no url, just compile the expected show_s#_e#
			# url = '%s_s%s_e%s' % (title, int(season), int(episode))
			# url = urlparse.urljoin(self.ep_link, url)
			# outgoing episode url format: /episode/x_files_s4_e10.html		
			
			url = url.encode('utf-8')
			
			url = {'show_title': tvshowtitle, 'ep_url': url, 's': season, 'e': episode}
			
			log_utils.log('\n\n~~~ outgoing episode() url')
			log_utils.log(url)
			
			return url
		except:
			return


	def sources(self, url, hostDict, hostprDict):
	
		log_utils.log('\n\n~~~ incoming sources() url')
		log_utils.log(url)
	
		try:
			sources = []
			if url == None: return sources

			tvshowtitle = url['show_title']
			season = url['s']
			episode = url['e']
			url = url['ep_url']
			
			
			#url = {'show_title': tvshowtitle, 'ep_url': url, 's': season, 'e': episode}
			req = urlparse.urljoin(self.base_link, url)
			
			log_utils.log('\n\n~~~ sources() pre-request req url')
			log_utils.log(req)
			
			
#			data = urlparse.parse_qs(url)		  
#			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])   
			
			
			# compile the query part of the episode-page url
			# keep only normal characters and use underscores for etc
#			req	= '%s s%s e%s' % (data['tvshowtitle'], int(data['season']), int(data['episode']))
#			req = req.replace('\'','').lower()
#			req = self.ep_link % re.sub('\W+','_',req)
			#log_utils.log('req = %s' % req) ########
					
			
			# three attempts to pull up the episode-page, then bail
			for i in range(3):
				result = client.request(req, timeout=3)
				if not result == None: break
				
				
			# get the key div's contents
			# then get all the links along with preceding text hinting at host
			# ep pages sort links by hoster which is bad if the top hosters
			#	are unavailable for debrid OR if they're ONLY avail for debrid
			#	(for non-debrid peeps) so shuffle the list
			dom = dom_parser.parse_dom(result, 'div', attrs={'class':'links', 'id': 'noSubs'})
			result = dom[0].content		
			links = re.compile('<i class="fa fa-youtube link-logo"></i>([^<]+).*?href="([^"]+)"\s+class="watch',re.DOTALL).findall(result)
			random.shuffle(links)


			
			# master list of hosts ResolveURL and placenta itself can resolve
			# we'll check against this list to not waste connections on unsupported hosts
			hostDict = hostDict + hostprDict
			
			conns = 0 
			for pair in links:
			
				# try to be a little polite, and limit connections 
				#  (unless we're not getting sources)
				if conns > self.max_conns and len(sources) > self.min_srcs: break	 

				
				# the 2 groups from the link search = hoster name, episode page url
				host = pair[0].strip()	  
				link = pair[1]
				
				
				# check for valid hosts and jump to next loop if not valid
				valid, host = source_utils.is_host_valid(host, hostDict)
				#log_utils.log("\n\n** conn #%s: %s (valid:%s) %s" % (conns,host,valid,link)) #######
				if not valid: continue
				
				
				# two attempts per source link, then bail
				# NB: n sources could potentially cost n*range connections!!! 
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
				#log_utils.log('	checked host: %s' % host)
				#log_utils.log('	checked direct: %s' % direct)
				#log_utils.log('	quality, link: %s, %s' % (quality,link))
				#log_utils.log('	# of urls: %s' % len(u_q))

				
				sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'direct': direct, 'debridonly': False})
					
			return sources
		except:
			failure = traceback.format_exc()
			log_utils.log('WATCHSERIES - Exception: \n' + str(failure))
			return sources


	def resolve(self, url):
		return url
