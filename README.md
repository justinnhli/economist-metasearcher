# economist-metasearcher
A script to find Economist articles based on keywords.

The Function GetLinks() will take the search terms out of "textfile.txt" and create a list of links to be searched by the scraper.

The spider is defined in EconomistSpider, and the scrapy API commands:  process.crawl(EconomistSpider) and process.start() are used to run it. 

The settings to alter the outputs of the spider are avaliable in the CrawlerProcess settings.

The function Duplicates() goes into the Output file and creates a new dile based upon articles that appear more than once across the search.

IndividualSearches() is used to create a file containing the ranked results for each searh term
