from django.urls import path
from . import views

app_name = "employees"

urlpatterns = [
    path('', views.EmployeeListView.as_view(), name='employee_list'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('<int:pk>/edit_skills/', views.SkillView.as_view(), name='edit_skills'),
]