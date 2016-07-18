from flask_wtf import Form
from wtforms.fields import *
from flask.ext.wtf.html5 import URLField
#from flask.ext.wtf import Optional
from wtforms.validators import *
from wtforms.validators import ValidationError, StopValidation
from models import *

def get_countries_etld():
    """function to return a full list of countries for which I have extracted valid data from the sources via the scripts in Vasco\ETL"""
    countries_in_database=db.engine.execute('select * from ent where id in (select ent_id from literal)').fetchall()
    full_list=[]
    for c in countries_in_database:
        full_list.append(
            (str(c[2]), str(c[2]))
            )
    
    return full_list

def create_years(up_to=2015):
    Years=[]
    add_this_year=1989
    while add_this_year < up_to:
        add_this_year += 1
        Years.append(
            (str(add_this_year),str(add_this_year))
            )

    return Years


class Availibility_order(Form):
    """the final product on this form is just a set of years and countries from which I can derive availible data."""
    countries = SelectMultipleField('Countries with valid data here', choices=get_countries_etld(), coerce=str)
    years = SelectMultipleField('Years with valid data here', choices=create_years(), coerce=str)

class Data_set_order(Form):
    """this will build out the final data set from the data in the form declared above"""
    indicators = SelectMultipleField('Indicators availible', coerce=str, choices=[('no data','no data')])
    Email = StringField('<font size="1">If you\'d like an email with the data please enter your address here. (the data will be sent here in CSV format)</font> &nbsp  &nbsp', 
             validators=[
             Optional(),
             Length(1,120),
             Email(message='dude, valid email. if you dont know what that is google \"email\". or, you know, maybe the internet isn\'t for you?')
             ])
    send_descriptions = BooleanField('<font size="1">check here if you would like indicator desctiprtions added<br></font> &nbsp  &nbsp')
    #the above will allow users to add data descriptions once they are building to the final file correctly, work still in progress

    def set_data_options(self, query_results):
        self.indicators.choices = query_results