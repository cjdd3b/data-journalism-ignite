'''
This script builds histograms counting mentions of various query terms
on the NICAR-L listserv from 1994 to 2012. More info on the list here:
http://www.ire.org/resource-center/listservs/subscribe-nicar-l/ 
'''

import re
import urllib, urllib2
import matplotlib.pyplot as plt
from collections import defaultdict
from BeautifulSoup import BeautifulSoup

########## GLOBALS ##########

QUERY = '"Cold fusion"' # Change this to query for different things

########## MAIN ##########

# Set up initial URL and web query
url = 'http://lists.reporter.org/ire_bin/namazu.cgi?'
params = {
    'query': QUERY,
    'submit': 'Search!',
    'idxname': 'NICAR-L',
    'max': '100',
    'result': 'normal',
    'sort': '',
}

# Open the first page into BeautifulSoup
html = urllib2.urlopen(url + urllib.urlencode(params)).read()
soup = BeautifulSoup(html)

# Ultimately we're going to save the HTML for every page in the result set
# to a list called toparse. First we'll add the initial page of results.
toparse = []
toparse.append(html)

# Loop through result pages, if any, and add their html to toparse
for p in [a['href'] for a in soup.find("div", "namazu-result-footer").findAll('a') if re.match(r'^\[', a.text)]:
    html = urllib2.urlopen('http://lists.reporter.org' + p).read()
    toparse.append(html)

# Now loop through the HTML for those pages and append message years to a list called data
data = []
for doc in toparse:
    docsoup = BeautifulSoup(doc)
    dl = docsoup.find("dl")
    for dd in dl.findAll('dd') : # Loop through each result
        if re.match(r'^Date.*', dd.text): # Find the date line
            try:
                year = re.findall(r'\s\d{4}\s', dd.text)[0].strip() # Parse out the year
                data.append(int(year)) # Append it to the data list
            except IndexError: # Skip if no date returned for some reason
                pass

# Finally, build a histogram based on the year counts
N = 16
n, bins, patches  = plt.hist(data, N, range=[1994, 2012])
plt.title('%s mentions on NICAR-L' % QUERY)
plt.xlabel('Year')
plt.ylabel('Count')
plt.show()