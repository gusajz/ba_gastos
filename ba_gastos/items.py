# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class BaGastosItem(Item):
    # define the fields for your item here like:
    # name = Field()
    contratacion = Field()
    actuacion = Field()
    rubro = Field()
    rubro_referencia = Field()
    fecha_apertura = Field()
    hora_apertura = Field()
    fecha_postergacion = Field()
    hora_postergacion = Field()
    solicitante = Field()
    licitante = Field()
    estado = Field()
    detalle = Field()
    lugar_apertura = Field()
    postergaciones_previas = Field()
    valor_pliego = Field()
    plazo_entrega = Field()
    circulares = Field()
    observaciones = Field()
    descripcion = Field()
