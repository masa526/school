from django.shortcuts import render

from member.models import Member
from lesson.models import Lesson
from django.db.models import Sum
from datetime import datetime
from . import forms

# Create your views here.
def invoice_list(request):

    form = forms.InvoiceForm(request.GET or None)

    search_year = datetime.today().year
    search_month = datetime.today().month
    if "select_month" in request.GET:
        select_month = request.GET.get("select_month")
        search_ym = datetime.strptime(select_month, '%Y-%m')
        search_year = search_ym.year
        search_month = search_ym.month

    members = Member.objects.all().order_by('id')
    lessons = Lesson.objects.filter(date__year=search_year, date__month=search_month)

    for member in members:
        member.count = lessons.filter(member=member).count()
        plan_names = []
        member.basic_charge_yen = 0
        for plan in lessons.filter(member=member).values('plan__name','plan__basic_charge_yen').distinct():
            plan_names.append(plan['plan__name'])
            member.basic_charge_yen += plan['plan__basic_charge_yen']
        member.plan_names = ",".join(plan_names)
        member.plan_len = len(plan_names)
        member.lesson = lessons.filter(member=member).aggregate(sum_charge_yen=Sum('charge_yen'))

    return render(request, 'invoice/list.html', {'members': members, 'form': form})
