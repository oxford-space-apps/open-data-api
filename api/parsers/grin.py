from flaskext.mongoalchemy import BaseQuery
import requests
import json

from api import app
from api import db


from lxml import etree
import lxml.html
import urllib
import sys

class JSONField(db.StringField):
    def unwrap(self, value, *args, **kwargs):
        """Pass the json field around as a dictionary internally"""
        return json.loads(value)

class DatasetQuery(BaseQuery):
    def filter_by_center_code(self, center_code):
	results = self.filter(Grin.center_code == center_code)
	list1 = []
	for grin in results:
		dictionary = dict(internal_id = str(grin.mongo_id), 
				image_reference = grin.image_reference, 
				grin_id = grin.grin_id, 
				data_url = grin.data_url, 
				image_creator = grin.image_creator, 
				original_source = grin.original_source, 
				date_time = grin.date_stamp, 
				center_code = grin.center_code, 
				center_name = grin.center_name, 
				short_desc = grin.short_description, 
				full_desc = grin.full_description, 
				keywords = grin.keyword_list, 
				subjects = grin.subject_list, 
				thumbnail_url = grin.thumbnail_url, 
				thumbnail_type = grin.thumbnail_type,
				thumbnail_height = grin.thumbnail_height, 
				thumbnail_width = grin.thumbnail_width, 
				thumbnail_size = grin.thumbnail_size, 
				small_url = grin.small_url, 
				small_type = grin.small_type, 
				small_height = grin.small_height, 
				small_width = grin.small_width, 
				small_size = grin.small_size, 
				medium_url = grin.medium_url, 
				medium_type = grin.medium_type, 
				medium_height = grin.medium_height, 
				medium_width = grin.medium_width, 
				medium_size = grin.medium_size, 
				large_url = grin.large_url, 
				large_type = grin.large_type, 
				large_height = grin.large_height, 
				large_width = grin.large_width, 
				large_size = grin.large_size)
		list1.append(dictionary)

	return list1

    def filter_by_grin_id(self, grin_id):
	results = self.filter(Grin.grin_id == grin_id)
	list1 = []
	for grin in results:
                dictionary = dict(internal_id = str(grin.mongo_id),
                                image_reference = grin.image_reference,
                                grin_id = grin.grin_id,
                                data_url = grin.data_url,
                                image_creator = grin.image_creator,
                                original_source = grin.original_source,
                                date_time = grin.date_stamp,
                                center_code = grin.center_code,
                                center_name = grin.center_name,
                                short_desc = grin.short_description,
                                full_desc = grin.full_description,
                                keywords = grin.keyword_list,
                                subjects = grin.subject_list,
                                thumbnail_url = grin.thumbnail_url,
                                thumbnail_type = grin.thumbnail_type,
                                thumbnail_height = grin.thumbnail_height,
                                thumbnail_width = grin.thumbnail_width,
                                thumbnail_size = grin.thumbnail_size,
                                small_url = grin.small_url,
                                small_type = grin.small_type,
                                small_height = grin.small_height,
                                small_width = grin.small_width,
                                small_size = grin.small_size,
                                medium_url = grin.medium_url,
                                medium_type = grin.medium_type,
                                medium_height = grin.medium_height,
                                medium_width = grin.medium_width,
                                medium_size = grin.medium_size,
                                large_url = grin.large_url,
                                large_type = grin.large_type, 
                                large_height = grin.large_height, 
                                large_width = grin.large_width, 
                                large_size = grin.large_size)

		list1.append(dictionary)

	return list1

class Grin(db.Document):
    data_url = db.StringField()
    center_name = db.StringField()
    image_reference = db.StringField()
    date_stamp = db.StringField()
    short_description = db.StringField()
    full_description = db.StringField()
    keyword_list = db.AnythingField()
    subject_list = db.AnythingField()
    center_code = db.StringField()
    grin_id = db.StringField()
    image_creator = db.StringField()
    original_source = db.StringField()
    thumbnail_url = db.StringField()
    thumbnail_type = db.StringField()
    thumbnail_width = db.StringField()
    thumbnail_height = db.StringField()
    thumbnail_size = db.StringField()
    small_url = db.StringField()
    small_type = db.StringField()
    small_width = db.StringField()
    small_height = db.StringField()
    small_size = db.StringField()
    medium_url = db.StringField()
    medium_type = db.StringField()
    medium_width = db.StringField()
    medium_height = db.StringField()
    medium_size = db.StringField()
    large_url = db.StringField()
    large_type = db.StringField()
    large_width = db.StringField()
    large_height = db.StringField()
    large_size = db.StringField()
    data = JSONField()

    query_class = DatasetQuery


