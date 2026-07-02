from django.contrib import admin
from .models import Module, ModuleMembership, Lecture
# Register your models here.

admin.site.register(Module)
admin.site.register(ModuleMembership)
admin.site.register(Lecture)
