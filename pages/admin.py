from django.contrib import admin
from .models import *
from filter.models import *

class FilterInline (admin.TabularInline):
    model = FilterValue
    extra = 0
class ImagesInline (admin.TabularInline):
    model = HousePhotos
    extra = 0

# class FilterValueInline(admin.TabularInline):
#     model = FilterValue.
class HouseAdmin(admin.ModelAdmin):

    list_display = [field.name for field in House._meta.fields]
    inlines = [ImagesInline,FilterInline]

    class Meta:
        model = House

class HouseCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in House._meta.fields]
    inlines = [FilterInline]

    class Meta:
        model = HouseCategory

admin.site.register(Town)
admin.site.register(NewsTag)
admin.site.register(News)
admin.site.register(HouseCategory)

admin.site.register(CategoryFilter)
admin.site.register(House,HouseAdmin)
admin.site.register(HousePhotos)
admin.site.register(Chat)
admin.site.register(Message)