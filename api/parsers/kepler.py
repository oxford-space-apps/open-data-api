from flaskext.mongoalchemy import BaseQuery
import requests

from lxml import etree
import lxml.html
import urllib
import sys

def get_candidates():
	candidates_url = 'http://archive.stsci.edu/kepler/planet_candidates.html'
	html = lxml.html.parse(candidates_url)
	page = lxml.html.tostring(html, pretty_print=True, method="html")		

	return 'Nothing'

def find_all(string, occurrence):
     found = 0

     while True:
         found = string.find(occurrence, found)
         if found != -1:
             yield found
         else:
             break

         found += 1

