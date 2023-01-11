import datetime

from django import forms
from django.core.exceptions import ValidationError

# used to wrap text in on of django's translation functions, which is good practice if you want to translate site at a later date
from django.utils.translation import gettext_lazy as _


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default is 3 weeks)")

    # django provides numerous places to validate data. Easiest way is to override the method clean_<fieldname>()
    def clean_renewal_date(self):
        # cleaned_data gets the data "cleaned" and sanitised of potentially unsafe input using the default validators
        # "cleaned" - converted into the correct standard type for the data (in this case datetime.datetime)
        data = self.cleaned_data['renewal_date']

        # check if date is not in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal is in the past'))
        
        # check if date is in the allowed range (+4 weeks from today)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal is too far ahead (i.e. more than 4 weeks)'))

        return data


from django.forms import ModelForm
from catalog.models import BookInstance

class RenewBookModelForm(ModelForm):
    
    # same as before, except name of function: the name of the model field!!
        # - 'due_back'
    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
           raise ValidationError(_('Invalid date - renewal in past'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
           raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data

    class Meta: 
        model = BookInstance
        fields = ['due_back']
        # fields = '__all__' or exclude ['id', ect ...]

        # can also override some of the attributes in the model, specifiying a dict containing the field to change and its new value
        labels = {'due_back': _('New renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default is 3 weeks).')} 



