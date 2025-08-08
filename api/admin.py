from django.contrib import admin
from .models import Intern, Company, Project, Supervisor

# Register your models here.
admin.site.register(Intern)
admin.site.register(Company)
admin.site.register(Project)
admin.site.register(Supervisor)