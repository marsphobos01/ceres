from django.contrib import admin
from .models import DashboardLayout, DashboardWidget, QuickActionPreference, UserInterfacePreference
# Register your models here.
admin.site.register(DashboardLayout)
admin.site.register(DashboardWidget)
admin.site.register(QuickActionPreference)
admin.site.register(UserInterfacePreference)