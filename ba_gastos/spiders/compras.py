# encoding=utf-8

from scrapy.spider import BaseSpider
from scrapy import log
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from ba_gastos.items import BaGastosItem
import urlparse


def first_or_empty(l):
    return l
    #return l[0] if l else ''

class ComprasSpider(BaseSpider):
    name = "compras"
    allowed_domains = ["www.buenosaires.gob.ar"]
    start_urls = (
        'http://www.buenosaires.gob.ar/areas/hacienda/compras/consulta/popup_consulta.php?cfilas=10&orden_tipo=desc&tipocontratacion=-&numcontratacion=N%FAmero&siglacontratacion=-&aniocontratacion=2013&tipoactuacion=-&numactuacion=N%FAmero&siglaactuacion=-&anioactuacion=-&idrubro=-&idrlicitante=-&idrsolicitante=-&idestado=6&siglaactuacion=-&anulado=f&rlidep=1&rsoldep=1&f_dia_desde=-&f_mes_desde=-&f_anio_desde=-&f_dia_hasta=-&f_mes_hasta=-&f_anio_hasta=-&r_fecha=todos',
        )

    def parse(self, response):
        try:
            hxs = HtmlXPathSelector(response)
            rows =   hxs.select('//table[@summary="Tabla"]/tbody/tr')
            if not rows:
                self.log("ERROR! Failed to extract results table from response for URL '{:s}'. Has 'summary' changed?".format(response.request.url), level=log.ERROR)
                return
            for row in rows:
                item = BaGastosItem()

                cells = row.select('td')
                

                # Actually, all of this information is already in details, so I take it from there.                
                item['contratacion'] = cells[0].select('span/text()').extract()
                item['actuacion'] = cells[1].select('span/text()').extract()
                item['rubro'] = cells[2].select('span/text()').extract()
                item['fecha_apertura'] = cells[3].select('span/text()').extract()
                item['solicitante'] = cells[4].select('span/text()').extract()
                item['licitante'] = cells[5].select('span/text()').extract()
                item['estado'] = cells[6].select('span/text()').extract()
                
                detalle = cells[7].select('span/a/@href').extract()
                detalle_url = urlparse.urljoin(response.url, detalle[0]) 
                                
                yield Request(url=detalle_url, callback=self.parse_details)                
                #yield item#Request(url=record_href, callback=self.parse_details)
                
                
        except Exception as e:
            # Something went wrong parsing this page. Log URL so we can determine which one.
            self.log("Parsing failed for URL '{:s}'".format(response.request.url), level=log.ERROR)
            raise # Re-raise exception
    
        
    def parse_details(self, response):
        try:
            hxs = HtmlXPathSelector(response)
            rows = hxs.select('//div[@class="popup contenido"]/table/tr[2]/td/table/tr/td[2]')
                    
            if not rows:
                self.log("ERROR parse details")
#                self.log("ERROR! Failed to extract results table from response for URL '{:s}'. Has 'summary' changed?".format(response.request.url), level=log.ERROR)
                return

            item = BaGastosItem()

            self.log("\n\n\n\n%s\n\n\n" % rows[0].select('text()').extract() )
            
            item['contratacion'] = first_or_empty( rows[0].select('text()').extract() )
            item['actuacion'] = first_or_empty( rows[1].select('text()').extract() )
            item['rubro'] = first_or_empty(  rows[2].select('text()').extract() )
            item['descripcion'] = first_or_empty(  rows[3].select('text()').extract() )
            item['licitante'] = first_or_empty( rows[4].select('text()').extract() )
            item['solicitante'] = first_or_empty( rows[5].select('text()').extract() )
            item['rubro_referencia'] = first_or_empty( rows[6].select('text()').extract() )
            item['fecha_apertura'] = first_or_empty( rows[7].select('text()').extract() )
            item['hora_apertura'] = first_or_empty( rows[8].select('text()').extract() )
            item['fecha_postergacion'] = first_or_empty( rows[9].select('text()').extract() )
            item['hora_postergacion'] = first_or_empty( rows[10].select('text()').extract() )
            item['lugar_apertura'] = first_or_empty( rows[11].select('text()').extract() )
            item['postergaciones_previas'] = first_or_empty( rows[12].select('text()').extract() )
            item['valor_pliego'] = first_or_empty( rows[13].select('text()').extract() )
            item['plazo_entrega'] = first_or_empty( rows[12].select('text()').extract() )
#                Pliego adjunto. item['plazo_entrega'] = first_or_empty( rows[13].select('text()').extract()
            item['circulares'] = first_or_empty( rows[14].select('text()').extract() )
            item['observaciones'] = first_or_empty( rows[15].select('text()').extract() )


#           TODO: 
#                 continue through pagination
#                 download licitación and adjudicación documents
            yield item                
                
                
        except Exception as e:
            # Something went wrong parsing this page. Log URL so we can determine which one.
            self.log("Parsing failed for URL '{:s}'".format(response.request.url), level=log.ERROR)
            raise # Re-raise exception

        