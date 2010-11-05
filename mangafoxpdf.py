from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import pycurl, re, urllib2

MANGA_URL = "http://www.mangafox.com/manga/miman_renai/v01/c001/"
PDF_NAME  = "miman_renai_v01c001"

# Sorry is set if detected in the source
# this means that all html pages have been gotten
global sorry, i, c, width, height
sorry = False

def on_receive(data):
	global sorry, width, height, c
	matches = re.compile('(http.+mfcdn.+jpg)').findall(data)
	sor = re.compile('Sorry, the').findall(data)
	
	# So if there was an image to download then this is true
	if len(matches) > 0 :
		print matches[0]
		u = urllib2.urlopen(matches[0])
		localfile = open(str(i) + ".jpg", 'w')
		localfile.write(u.read())
		localfile.close()

		# Add to the pdf file
		c.drawInlineImage(str(i) + ".jpg", 0, 0, width, height)
		c.showPage()

	# If sorry was matched then stop the download
	# iteration.
	if (len(sor) > 0):
		sorry = True 

# Open pdf to write. give it a name
c = canvas.Canvas(PDF_NAME + ".pdf", pagesize=A4)
width, height = A4

# Download the html. assumes html files are numbered in order.
for i in range(1,100):

	conn = pycurl.Curl()
	conn.setopt(pycurl.URL, MANGA_URL + str(i) + ".html")
	conn.setopt(pycurl.WRITEFUNCTION, on_receive)
	conn.perform()

	if sorry:
		break

# Write out the pdf
c.save()
