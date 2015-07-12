__author__ = 'jkessel'

from bs4 import BeautifulSoup
import os
from urllib.error import HTTPError
import urllib.request

# Be sure to create the folder beforehand
output_folder = 'c:\\microsoft_books'

books_url = ('http://blogs.msdn.com/b/mssmallbiz/archive/2015/07/07/i-m-giving-away-millions-of-free-microsoft-ebooks-'
'again-including-windows-10-windows-8-1-windows-8-windows-7-office-2013-office-365-sharepoint-2013-dynamics-crm-'
'powershell-exchange-server-lync-2013-system-center-azure-clo.aspx')
request = urllib.request.urlopen(books_url)
page = request.read()

soup = BeautifulSoup(page, 'html.parser')

table = soup.find_all('table')[2]
paragraphs = table.find_all('p')

print('Starting download of books...')

i = 1

for paragraph in paragraphs:
    no_of_books = len(paragraphs)
    anchors = paragraph.find_all('a')
    print('Downloading book', i, 'of', no_of_books)
    for anchor in anchors:
        href = anchor.get('href')
#        print(href)
        try:
            download = urllib.request.urlopen(href)
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
