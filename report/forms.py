from django import forms
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

class ReportForm(forms.Form):
    today = datetime.today()
    select_month = forms.ChoiceField(
        choices = (
            (today.strftime('%Y-%m'), today.strftime('%Y-%m')),
            ((today - relativedelta(months=1)).strftime('%Y-%m'), (today - relativedelta(months=1)).strftime('%Y-%m')),
            ((today - relativedelta(months=2)).strftime('%Y-%m'), (today - relativedelta(months=2)).strftime('%Y-%m')),
            ((today - relativedelta(months=3)).strftime('%Y-%m'), (today - relativedelta(months=3)).strftime('%Y-%m')),
        ),
        required=True,
        widget=forms.widgets.Select
    )
