from lxml import etree
import lxml.html
import urllib
import sys



html = lxml.html.parse('http://grin.hq.nasa.gov/ABSTRACTS/GPN-2000-001310.html')
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


