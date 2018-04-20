# encoding=utf8
import urllib2
from google import google
import csv
import re
import urllib
import sys
import html2text
# Переменные
REGULAR_EXPRESSION_FOR_PHONE = r'([\+^ ]*(7|8)[ ]*[\( ]?\d+?[\) ][\d -]+)'
COMPANY = 'company.csv'
COMPANY_WITH_PHONE = "company_with_phone.csv"

with open(COMPANY, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='\t')
    for row in spamreader:
        search_results = google.search("contacts " + row[0].decode('utf-8'), 1)
        for result in search_results:
            print(result.link)
            try:
                try:
                    response = urllib2.urlopen(result.link)
                except urllib2.HTTPError, e:
                    continue
                except urllib2.URLError, e:
                    continue
                data = response.read()
                text = html2text.html2text(data.decode('utf-8'))
                if re.search(REGULAR_EXPRESSION_FOR_PHONE, text):
                    phones = re.findall(REGULAR_EXPRESSION_FOR_PHONE, text)
                    with open(COMPANY_WITH_PHONE, "a") as myfile:
                        phoneline = '\t'.join(''.join(elems) for elems in phones)
                        lines = row[0].decode('utf-8') + "\t" + phoneline.decode('utf-8') + "\n"
                        print(lines)
                        myfile.write(lines.encode('utf-8'))
                    break
            except ValueError:
                continue
