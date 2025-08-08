from django.urls import path
from .views import CompanyCRUDView, InternCRUDView, SupervisorCRUDView, ProjectCRUDView

urlpatterns = [
    # Company
    path('companies/', CompanyCRUDView.as_view()),
    path('companies/<int:pk>/', CompanyCRUDView.as_view()),

    # Intern
    path('interns/', InternCRUDView.as_view()),
    path('interns/<int:pk>/', InternCRUDView.as_view()),

    # Supervisor
    path('supervisors/', SupervisorCRUDView.as_view()),
    path('supervisors/<int:pk>/', SupervisorCRUDView.as_view()),

    # Project
    path('projects/', ProjectCRUDView.as_view()),
    path('projects/<int:pk>/', ProjectCRUDView.as_view()),
]
