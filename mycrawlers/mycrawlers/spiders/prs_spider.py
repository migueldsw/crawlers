import scrapy
from bs4 import BeautifulSoup as BS

def composePR(perguntas,respostas,index):
	return "P:\n%s\nR:\n%s" %(perguntas[index],respostas[index])


def writeFile(filename,content):
	f = open(filename,'w')
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
		for i in rawRespostas:
			respostas.append(htm2txt(i))
		
		for i in range(len(perguntas)):
			pr_str = composePR(perguntas,respostas,i)
			PRSpider.CONT+=1
			writeFile('out/PR%d'%PRSpider.CONT,pr_str)

		#print "THE DATA AMOUNT IS %d/%d !!!!!!!!!!" %(len(perguntas),len(respostas))