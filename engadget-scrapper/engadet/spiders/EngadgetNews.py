# -*- coding: utf-8 -*-
import scrapy
import json
import requests
from bs4 import BeautifulSoup


class EngadgetnewsSpider(scrapy.Spider):
    name = 'EngadgetNews'

    def get_total_aricles(self):
        url = "https://www.spot.im/api/init/spot/sp_f76RE06N"
        response = requests.get(url)
        return json.loads(response.text)["newsfeed"]["total_items"]

    def get_articles_for_page(self, page):
        base_url = "https://www.engadget.com/all/page/"
        return f"{base_url}{page}"

    def get_absolute_article_url(self, url):
        base_url = "https://www.engadget.com"
        return f"{base_url}{url}"

    def clean_output_file(self):
        open('articles.json', 'w').close()

    def get_article_urls_for_page(self, page):
        response = requests.get(self.get_articles_for_page(page))
        html = response.text
        parsed_html = BeautifulSoup(html, 'html.parser')
        links = parsed_html.body.select('.o-hit__link', href=True)
        urls = []
        for link in links:
            urls.append(link['href'])
        return {
            'total_articles': len(links),
            'urls': urls,
        }

    def extract_text(self, response):
        return " ".join(response.css('.article-text > p *::text').getall())

    def start_requests(self):
        self.clean_output_file()
        total_articles = self.get_total_aricles()
        processed_articles = 0
        current_page = 0
        while processed_articles < total_articles:
            articles = self.get_article_urls_for_page(current_page)
            current_page += 1
            processed_articles += articles['total_articles']
            for url in articles['urls']:
                yield scrapy.Request(url=self.get_absolute_article_url(url),
                                     callback=self.parse)

    def parse(self, response):
        yield {
            'text': self.extract_text(response)
        }
