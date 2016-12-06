# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
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

def remove_trash_itens(itens_lst,words_lst):
	out = []
	if words_lst == []:
		return itens_lst
	for i in itens_lst:
		ok = True
		for w in words_lst:
			if w in i:
				ok = False
		if ok:
			out.append(i)
	return out


def check_url(url,inclusion_words_list,exclusion_words_list):
	#the given url must have at least one of the inclusion words, and none of the exclusion words.
	accept = True
	for w in inclusion_words_list:
		if not w in url:
			accept = False
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

	INCLUSION_WORDS = ['/noticia']
	EXCLUSION_WORDS = ['busca/?q']

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
		#'http://jconline.ne10.uol.com.br/canal/cidades/geral/noticia/2016/11/23/rodoviarios-nao-vao-aderir-a-paralisacao-nacional-do-dia-25-261416.php'
		]
	rules = (Rule(LinkExtractor(allow=(), ), callback="parse_page", follow= True),)

	CONT = 0
	INCLUSION_WORDS = ['/noticia']
	EXCLUSION_WORDS = ['busca/?q']
	TRASH_WORDS = ['Todos os direitos reservados','Recomendados para voc','Publicado em']

	def parse_page(self, response):
		#crawler doc limit
		CRAW_LIMIT = 10
		if (Spider1.CONT>=CRAW_LIMIT):
			raise CloseSpider('docs_limit_exceeded')
		rr = response
		if check_url(rr.url,Spider1.INCLUSION_WORDS,Spider1.EXCLUSION_WORDS):

			appendFile('URLS.log',rr.url)

			itensRaw = []
			
			itensRaw += rr.xpath('//h1/text()').extract()
			itensRaw += rr.xpath('//h2/text()').extract()
			itensRaw += rr.xpath('//h3/text()').extract()
			itensRaw += rr.xpath('//p/text()').extract()

			itensRaw = remove_trash_itens(itensRaw,Spider1.TRASH_WORDS)
			#print ('LEN : '+str(len(itensRaw)))
			itensOut = []
			outdir = './out'
			if not os.path.isdir(outdir):
				os.makedirs(outdir)
			for i in itensRaw:
				txt = htm2txt(i.encode('utf8'))
				if (len(txt) >= 20): #string min. length
					itensOut.append(txt)
					appendFile('out/DOC-JC-'+str(Spider1.CONT),txt)
			Spider1.CONT+=1

class Spider2(CrawlSpider):
	name = "spider_2"
	allowed_domains = ['www.diariodepernambuco.com.br']
	start_urls = [
		'http://www.diariodepernambuco.com.br/app/noticia/vida-urbana/2016/12/05/interna_vidaurbana,678505/assalto-no-bompreco-de-olinda-termina-com-feridos-e-presos.shtml',
		'http://www.diariodepernambuco.com.br/',
		]
	rules = (Rule(LinkExtractor(allow=(), ), callback="parse_page", follow= True),)

	CONT = 0
	INCLUSION_WORDS = ['/noticia']
	EXCLUSION_WORDS = ['busca/?q']
	TRASH_WORDS = ['bua de mar','todos os direitos reservados.','Copyright Jornal Diario de Pernambuco', ' | 1']

	def parse_page(self, response):
		#crawler doc limit
		CRAW_LIMIT = 30
		if (Spider2.CONT>=CRAW_LIMIT):
			raise CloseSpider('docs_limit_exceeded')
		rr = response
		if check_url(rr.url,Spider2.INCLUSION_WORDS,Spider2.EXCLUSION_WORDS):

			appendFile('URLS.log',rr.url)

			itensRaw = []
			
			itensRaw += rr.xpath('//h1/text()').extract()
			itensRaw += rr.xpath('//h2/text()').extract()
			itensRaw += rr.xpath('//h3/text()').extract()
			itensRaw += rr.xpath('//br/text()').extract()

			itensRaw += rr.xpath('//div/text()').extract()
			itensRaw += rr.xpath('//em/text()').extract()
			itensRaw += rr.xpath('//strong/text()').extract()
			itensRaw += rr.xpath('//span[@class="h1"]/text()').extract()
			itensRaw += rr.xpath('//span[@class="gallery_desc"]/text()').extract()
			itensRaw += rr.xpath('//p/text()').extract()

			itensRaw = remove_trash_itens(itensRaw,Spider2.TRASH_WORDS)

			#print ('LEN : '+str(len(itensRaw)))
			itensOut = []
			outdir = './out'
			if not os.path.isdir(outdir):
				os.makedirs(outdir)
			for i in itensRaw:
				txt = htm2txt(i.encode('utf8'))
				if (len(txt) >= 20): #string min. length
					itensOut.append(txt)
					appendFile('out/DOC-DP-'+str(Spider2.CONT),txt)
			Spider2.CONT+=1

class Spider3(CrawlSpider):
	name = "spider_3"
	allowed_domains = ['http://www.folhape.com.br']
	start_urls = [
		'http://www.folhape.com.br/',
		]
	rules = (Rule(LinkExtractor(allow=(), ), callback="parse_page", follow= True),)

	CONT = 0
	INCLUSION_WORDS = ['/noticia','RENAN']
	EXCLUSION_WORDS = ['busca/?q']
	TRASH_WORDS = ['bua de mar','todos os direitos reservados.','Copyright Jornal Diario de Pernambuco', ' | 1']

	def parse_page(self, response):
		#crawler doc limit
		CRAW_LIMIT = 30
		if (Spider3.CONT>=CRAW_LIMIT):
			raise CloseSpider('docs_limit_exceeded')
		rr = response
		if check_url(rr.url,Spider3.INCLUSION_WORDS,Spider3.EXCLUSION_WORDS):

			appendFile('URLS.log',rr.url)

			itensRaw = []
			
			itensRaw += rr.xpath('//h1/text()').extract()
			itensRaw += rr.xpath('//h2/text()').extract()
			itensRaw += rr.xpath('//h3/text()').extract()


			itensRaw += rr.xpath('//p/text()').extract()


			itensRaw = remove_trash_itens(itensRaw,Spider3.TRASH_WORDS)

			#print ('LEN : '+str(len(itensRaw)))
			itensOut = []
			outdir = './out'
			if not os.path.isdir(outdir):
				os.makedirs(outdir)
			for i in itensRaw:
				txt = htm2txt(i.encode('utf8'))
				if (len(txt) >= 20): #string min. length
					itensOut.append(txt)
					appendFile('out/DOC-DP-'+str(Spider3.CONT),txt)
			Spider3.CONT+=1
