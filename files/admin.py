from django.contrib import admin
from .models import StoredFile, FileVersion, FileLink, FileShare, FileTag, FilePreview
# Register your models here.
admin.site.register(StoredFile)
admin.site.register(FileVersion)
admin.site.register(FileLink)
admin.site.register(FileShare)
admin.site.register(FileTag)
admin.site.register(FilePreview)
