from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import Optional

class SearchForm(FlaskForm):
    q = StringField('Suche', validators=[Optional()])
    submit = SubmitField('Suchen')

class DateRangeForm(FlaskForm):
    start = DateField('Von', format='%Y-%m-%d', validators=[Optional()])
    end = DateField('Bis', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Filter')

class ContactFilterForm(FlaskForm):
    kind = SelectField('Art', choices=[('', 'Alle'), ('Email', 'Email'), ('Telefon', 'Telefon'), ('persönlich', 'persönlich')])
    submit = SubmitField('Filter')
