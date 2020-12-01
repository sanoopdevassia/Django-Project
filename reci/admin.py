from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
import datetime
from django.contrib.admin.filters import DateFieldListFilter
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import decimal, csv
from django.contrib import admin
from django.http import HttpResponse
from django.db.models import F



def make_star_of_the_week(modeladmin, request, queryset):
    queryset.update(star=True )
    make_star_of_the_week.short_description = 'Make star'
def remove_star(modeladmin, request, queryset):
    queryset.update(star=False )
    remove_star.short_description = 'Remove star of the week'

def export_recipes(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Description', 'Active Time', 'Total Time', 'Serves', 'Author ID','Created At'])
    recipe = queryset.values_list('title','descr','active_time','total_time','serves','author','created_at')
    for book in recipe:
        writer.writerow(book)
    return response
    export_recipes.short_description = 'Export to csv'




class MyDateTimeFilter(DateFieldListFilter):
    def __init__(self, *args, **kwargs):
        super(MyDateTimeFilter, self).__init__(*args, **kwargs)

        now = timezone.now()
        # When time zone support is enabled, convert "now" to the user's time
        # zone so Django's definition of "Today" matches what the user expects.
        if timezone.is_aware(now):
            now = timezone.localtime(now)

        today = now.date()

       



class adminRecipe(admin.ModelAdmin):
     
    admin.site.site_header="Welcome Oiishi Admin"
    admin.site.site_title="Oiishi Admin"
    admin.site.index_title="Oiishi"
    list_display=('title','descr','author','fivestarcount','created_at','star')
    readonly_fields=('title','descr','author','fivestarcount','created_at','active_time','total_time','serves','image')
    search_fields = ('title', 'descr', 'created_at')
    list_filter = (
        ('created_at', MyDateTimeFilter),'star'
    )
    def get_queryset(self, request):
        queryset = super(adminRecipe, self).get_queryset(request)
        queryset = queryset.order_by('-fivestarcount',)
        return queryset
    actions = [make_star_of_the_week,remove_star,export_recipes ]

class adminCategory(admin.ModelAdmin):
    list_display=('category_name',)

# class adminRec_cat(admin.ModelAdmin):
#     def recipe_title(self, instance):
#         return instance.recipe.title# 
#     def category_category_name(self, instance):
#         return instance.category.category_name
#     list_display=('recipe_title','category_category_name',)
   
class AdminComment(admin.ModelAdmin):
    def recipe_title(self, instance):
        return instance.recipe.title

    list_display=('comment','rating','author','recipe_title','created_at',)
    readonly_fields=('comment','rating','author','recipe_title','created_at','recipe')
    list_filter = (
        ('created_at', MyDateTimeFilter),
    )
    search_fields = ('rating',)


    
admin.site.register(recipes,adminRecipe)
admin.site.register(category,adminCategory)
# admin.site.register(reciepe_category,adminRec_cat)
admin.site.register(comments,AdminComment)
admin.site.unregister(Group)

