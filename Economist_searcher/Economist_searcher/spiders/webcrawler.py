import scrapy

## text file open
import os
import csv
from collections import Counter
import pandas as pd

path = os.getcwd()
path = path + "/textfile.txt"
my_file = open(path)  # opens textfile for keyword retrival

all_the_lines = my_file.readlines()

items = []

for i in all_the_lines:
    items.append(i)
print(items)

new_items = [x[:-1] for x in items]
print(new_items)
# print text file

urls = []
for item in new_items:
    urls.append('https://www.economist.com/search?q=' + item);  # creates URLs by adding keywords to search link

print urls

search_matrix = []

for i in range(len(new_items)):
    search_matrix.append([])  # creates a search matrix for use later in ordering csv output by term

print(search_matrix)


# position = new_items.index("bubble")
# search_matrix[position].append("hello")


class EconomistSpider(scrapy.Spider):
    name = "economist"
    start_urls = urls

    def parse(self, response):
        substring = '&page'
        # page = item
        page = response.url.split('=')[1]
        for result in response.css('ol.layout-search-results li'):
            if substring in page:
                page = page.replace('&page', '')
            yield {
                'Link': result.css('li a.search-result::attr(href)').get(),
                'title': result.css('span.search-result__headline::text').get(),  # yields for info requested
                'word': page
            }

        next_page = 'https://www.economist.com/search' + response.css('li.ds-pagination__nav--next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)  # follows to the next page of that search term

        entries = []
        duplicate_entries = []
        unique_duplicates = []

        with open('output.csv', 'r') as my_file:
            for line in my_file:
                columns = line.strip().split(',')
                if columns[1] not in entries:
                    entries.append(columns[1])  # populates entries and duplicates arrays
                else:
                    duplicate_entries.append(columns[1])

        if len(duplicate_entries) > 0:
            with open('duplicates.csv', 'w') as out_file:
                with open('output.csv', 'r') as my_file:
                    for line in my_file:
                        columns = line.strip().split(',')
                        if (columns[1] in duplicate_entries) and (columns[1] not in unique_duplicates): #adds duplicate items to file, Output items are put into file by pipleine
                            unique_duplicates.append(columns[1])                            #^ stops same one from going in but ommits same link diff search
                            print line.strip()
                            out_file.write(line)


        for item in new_items:
            with open('output.csv', 'r') as my_file:  # puts search terms into nested array list by term name
                for line in my_file:
                    columns = line.strip().split(',')
                    if columns[0] == item:
                        position = new_items.index(str(
                            item))  # the index of the searh item which cooresponds to the search matrix index for each term
                        search_matrix[position].append(columns[0])

        for items in new_items:
            if len(search_matrix) > 0:
                name = items + ".csv"
                with open(name, 'w') as out_file:
                    with open('output.csv', 'r') as my_file:
                        for line in my_file:
                            columns = line.strip().split(',')
                            if columns[0] in search_matrix[new_items.index(items)]:
                                print line.strip()
                                out_file.write(line)





        #with open('duplicates.csv', 'r') as my_file:
            #c = Counter(row[1] for row in csv.reader(my_file))

        #df = pd.read_csv("duplicates.csv")
        #df["new_column"] = c[1]
        #df.to_csv("sample.csv", index=False)

# response.css('a.search-result::attr(href)').getall()


# response.css('a.search-result::attr(href)').getall()

# response.css('ol.layout-search-results li')
