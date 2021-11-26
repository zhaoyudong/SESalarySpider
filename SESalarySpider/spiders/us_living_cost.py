import scrapy
import csv
import os


class UsLivingCostSpider(scrapy.Spider):
    name = 'us_living_cost'
    allowed_domains = ['https://www.numbeo.com/']
    start_urls = ['https://www.numbeo.com/cost-of-living/country_result.jsp?country=United+States']

    def parse(self, response):
        table = response.xpath('//table[@id="t2"]')
        theads = table.xpath('thead//tr//th//text()')
        header = self.extract_header(theads)
        trows = table.xpath('tbody//tr')
        rows = self.extract_tbody(trows)
        self.write_2_csv(header, rows)

    def write_2_csv(self, header, rows):
        if not os.path.exists('outputs'):
            os.mkdir('outputs')
        with open('outputs/us_living_cost.csv', 'wt') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(rows)

    def extract_header(self, theads):
        header = []
        for h in theads:
            header.append(h.extract())
        return header

    def extract_tbody(self, trows):
        rows = []
        index = 1
        for tr in trows:
            row = [index]
            tds = tr.xpath('td//text()')
            for td in tds:
                row.append(td.extract())
            rows.append(row)
            index += 1
        return rows
