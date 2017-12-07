#!/home/richard/proj/evergreendb/backend/venv/bin/python
import pdfkit

# Requires: sudo apt-get install wkhtmltopdf

pdfkit.from_file('/home/richard/tmp/test.html', '/home/richard/tmp/example.pdf', options={'quiet':''})
