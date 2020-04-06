from django.shortcuts import render, get_object_or_404, redirect

from member.models import Member
from member.forms import MemberForm

# Create your views here.
def member_list(request):
    members = Member.objects.all().order_by('id')
    return render(request, 'member/list.html', {'members': members})


def member_edit(request, member_id=None):
    if member_id:
        member = get_object_or_404(Member, pk=member_id)
        title = "顧客編集"
    else:
        member = Member()
        title = "顧客追加"

    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            member = form.save(commit=False)
            member.save()
            return redirect('member:member_list')
    else:
        form = MemberForm(instance=member)

    return render(request, 'member/edit.html', dict(form=form, member_id=member_id, title=title))


