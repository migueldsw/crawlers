# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as BS
import os

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

class Spider1(scrapy.Spider):
	name = "spider_1"
	start_urls = [
		'http://jconline.ne10.uol.com.br/canal/cidades/geral/noticia/2016/11/23/rodoviarios-nao-vao-aderir-a-paralisacao-nacional-do-dia-25-261416.php'
		]
	CONT = 0

	def parse(self, response):
		rr = response
		itensRaw = rr.xpath('//a/text()').extract()
		print ('LEN : '+str(len(itensRaw)))
		itensOut = []
		outdir = './out'
		if not os.path.isdir(outdir):
			os.makedirs(outdir)
		for i in itensRaw:
			txt = htm2txt(i.encode('utf8'))
			print ("____> "+ txt)
			itensOut.append(txt)
			appendFile('out/DATA',txt)
		
		for i in range(len(itensOut)):
			pr_str = itensOut[i]
			PRSpider.CONT+=1
			#writeFile('out/DATA%d'%Spider1.CONT,pr_str)
			#appendFile('out/DATA',pr_str)
