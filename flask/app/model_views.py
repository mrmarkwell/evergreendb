from datetime import date
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import typefmt
from api.marshallers import DATE_FMT


def date_format(view, value):
    return value.strftime(DATE_FMT)

MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
        type(None): typefmt.null_formatter,
        date: date_format
    })

class MyBaseView(ModelView):
    column_type_formatters = MY_DEFAULT_FORMATTERS

class ChildView(MyBaseView):
    column_exclude_list = ['medical_history', 'child_history','program_departure_reason']
    #form_columns = ['child_english_name', 'child_pinyin_name']