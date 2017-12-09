#!/home/richard/proj/evergreendb/backend/venv/bin/python
import pdfkit

# Requires: sudo apt-get install wkhtmltopdf
#   Or for Windows installing https://wkhtmltopdf.org/downloads.html (MinGW worked for me) and adding to path
html_str = '<html><h1>Testing is the Best thing</h1></html>'
dest = 'C:\\Users\\rclermon\\Documents\\Docs\\Other\\test.pdf'
pdfkit.from_string(html_str, dest, options={'quiet':''})
