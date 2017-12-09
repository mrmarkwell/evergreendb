from flask import render_template
from app import app

@app.route('/forms/<form_type>')
def generate_forms(form_type):
    return render_template('form_common.html', title=form_type)
