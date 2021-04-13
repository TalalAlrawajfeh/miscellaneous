import os
import time
import urllib.request as request
from bs4 import BeautifulSoup

RETRY_DELAY = 4

OUTPUT_DIRECTORY = 'out'

URL = 'http://www.earlymoderntexts.com/assets/pdfs/'


def main():
    req = request.urlopen(URL)
    soup = BeautifulSoup(req.read(), 'html.parser')
    req.close()

    links = soup.find_all('a')
    refs = [(a['href'], URL + a['href']) for a in links if a['href'].endswith('.pdf')]
    os.makedirs(os.path.join(os.curdir, OUTPUT_DIRECTORY))

    for ref in refs:
        download_file(ref)

    print("Done!")


def download_file(ref):
    file_path = os.path.join(os.curdir, OUTPUT_DIRECTORY, ref[0])
    request.urlretrieve(ref[1], file_path)
    while not os.path.isfile(file_path):
        time.sleep(RETRY_DELAY)
        request.urlretrieve(ref[1], file_path)


if __name__ == '__main__':
    main()
