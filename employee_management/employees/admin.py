from django.contrib import admin
from .models import Employee, Skill, SkillCategory, EmployeeSkill

admin.site.register(Employee)
admin.site.register(Skill)
admin.site.register(SkillCategory)
admin.site.register(EmployeeSkill)