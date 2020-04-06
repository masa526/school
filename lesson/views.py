from django.shortcuts import render, get_object_or_404, redirect

from lesson.models import Lesson
from plan.models import Plan, PlanPayg
from lesson.forms import LessonForm
from django.db.models import Sum, Q
from datetime import date, timedelta

# Create your views here.
def lesson_list(request):
    lessons = Lesson.objects.all().order_by('id')
    return render(request, 'lesson/list.html', {'lessons': lessons})


def lesson_edit(request, lesson_id=None):
    if lesson_id:
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        title = "レッスン受講記録編集"
    else:
        lesson = Lesson()
        title = "レッスン受講記録登録"

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.charge_yen = 0
            lesson.save()

            # 対象ユーザーの対象プランの当月受講履歴を取得
            year = int(lesson.date.strftime('%Y'))
            month = int(lesson.date.strftime('%m'))
            first_day = date(year, month, 1)
            end_day = date(year, month + 1, 1) - timedelta(days=1)
            q = Q(member=lesson.member, plan=lesson.plan, date__range=[first_day, end_day])
            t_lessons = Lesson.objects.filter(q).order_by('date')

            ruiseki_start = 0 # 累積開始時間
            ruiseki_end = 0   # 累積終了時間

            # 当月受講履歴をひとつずつ計算する
            for t_lesson in t_lessons:
                print("id:" + str(t_lesson.id))
                # 今回の累積レッスン終了時間
                ruiseki_end += t_lesson.hour

                # 今回の支払金額
                charge_yen = 0

                # 基本時間 > 0
                if t_lesson.plan.basic_include_hour > 0:
                    # 累積終了時間 <= 基本時間
                    if ruiseki_end <= t_lesson.plan.basic_include_hour:
                        t_lesson.charge_yen = charge_yen
                        t_lesson.save()
                        continue
                    else:
                        ruiseki_start = t_lesson.plan.basic_include_hour

                # 従量開始時間 <= 累積終了時間
                # 従量開始時間 <= 累積開始時間
                # 累積開始時間 <= 従量終了時間 または 従量終了時間 is null
                plan_paygs = PlanPayg.objects.filter(
                    Q(Q(plan=t_lesson.plan), Q(payg_end_hour__gte=ruiseki_start), Q(payg_start_hour__lte=ruiseki_end)) |
                    Q(Q(plan=t_lesson.plan), Q(payg_start_hour__lte=ruiseki_end), Q(payg_end_hour__isnull=True))
                ).order_by('payg_start_hour')

                for plan_payg in plan_paygs:
                    print("ruiseki_start:" + str(ruiseki_start))
                    print("ruiseki_end:" + str(ruiseki_end))
                    print("before_charge_yen:" + str(charge_yen))
                    if plan_paygs.count() > 1 and plan_payg.payg_end_hour is not None:
                        if plan_payg == plan_paygs.last():
                            # (累積終了時間 - 現在の従量開始時間) × 従量料金
                            now_hour = (ruiseki_end - ruiseki_start)
                            charge_yen += (ruiseki_end - ruiseki_start) * plan_payg.payg_charge_yen
                            ruiseki_start = ruiseki_end
                        else:
                            # (現在の従量終了時間 - 累積開始時間) × 従量料金
                            now_hour = (plan_payg.payg_end_hour - ruiseki_start)
                            charge_yen += (plan_payg.payg_end_hour - ruiseki_start) * plan_payg.payg_charge_yen
                            ruiseki_start = plan_payg.payg_end_hour
                    else:
                        # (累積終了時間 - 累積開始時間) × 従量料金
                        now_hour = (ruiseki_end - ruiseki_start)
                        charge_yen += (ruiseki_end - ruiseki_start) * plan_payg.payg_charge_yen
                        ruiseki_start = ruiseki_end
                    print("now_hour:" + str(now_hour))
                    print("after_charge_yen:" + str(charge_yen))
                    print("payg_charge_yen:" + str(plan_payg.payg_charge_yen))

                # 支払金額を更新
                t_lesson.charge_yen = charge_yen
                t_lesson.save()

            return redirect('lesson:lesson_list')
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'lesson/edit.html', dict(form=form, lesson_id=lesson_id, title=title))