def find_all(string, occurrence):
     found = 0

     while True:
         found = string.find(occurrence, found)
         if found != -1:
             yield found
         else:
             break

         found += 1


def get_pages():
	center_list = ['AMES','DFRC','GRC','GSFC','HQ','JPL','JSC','KSC','LARC','MSFC','SSC']
	for center in center_list:
		html = lxml.html.parse('http://grin.hq.nasa.gov/BROWSE/' + center + '.html')
        	page = lxml.html.tostring(html, pretty_print=True, method="html")
		
		first_tag = list(find_all(page, '<a href="/ABSTRACTS/'))
		second_tag = list(find_all(page, '" accesskey="z"'))
		
		count = 0

		while count < len(first_tag):
			url = 'http://grin.hq.nasa.gov/ABSTRACTS/' + page[first_tag[count]+20:second_tag[count]]		
			get_a_page(url)
			count = count + 1
		
	return ''
   
def get_a_page(url):

	html = lxml.html.parse(url)
	page = lxml.html.tostring(html, pretty_print=True, method="html")

	startPos = page.find('NASA Center:')
	remaining = page[startPos+47:startPos+200]
	endPos = remaining.find('</td>')
	centerName = remaining[0:endPos]

	startPos = page.find(' : </font></th>')
	remaining = page[startPos+37:startPos+50]
	endPos = remaining.find('</td>')
	imageRef = remaining[0:endPos]

	startPos = page.find('DA:')
	dateTimestamp = page[startPos+3:startPos+10]

	startPos = page.find('<!-- ONE-LINE-DESCRIPTION-BEGIN -->')
	endPos = page.find('<!-- ONE-LINE-DESCRIPTION-END -->')
	shortDescription = page[startPos+35:endPos]

	startPos = page.find('<!-- DESCRIPTION-BEGIN -->')
	endPos = page.find('<!-- DESCRIPTION-END -->')
	description = page[startPos+27:endPos]

	startPos = page.find('<!-- KEYWORD-BEGIN -->')
	endPos = page.find('<!-- KEYWORD-END -->')
	keywords = page[startPos+22:endPos]
	keywordList = keywords.split()

	startPos = page.find('<!-- SUBJECT-BEGIN -->')
	endPos = page.find('<!-- SUBJECT-END -->')
	subjects = page[startPos+22:endPos]
	subjects.strip()
	subjectList = subjects.split(',')

	startPos = page.find('<!-- CENTER-BEGIN -->')
	endPos = page.find('<!-- CENTER-END -->')
	centerCode = page[startPos+21:endPos]
	centerCode = centerCode.strip()

	startPos = page.find('<!-- GRINNUMBER-BEGIN -->')
	endPos = page.find('<!-- GRINNUMBER-END -->')
	grinID = page[startPos+25:endPos]

	startPos = page.find('Creator/Photographer:')
	remaining = page[startPos+25:startPos+50]
	endPos = remaining.find('</li>')
	creator = remaining[0:endPos]
	creator = creator.strip()

	startPos = page.find('Original Source:')
	remaining = page[startPos+20:startPos+60]
	endPos = remaining.find('</li>')
	origSource = remaining[0:endPos]
	origSource = origSource.strip()

	startPos = page.find('<td id="r2" headers="c1"><a href="')
	remaining = page[startPos+34:startPos+200]
	endPos = remaining.find('">')
	thumbnailUrl = remaining[0:endPos]

	startPos = page.find('headers="c2 r2"')
	remaining = page[startPos+31:startPos+60]
	endPos = remaining.find('</td>')
	thumbnailType = remaining[0:endPos]
	thumbnailType = thumbnailType.strip()

	startPos = page.find('headers="c3 r2"')
	remaining = page[startPos+31:startPos+60]
	endPos = remaining.find('</td>')
	thumbnailWidth = remaining[0:endPos]
	thumbnailWidth = thumbnailWidth.strip()

	startPos = page.find('headers="c4 r2')
	remaining = page[startPos+31:startPos+60]
	endPos = remaining.find('</td>')
	thumbnailHeight = remaining[0:endPos]
	thumbnailHeight = thumbnailHeight.strip()

	startPos = page.find('headers="c5 r2"')
	remaining = page[startPos+30:startPos+60]
	endPos = remaining.find('</td>')
	thumbnailSize = remaining[0:endPos]
	thumbnailSize = thumbnailSize.strip()



	startPos = page.find('<td id="r3" headers="c1"><a href="')
	remaining = page[startPos+34:startPos+200]
	endPos = remaining.find('">')
	smallUrl = remaining[0:endPos]

	startPos = page.find('headers="c2 r3"')
	remaining = page[startPos+31:startPos+60]
	endPos = remaining.find('</td>')
	smallType = remaining[0:endPos]
	smallType = smallType.strip()

	startPos = page.find('headers="c3 r3"')
	remaining = page[startPos+31:startPos+60]
	endPos = remaining.find('</td>')	
	smallWidth = remaining[0:endPos]
	smallWidth = smallWidth.strip()

	startPos = page.find('headers="c4 r3"')
	remaining = page[startPos+31:startPos+60]
	endPos = remaining.find('</td>')
	smallHeight = remaining[0:endPos]
	smallHeight = smallHeight.strip()

	startPos = page.find('headers="c5 r3"')
	remaining = page[startPos+30:startPos+60]
	endPos = remaining.find('</td>')
	smallSize = remaining[0:endPos]
	smallSize = smallSize.strip()


	startPos = page.find('<td headers="c1" id="r4"><a href="')
	remaining = page[startPos+34:startPos+200]
	restOfRow3 = page[startPos+31:startPos+5000]
	endPos = remaining.find('">')
	mediumUrl = remaining[0:endPos]


	startPos = restOfRow3.find('headers="c2 r3"')
	remaining = restOfRow3[startPos+31:startPos+60]
	endPos = remaining.find('</td>')
	mediumType = remaining[0:endPos]
	mediumType = mediumType.strip()


	startPos = restOfRow3.find('headers="c3 r3"')
	remaining = restOfRow3[startPos+31:startPos+60]
	endPos = remaining.find('</td>')
	mediumWidth = remaining[0:endPos]
	mediumWidth = mediumWidth.strip()

	startPos = restOfRow3.find('headers="c4 r3"')
	remaining = restOfRow3[startPos+31:startPos+60]
	endPos = remaining.find('</td>')
	mediumHeight = remaining[0:endPos]
	mediumHeight = mediumHeight.strip()

	startPos = restOfRow3.find('headers="c5 r3"')
	remaining = restOfRow3[startPos+30:startPos+60]
	endPos = remaining.find('</td>')
	mediumSize = remaining[0:endPos]
	mediumSize = mediumSize.strip()


	startPos = page.find('<td id="r5" headers="c1"><a href="')
	remaining = page[startPos+34:startPos+200]
	restOfRow4 = page[startPos+31:startPos+5000]
	endPos = remaining.find('">')
	largeUrl = remaining[0:endPos]


	startPos = restOfRow4.find('headers="c2 r3"')
	remaining = restOfRow4[startPos+31:startPos+60]
	endPos = remaining.find('</td>')
	largeType = remaining[0:endPos]
	largeType = largeType.strip()

	startPos = restOfRow4.find('headers="c3 r3"')
	remaining = restOfRow4[startPos+31:startPos+60]
	endPos = remaining.find('</td>')
	largeWidth = remaining[0:endPos]
	largeWidth = largeWidth.strip()

	startPos = restOfRow4.find('headers="c4 r3"')
	remaining = restOfRow4[startPos+31:startPos+60]
	endPos = remaining.find('</td>')
	largeHeight = remaining[0:endPos]
	largeHeight = largeHeight.strip()
	

	startPos = restOfRow4.find('headers="c5 r3"')
	remaining = restOfRow4[startPos+30:startPos+60]
	endPos = remaining.find('</td>')
	largeSize = remaining[0:endPos]
	largeSize = largeSize.strip()


	dataset = Grin(data_url = url, center_name = centerName, image_reference = imageRef, date_stamp = dateTimestamp, short_description = shortDescription, full_description = description, keyword_list = keywordList, subject_list = subjectList, center_code = centerCode, grin_id = grinID, image_creator = creator, original_source = origSource, thumbnail_url = thumbnailUrl, thumbnail_type = thumbnailType, thumbnail_width = thumbnailWidth, thumbnail_height = thumbnailHeight, thumbnail_size = thumbnailSize, small_url = smallUrl, small_type = smallType, small_width = smallWidth, small_height = smallHeight, small_size = smallSize, medium_url = mediumUrl, medium_type = mediumType, medium_width = mediumWidth, medium_height = mediumHeight, medium_size = mediumSize, large_url = largeUrl, large_type = largeType, large_width = largeWidth, large_height = largeHeight, large_size = largeSize)
	dataset.save();
