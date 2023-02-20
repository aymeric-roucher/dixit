from dal import autocomplete

from django import forms


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('__all__')
        widgets = {
            'birth_country': autocomplete.ModelSelect2(url='country-autocomplete')
        }

class Person(models.Model):
    visited_countries = models.ManyToManyField('your_countries_app.country')