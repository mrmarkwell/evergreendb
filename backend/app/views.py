from flask import render_template, send_from_directory
from app import app
from config import basedir
import pdfkit
from os.path import join

@app.route('/forms/<form_type>')
def generate_forms(form_type):
    temp_dir = join('static','temp')
    rpt_name = 'generated.pdf'
    rpt_path = join(basedir, 'app', temp_dir, rpt_name)

    rpt_html = render_template('form_common.html', title=form_type)
    pdfkit.from_string(rpt_html, rpt_path, options={'quiet':''})
    return send_from_directory(temp_dir, rpt_name, mimetype='application/pdf')
