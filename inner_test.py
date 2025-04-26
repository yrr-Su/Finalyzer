

from FinCrawler.builder import CrawlerBuilder
from config.setting import CONFIG




if __name__ == '__main__':
    rules = {
        '轉換價值': [60, 100],
        '轉換溢價率 (%)': 6,
    }
    output_path = CONFIG.OUTPUT

    builder = CrawlerBuilder(rules, output_path)
    builder.build()

