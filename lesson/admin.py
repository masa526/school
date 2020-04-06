from django.contrib import admin
from lesson.models import Lesson

# Register your models here.
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'hour', 'charge_yen', 'member', 'plan')

admin.site.register(Lesson, LessonAdmin)
