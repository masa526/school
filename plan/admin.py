from django.contrib import admin
from plan.models import Plan, PlanPayg

# Register your models here.
class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'basic_charge_yen', 'basic_include_hour',)

class PlanPaygAdmin(admin.ModelAdmin):
    list_display = ('id', 'plan', 'payg_start_hour', 'payg_end_hour', 'payg_charge_yen', )

admin.site.register(Plan, PlanAdmin)
admin.site.register(PlanPayg, PlanPaygAdmin)
