from django.contrib import admin
from .models import *
# Register your models here.

class BrandAdmin(admin.ModelAdmin):
	list_display=['id','name','link','img','price','connect','brand_cate','location_cate','views','create_time','status','introduce']
	list_editable=['status','price','img','link','introduce']
	list_filter=['status','brand_cate','location_cate']
	search_fields=['introduce']

class Location_CateAdmin(admin.ModelAdmin):
	list_display=['id','Location_name']

class Brands_CateAdmin(admin.ModelAdmin):
	list_display=['id','Brands_name']

class LabelAdmin(admin.ModelAdmin):
	list_display=['id','name','label']	

class HistoryAdmin(admin.ModelAdmin):
	list_display=['id','user','name','view_date']
	list_filter=['user','name','view_date']

class SetAdmin(admin.ModelAdmin):
    list_display = ['id','name','brand']
    list_filter = ['name']
	
class AboutAdmin(admin.ModelAdmin):
	list_display=['text','qq','email']


admin.site.register(Location_Cate,Location_CateAdmin)
admin.site.register(Brands_Cate,Brands_CateAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(Label,LabelAdmin)
admin.site.register(Set,SetAdmin)
admin.site.register(About,AboutAdmin)
admin.site.register(History,HistoryAdmin)

admin.site.register(User)

