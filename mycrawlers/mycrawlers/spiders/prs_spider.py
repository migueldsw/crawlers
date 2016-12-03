# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup as BS
import os

from mycrawlers.items import ItemGeneric

def composePR(perguntas,respostas,index):
	return "P:\n%s\nR:\n%s" %(perguntas[index],respostas[index])


def writeFile(filename,content):
	f = open(filename,'w')
	f.write(str(content).encode('utf8') + '\n')
	f.close()

def appendFile(filename,content):
	f = open(filename,'a')
	f.write(content.encode('utf8') + '\n')
	f.close()

def htm2txt(htm):
	frag = BS(htm)
	return frag.get_text()

INCLUSION_WORDS = ['/noticia']
EXCLUSION_WORDS = ['busca/?q']

def check_url(url,inclusion_words_list,exclusion_words_list):
	#the given url must have at least one of the inclusion words, and none of the exclusion words.
	accept = False
	for w in inclusion_words_list:
		if w in url:
			accept = True
			break
	for w in exclusion_words_list:
		if w in url:
			accept = False
			break
	return accept

class PRSpider(scrapy.Spider):
	name = "prspider"
	start_urls = [
		'http://www.sebrae.com.br/sites/PortalSebrae/faq?temas=&q=&pagina=1',
		'http://www.sebrae.com.br/sites/PortalSebrae/faq?temas=&q=&pagina=2',
		'http://www.sebrae.com.br/sites/PortalSebrae/faq?temas=&q=&pagina=3',
		'http://www.sebrae.com.br/sites/PortalSebrae/faq?temas=&q=&pagina=4',
		'http://www.sebrae.com.br/sites/PortalSebrae/faq?temas=&q=&pagina=5',
		'http://www.sebrae.com.br/sites/PortalSebrae/faq?temas=&q=&pagina=6',
		'http://www.sebrae.com.br/sites/PortalSebrae/faq?temas=&q=&pagina=7',
		'http://www.sebrae.com.br/sites/PortalSebrae/faq?temas=&q=&pagina=8',
		'http://www.sebrae.com.br/sites/PortalSebrae/faq?temas=&q=&pagina=9',
		'http://www.sebrae.com.br/sites/PortalSebrae/faq?temas=&q=&pagina=10'
		]
	CONT = 0

	def parse(self, response):
		rr = response
		perguntas = rr.xpath('//header/h3/text()').extract()
		rawRespostas = rr.xpath('//div[@class="collap-body"]').extract()
		respostas = []
		outdir = './out'
		if not os.path.isdir(outdir):
			os.makedirs(outdir)
		for i in rawRespostas:
			respostas.append(htm2txt(i))
		
		for i in range(len(perguntas)):
			pr_str = composePR(perguntas,respostas,i)
			PRSpider.CONT+=1
			writeFile('out/PR%d'%PRSpider.CONT,pr_str)

		#print "THE DATA AMOUNT IS %d/%d !!!!!!!!!!" %(len(perguntas),len(respostas))
		#

class Spider1(CrawlSpider):
	name = "spider_1"
	allowed_domains = ['jconline.ne10.uol.com.br']
	start_urls = [
		'http://jconline.ne10.uol.com.br/',
		'http://jconline.ne10.uol.com.br/canal/cidades/geral/noticia/2016/11/23/rodoviarios-nao-vao-aderir-a-paralisacao-nacional-do-dia-25-261416.php'
		]
	rules = (Rule(LinkExtractor(allow=(), ), callback="parse_page", follow= True),)

	CONT = 1

	def parse_page(self, response):
		rr = response
		if check_url(rr.url,INCLUSION_WORDS,EXCLUSION_WORDS):

			appendFile('URLS.log',rr.url)

			itensRaw = []
			
			itensRaw += rr.xpath('//h1/text()').extract()
			itensRaw += rr.xpath('//h2/text()').extract()
			itensRaw += rr.xpath('//h3/text()').extract()
			itensRaw += rr.xpath('//p/text()').extract()

			#print ('LEN : '+str(len(itensRaw)))
			itensOut = []
			outdir = './out'
			if not os.path.isdir(outdir):
				os.makedirs(outdir)
			for i in itensRaw:
				txt = htm2txt(i.encode('utf8'))
				if (len(txt) >= 20): #string min. length
					itensOut.append(txt)
					appendFile('out/DATA'+str(Spider1.CONT),txt)
			Spider1.CONT+=1
