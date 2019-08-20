import urllib
import requests
import re, os, argparse
import HTMLParser

parser = argparse.ArgumentParser(description="Helper script for automatically donwloading Harry Potter audiobooks from https://hpaudiobooks.club")
parser.add_argument(
    '--book',
    type=int,
    help='Release number of book. E.g. for sorcerer\'s stone, enter 1 and for chamber of secrets, enter 2'
)
FLAGS, unparsed = parser.parse_known_args()

class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

def list_has_duplicates(lst):
    return len(lst) != len(set(lst))



book_no = FLAGS.book
mopen = MyOpener()

base_url = ""
if book_no == 1:
    base_url = "https://hpaudiobooks.club/philosopher-stone-audiobook-stephen-fry/"
elif book_no == 2:
    base_url = "https://hpaudiobooks.club/chamber-secrets-audiobook-stephen-fry/"
elif book_no == 3:
    base_url = "https://hpaudiobooks.club/prisoner-of-azkaban-audiobook-stephen-fry/"
elif book_no == 4:
    base_url = "https://hpaudiobooks.club/goblet-of-fire-audiobook-stephen-fry/"
elif book_no == 5:
    base_url = "https://hpaudiobooks.club/order-of-the-phoenix-audiobook-stephen-fry/"
elif book_no == 6:
    base_url = "https://hpaudiobooks.club/half-blood-prince-audiobook-stephen-fry/"
elif book_no == 7:
    base_url = "https://hpaudiobooks.club/deathly-hallows-audiobook-stephen-fry/"

should_continue_crawling = True
page_count = 1
download_links = []
while should_continue_crawling:
    link = base_url + str(page_count) + "/"
    print("DOWNLOADING FROM\n{}".format(link))

    myfile = str(mopen.open(link).read())



    matches = re.findall(r'((https?|ftp|gopher|telnet|file|notes|ms-help):((\/)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*\.mp3\?_=[0-9])', myfile)
    download_links.extend([m[0] for m in matches])

    if list_has_duplicates(download_links):
        del download_links[len(download_links)-len(matches):]
        should_continue_crawling = False

    page_count += 1
print("Found {} Chapters".format(len(download_links)))

# Create directory to save download
dirname = "Book " + str(book_no)
if not os.path.exists(dirname):
    os.mkdir(dirname)
    print("Directory " , dirname ,  " Created ")
else:
    print("Directory " , dirname ,  " already exists")

for dl in download_links:
    dl = HTMLParser.HTMLParser().unescape(dl)
    print dl
    r = requests.get(dl, allow_redirects=True)
    open(dirname + "/" + dl.rsplit('/', 1)[1][:-4].replace("%20", "_"), 'wb').write(r.content)
