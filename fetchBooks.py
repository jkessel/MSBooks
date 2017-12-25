__author__ = 'jkessel'

from bs4 import BeautifulSoup
import os
from urllib.error import HTTPError
import urllib.request

# Be sure to create the folder beforehand
output_folder = 'd:\\microsoft_books_new'

try:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

except OSError as ose:
    print('OSError: {0}'.format(ose))


"""
books_url = ('http://blogs.msdn.com/b/mssmallbiz/archive/2015/07/07/i-m-giving-away-millions-of-free-microsoft-ebooks-'
             'again-including-windows-10-windows-8-1-windows-8-windows-7-office-2013-office-365-sharepoint-2013-'
             'dynamics-crm-powershell-exchange-server-lync-2013-system-center-azure-clo.aspx')
books_url = ('https://blogs.msdn.microsoft.com/mssmallbiz/2016/07/10/free-thats-right-im-giving-away-millions-of-free-'
             'microsoft-ebooks-again-including-windows-10-office-365-office-2016-power-bi-azure-windows-8-1-office-2013'
             '-sharepoint-2016-sha/')
"""

books_url = ('https://blogs.msdn.microsoft.com/mssmallbiz/2017/07/11/largest-free-microsoft-ebook-giveaway-im-giving-'
             'away-millions-of-free-microsoft-ebooks-again-including-windows-10-office-365-office-2016-power-bi-azure-'
             'windows-8-1-office-2013-sharepo/')

request = urllib.request.urlopen(books_url)
page = request.read()

soup = BeautifulSoup(page, 'html.parser')

#table = soup.find_all('table')[2]
table = soup.find_all('table')[0]

# paragraphs = table.find_all('p')
rows = table.find_all('tr')

print('Starting download of books...')

i = 1

# TODO: Check recursion (double for blocks)
for row in rows:
    # no_of_books = len(rows)
    anchors = row.find_all('a')
    no_of_books = len(anchors)
    for anchor in anchors:
        print('Downloading book', i, 'of', no_of_books)
        href = anchor.get('href')
#        print(href)
        try:
            download = urllib.request.urlopen(href)
            content_length = download.info()['Content-Length']
            print('Filesize:', content_length)
        except HTTPError as err:
            print('HTTP Error: {0}'.format(err))

        url = download.geturl()
        filename = url.rsplit('/', 1)
        converted_filename = urllib.parse.unquote_plus(filename[1])
        if not os.path.isfile(output_folder + '\\' + converted_filename):
            try:
                file = open(output_folder + '\\' + converted_filename, mode='wb')
                print('     Downloading file', converted_filename, '...')
                file.write(download.read())
                file.close()
            except OSError as err:
                print('OS Error: {0}'.format(err))
        else:
            print('     File', converted_filename, 'already downloaded')
        i += 1

print('Finished!')
