from django import forms
from .models import EmployeeSkill


class SkillForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = EmployeeSkill
        fields = ('employee', 'skill')