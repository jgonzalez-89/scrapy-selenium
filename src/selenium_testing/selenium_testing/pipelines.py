# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TransformDataPipeline:
    def process_item(self, item, spider):
        transformed_product = {
            "EAN": item["EAN"],
            "GSI": item["GSI"],
            "nombre": item["nombre"],
            "distribuidor": item["distribuidor"],
            "precio": item["precio"],
            "ASIN": item["ASIN"],
            "imagen": item["imagen"],
            "relevancia": item["relevancia"],
        }

        return transformed_product