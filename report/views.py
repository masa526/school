from django.shortcuts import render
from datetime import datetime
from . import forms

from plan.models import Plan
from lesson.models import Lesson
from member.models import Member
from django.db.models import Sum

# Create your views here.
def report_list(request):

    form = forms.ReportForm(request.GET or None)

    search_year = datetime.today().year
    search_month = datetime.today().month
    if "select_month" in request.GET:
        select_month = request.GET.get("select_month")
        search_ym = datetime.strptime(select_month, '%Y-%m')
        search_year = search_ym.year
        search_month = search_ym.month

    gender_reports= []
    plans = Plan.objects.all().order_by('id')
    lessons = Lesson.objects.filter(date__year=search_year, date__month=search_month)
    for plan in plans:
        for gender in Member.GENDER:
            gender_reports.append({
                'plan_name': plan.name,
                'plan_basic_charge_yen': plan.basic_charge_yen,
                'gender': gender[1],
                'lesson_num': lessons.filter(plan=plan, member__gender=gender[0]).count(),
                'lesson_member_num': lessons.filter(plan=plan, member__gender=gender[0]).values('member').distinct().count(),
                'price': lessons.filter(plan=plan, member__gender=gender[0]).aggregate(sum_charge_yen=Sum('charge_yen')),
            })

    generation_reports= []
    for plan in plans:
        for gender in Member.GENDER:
            for generation in Member.GENERATION:
                gen = int(generation[0])
                generation_reports.append({
                    'plan_name': plan.name,
                    'plan_basic_charge_yen': plan.basic_charge_yen,
                    'gender': gender[1],
                    'generation': generation[1],
                    'lesson_num': lessons.filter(plan=plan, member__gender=gender[0], member__age__range=(gen, gen + 9)).count(),
                    'lesson_member_num': lessons.filter(plan=plan, member__gender=gender[0], member__age__range=(gen, gen + 9)).values('member').distinct().count(),
                    'price': lessons.filter(plan=plan, member__gender=gender[0], member__age__range=(gen, gen + 9)).aggregate(sum_charge_yen=Sum('charge_yen')),
                })
    return render(request, 'report/list.html', {'generation_reports':generation_reports, 'gender_reports':gender_reports, 'form': form})
