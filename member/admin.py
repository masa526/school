from django.contrib import admin
from member.models import Member

# admin.site.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'gender', 'age',)  # 一覧に出したい項目

admin.site.register(Member, MemberAdmin)
