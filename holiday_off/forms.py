
from django import forms
from holiday_off.models import OffDuty,Holiday
from django.contrib.auth.models import User



class OffDutyForm(forms.ModelForm):
    class Meta:
        model = OffDuty
        fields = ['staff', 'holiday','date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['staff'].queryset = User.objects.all()


class HolidayForm(forms.ModelForm):
    staff = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Holiday
        fields = ['name', 'date', 'staff']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        off_duty_staff_ids = OffDuty.objects.values_list('staff_id', flat=True)
        self.fields['staff'].queryset = User.objects.exclude(id__in=off_duty_staff_ids)
