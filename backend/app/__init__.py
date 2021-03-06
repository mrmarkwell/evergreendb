from flask import Flask, current_app, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_login import LoginManager
from flask_admin import Admin
from flask_login import current_user

app = Flask(__name__, static_url_path='/static')
app.config.from_object('config')
db = SQLAlchemy(app)
rest_api = Api(app)
login_manager = LoginManager(app)
admin = Admin(app, name='evergreendb', template_mode='bootstrap3')

from api.resources import QueryResource
from api.resources import EntityResource
from api.resources import EntityListResource
from api.resources import FilterResource
from api.resources import HeartbeatResource
from api.resources import VersionResource
from api.resources import AuthCheckResource
from api.resources import AdminAuthCheckResource
from api.resources import RollbackResource
from api.upload import Upload
from api.upload import Photos
from api.resources import UserResource
from api.resources import ReminderResource
from api.resources import EnumResource
from api.resources import ReportResource
from api.upload import InteractionFiles, MedicalFiles


@app.route('/photos/<path:path>')
def send_photo(path):
    return send_from_directory('photos', path)


# Add REST API endpoints
rest_api.add_resource(QueryResource, "/query", endpoint="query")
rest_api.add_resource(EntityResource, "/entity/<string:entity_name>", endpoint="entity")
rest_api.add_resource(FilterResource, "/filter")
rest_api.add_resource(EntityListResource, "/entity", endpoint="entities")
rest_api.add_resource(HeartbeatResource, "/heartbeat", endpoint="heartbeat")
rest_api.add_resource(VersionResource, "/version", endpoint="version")
rest_api.add_resource(RollbackResource, "/rollback", endpoint="rollback")
rest_api.add_resource(Upload, "/upload")
rest_api.add_resource(Photos, "/photos/<string:filename>", endpoint="photos")
rest_api.add_resource(UserResource, "/user")
rest_api.add_resource(EnumResource, "/enum/<string:enum_name>", endpoint="enum")
rest_api.add_resource(ReminderResource, "/reminder", endpoint="reminder")
rest_api.add_resource(InteractionFiles, "/interactionfiles/<string:id>", endpoint="interactionsfiles")
rest_api.add_resource(MedicalFiles, "/medicalfiles/<string:id>", endpoint="medicalfiles")
rest_api.add_resource(AuthCheckResource, "/authcheck", endpoint="authcheck")
rest_api.add_resource(AdminAuthCheckResource, "/adminauthcheck", endpoint="adminauthcheck")
rest_api.add_resource(ReportResource, "/reports/<string:format_name>", endpoint="reports")

from datetime import date
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin.model import typefmt
from api.marshallers import *
from models import Child, Partner, Caregiver, Specialist, SpecialistType
from models import MilestoneTypeCategory, MilestoneType, Doctor, DoctorType
from models import MeasurementType, Camp, MedicalCondition, Medication
from wtforms.fields import SelectField


#sex_select_field = SelectField('sex', choices=[('M', 'Male'), ('F',
#'Female')])
def date_format(view, value):
    return value.strftime(DATE_FMT)

MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
        type(None): typefmt.null_formatter,
        date: date_format
    })

class MyBaseView(ModelView):
    column_type_formatters = MY_DEFAULT_FORMATTERS
    can_export = True
    can_view_details = True

    def is_accessible(self):
        return current_app.config.get("LOGIN_DISABLED") or (current_user.is_authenticated and current_user.is_admin)

class ChildView(MyBaseView):
    column_exclude_list = ['medical_history', 'child_history','program_departure_reason']
    fields = child_fields.keys()
    fields.remove('id')
    form_columns = fields
    column_searchable_list = ['child_english_name']

    # Couldn't figure out how to get this one to work.
    #form_overrides = dict(sex=SelectField)
class DoctorView(MyBaseView):
    fields = doctor_fields.keys()
    fields.remove('id')
    fields.remove('doctor_type_id')
    fields.append('doctor_type')
    form_columns = fields

class PartnerView(MyBaseView):
    fields = partner_fields.keys()
    column_exclude_list = ['address', 'phone']
    fields.remove('id')
    form_columns = fields

class CaregiverView(MyBaseView):
    fields = caregiver_fields.keys()
    fields.remove('id')
    form_columns = fields

class SpecialistView(MyBaseView):
    fields = specialist_fields.keys()
    fields.remove('id')
    fields.remove('specialist_type_id')
    fields.append('specialist_type')
    form_columns = fields

class SpecialistTypeView(MyBaseView):
    fields = specialist_type_fields.keys()
    fields.remove('id')
    form_columns = fields

class MilestoneTypeCategoryView(MyBaseView):
    fields = milestone_type_category_fields.keys()
    fields.remove('id')
    form_columns = fields

class MilestoneTypeView(MyBaseView):
    fields = milestone_type_fields.keys()
    fields.remove('id')
    fields.remove('milestone_type_category_id')
    fields.append('milestone_type_category')
    form_columns = fields

class MeasurementTypeView(MyBaseView):
    fields = measurement_type_fields.keys()
    fields.remove('id')
    form_columns = fields

class CampView(MyBaseView):
    fields = camp_fields.keys()
    fields.remove('id')
    form_columns = fields

class MedicalConditionView(MyBaseView):
    fields = medical_condition_fields.keys()
    fields.remove('id')
    form_columns = fields

class MedicationView(MyBaseView):
    fields = medication_fields.keys()
    fields.remove('id')
    form_columns = fields

# Add Admin ModelViews
admin.add_view(ChildView(Child, db.session))
admin.add_view(DoctorView(Doctor, db.session))
admin.add_view(PartnerView(Partner, db.session))
admin.add_view(CaregiverView(Caregiver, db.session))
admin.add_view(SpecialistView(Specialist, db.session))
admin.add_view(SpecialistTypeView(SpecialistType, db.session))
admin.add_view(MilestoneTypeCategoryView(MilestoneTypeCategory, db.session))
admin.add_view(MilestoneTypeView(MilestoneType, db.session))
admin.add_view(MeasurementTypeView(MeasurementType, db.session))
admin.add_view(CampView(Camp, db.session))
admin.add_view(MedicalConditionView(MedicalCondition, db.session))
admin.add_view(MedicationView(Medication, db.session))
