from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Company(models.Model):
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name

class Supervisor(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)])
    email = models.EmailField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Intern(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active'
        INACTIVE = 'inactive'

    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)])
    email = models.EmailField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    supervisor = models.ForeignKey('Supervisor', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)

    def __str__(self):
        return self.name
    
class Project(models.Model):
    project_name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE, null=True)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, null=True)
    description = models.TextField()

    def __str__(self):
        return self.project_name
    
