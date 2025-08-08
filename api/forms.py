from django import forms
from .models import Company, Intern, Supervisor, Project

# Forms
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

class InternForm(forms.ModelForm):
    class Meta:
        model = Intern
        fields = '__all__'

class SupervisorForm(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = '__all__'

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'