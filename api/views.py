from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
import json

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
        


