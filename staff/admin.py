from django.contrib import admin
from .models import Department, StaffProfile

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'get_department', 'specialisation']

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Name'

    def get_department(self, obj):
        return obj.department.name if obj.department else '—'
    get_department.short_description = 'Department'