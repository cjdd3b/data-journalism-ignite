import urllib2
from BeautifulSoup import BeautifulSoup

# First find and open the URL we're trying to scrape
url = 'http://www.ire.org/conferences/nicar-2012/schedule/'
html = urllib2.urlopen(url).read()

# Open an output file to put our scraper results
outfile = open('handson_2012.txt', 'a')

# Now use BeautifulSoup to extract the course list from the schedule page.
# We're going to start by putting each of the daily scheudle tabs on the
# page into a list, so we can loop over them one at a time.
# More documentation on Beautiful Soup can be found here: http://www.crummy.com/software/BeautifulSoup/bs4/doc/
soup = BeautifulSoup(html)
pane_uls = soup.findAll("ul", "listview pane")

# Loop through each of the panes ...
for pane in pane_uls:

    # And then loop through each schedule item in each pane.
    for li in pane.findAll('li'):

        # If that schedule item is a hands-on class ...
        if li.find('div', "col-10 heading5").text == 'Hands-on':

            # Write the text title of that item to the output file.
            outfile.write(li.find('h3').text + '\n')