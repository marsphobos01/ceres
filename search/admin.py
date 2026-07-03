from django.contrib import admin
from .models import SearchIndexEntry, SearchHistoryItem, SavedSearch, SearchSynonym #, SearchAccessHint
# Register your models here.
admin.site.register(SearchIndexEntry)
#admin.site.register(SearchAccessHint)
admin.site.register(SearchHistoryItem)
admin.site.register(SavedSearch)
admin.site.register(SearchSynonym)

#TODO: Uncomment SearchAccessHint when search fully up and running.