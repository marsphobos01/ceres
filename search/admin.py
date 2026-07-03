from django.contrib import admin
from .models import SearchIndexEntry, SearchAccessHint, SearchHistoryItem, SavedSearch, SearchSynonym
# Register your models here.
admin.site.register(SearchIndexEntry)
admin.site.register(SearchAccessHint)
admin.site.register(SearchHistoryItem)
admin.site.register(SavedSearch)
admin.site.register(SearchSynonym)
