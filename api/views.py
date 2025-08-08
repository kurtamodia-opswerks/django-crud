from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
import json
from .models import Company, Supervisor, Intern, Project
from .forms import CompanyForm, SupervisorForm, InternForm, ProjectForm

# Parent view
@method_decorator(csrf_exempt, name='dispatch')
class BaseCRUDView(View):
    model: None
    form: None

    # Read 
    def get(self, request, pk=None):
        if pk:
            try:
                instance = self.model.objects.select_related().get(pk=pk)
                return JsonResponse(model_to_dict(instance))
            except self.model.DoesNotExist:
                return JsonResponse({'error': 'Object not found'})
        else:
            instances = self.model.objects.all()
            data = [model_to_dict(instance) for instance in instances]
            return JsonResponse(data, safe=False)
        
    # Create
    def post(self, request):
        data = json.loads(request.body)
        form = self.form(data)
        if form.is_valid():
            instance = form.save()
            return JsonResponse(model_to_dict(instance))
        else:
            return JsonResponse(form.errors)
        
    # Update
    def put(self, request, pk):
        try:
            instance = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return JsonResponse({'error': 'Object not found'})
        
        data = json.loads(request.body)
        instance = self.model.objects.get(pk=pk)
        form = self.form(data, instance=instance)
        if form.is_valid():
            instance = form.save()
            return JsonResponse(model_to_dict(instance))
        else:
            return JsonResponse(form.errors)
        
    # Delete
    def delete(self, request, pk):
        try:
            instance = self.model.objects.get(pk=pk)
            instance.delete()
            return JsonResponse({'deleted': True})
        except self.model.DoesNotExist:
            return JsonResponse({'error': 'Object not found'})
        

# Child views
class CompanyCRUDView(BaseCRUDView):
    model = Company
    form = CompanyForm

class InternCRUDView(BaseCRUDView):
    model = Intern
    form = InternForm

    def get(self, request, pk=None):
        status_param = request.GET.get("status")
        company_id = request.GET.get("company_id")

        # If filtering by status
        if status_param in [Intern.Status.ACTIVE, Intern.Status.INACTIVE]:
            interns = (
                self.model.objects
                .select_related('company', 'supervisor')  
                .filter(status=status_param)
            )
            data = [model_to_dict(intern) for intern in interns]
            return JsonResponse(data, safe=False)
        
        # If filtering by company
        if company_id:
            interns = (
                self.model.objects
                .select_related('company', 'supervisor')
                .filter(company_id=company_id)
            )
            data = [model_to_dict(intern) for intern in interns]
            return JsonResponse(data, safe=False)

        # Default
        return super().get(request, pk)


class SupervisorCRUDView(BaseCRUDView):
    model = Supervisor
    form = SupervisorForm

class ProjectCRUDView(BaseCRUDView):
    model = Project
    form = ProjectForm

    def get(self, request, pk=None):
        # If filtering by intern_id
        intern_id = request.GET.get("intern_id")
        if intern_id:
            projects = self.model.objects.filter(intern_id=intern_id)
            data = [model_to_dict(project) for project in projects]
            return JsonResponse(data, safe=False)

        # default
        return super().get(request, pk)


