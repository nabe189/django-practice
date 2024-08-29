from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
#from django.views import View
from django.views import generic
from django.views.generic import ListView, DetailView
from .models import Employee, SkillCategory, Skill, EmployeeSkill
from .forms import SkillForm
from django.http import JsonResponse

class EmployeeListView(ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'

class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.get_object()

        # カテゴリごとにスキルをグループ化
        categories = SkillCategory.objects.all()
        skills_by_category = {}
        for category in categories:
            skills = employee.employee_skills.filter(skill__category=category)
            if skills.exists():
                skills_by_category[category.name] = [emp_skill.skill.name for emp_skill in skills]

        context['skills_by_category'] = skills_by_category
        return context

class SkillView(DetailView, generic.edit.ModelFormMixin):
    model = Employee
    form_class = SkillForm
    template_name = 'employees/edit_skills.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy("employees:edit_skills", kwargs={"pk":self.kwargs["pk"]})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.kwargs["pk"]
        employee_skills = EmployeeSkill.objects.filter(employee=employee)
        context["employee_skills"] = employee_skills
        context['categories'] = SkillCategory.objects.all()
        context['skills'] = Skill.objects.all()

        category = self.request.GET.get('category')
        if category:
            context['form'].fields['skill'].queryset = Skill.objects.filter(category_id=category)

        return context
    
def get_skills_for_category(request, **kwargs):
    category_id = request.GET.get('category')
    if category_id:
        skills = Skill.objects.filter(category_id=category_id).values('id', 'name')
    else:
        skills = Skill.objects.all().values('id', 'name')
    
    context = {
        'skills': list(skills)
    }
    return JsonResponse(context)