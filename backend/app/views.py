from glob import glob
import os
from os.path import join

from flask import render_template, send_from_directory
from app import app, db
from models import FSSChild
from config import basedir
import pdfkit

@app.route('/forms/<form_type>/<child_id>')
def generate_forms(form_type, child_id):
    temp_dir = join('static','temp')
    rpt_name = 'generated.pdf'
    rpt_path = join(basedir, 'app', temp_dir, rpt_name)

    sesh = db.session
    child = sesh.query(FSSChild).filter_by(id=child_id).first()
    child_photo = glob(join('app', 'static', 'photos', '*%d.*' % child.id))[0].split(os.sep)[-1]

    return render_template(form_type + '.html',
                               title=form_type,
                               child=child,
                               child_photo=child_photo,
                               get_initial_interaction=get_initial_interaction,
                               get_relation=get_relation)

    rpt_html = render_template(form_type + '.html',
                               title=form_type,
                               child=child,
                               child_photo=child_photo)

    pdfkit.from_string(rpt_html, rpt_path, options={'quiet':''})
    return send_from_directory(temp_dir, rpt_name, mimetype='application/pdf')

def get_initial_interaction(interactions):
    for interaction in interactions:
        if interaction.is_initial_interaction:
            return interaction

    return None

def get_relation(relations, relationship):
    for relation in relations:
        if relation.relationship == relationship:
            return relation

    return None
