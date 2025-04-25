

from FinCrawler.builder import CrawlerBuilder
from config.setting import CONFIG




if __name__ == '__main__':
    rules = {

    }
    output_path = CONFIG.OUTPUT

    builder = CrawlerBuilder(rules, output_path)
    builder.build()

