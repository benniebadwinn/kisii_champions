from django.shortcuts import redirect, render

# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required
from .forms import HolidayForm,OffDutyForm
from holiday_off.models import Holiday,OffDuty
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required 
import time
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages


def index(request):
 
    return render(request, 'index.html')


class CustomLoginView(LoginView):
    template_name = 'admin/login.html'  # Use the appropriate template path for your admin login

    def form_valid(self, form):
        response = super().form_valid(form)
        next_url = self.request.GET.get('next', None)
        if next_url:
            return redirect(next_url)
        return response




def is_admin(user):
    print(user.is_authenticated, user.is_staff)
    return user.is_authenticated and user.is_staff


@login_required(login_url='account:login')
# @user_passes_test(is_admin, login_url='account:login')
def off_duty(request):
    error_message = None

    if not request.user.is_staff:
        # Display an error message and render the same page
        error_message = "You don't have permission to perform this action."
        messages.error(request, error_message)
        form = OffDutyForm(user=request.user)
        return render(request, 'off_duty.html', {'form': form, 'error_message': error_message})

    if request.method == 'POST':
        form = OffDutyForm(user=request.user, data=request.POST)
        if form.is_valid():
            off_duty_instance = form.save(commit=False)

            # Check if the same holiday is already assigned to the staff
            existing_off_duty = OffDuty.objects.filter(staff=off_duty_instance.staff, holiday=off_duty_instance.holiday).exists()

            if not existing_off_duty:
                # Deduct off-duty days from the remaining days of the associated holiday
                off_duty_instance.save()
                holiday = off_duty_instance.holiday
                holiday.remaining_days -= 1  # Assuming you deduct 1 day per off-duty instance
                holiday.save()

                # Wait for 3 minutes before logging out
                time.sleep(3)

                # Display a success message
                messages.success(request, "Off-duty request saved successfully.")

                return render(request, 'off_duty.html', {'form': OffDutyForm(user=request.user), 'error_message': error_message})
            else:
                # Handle the case where the holiday is already assigned to the staff
                error_message = "This holiday is already assigned to the staff."
                form.add_error(None, error_message)
                return render(request, 'off_duty.html', {'form': form, 'error_message': error_message})
    else:
        form = OffDutyForm(user=request.user)

    return render(request, 'off_duty.html', {'form': form, 'error_message': error_message})






def off_duty_read_only(request):
    holidays = Holiday.objects.all()

    holiday_info = []
    for holiday in holidays:
        assigned_staff = holiday.staff.all()
        for staff_member in assigned_staff:
            off_duty_instances = OffDuty.objects.filter(staff=staff_member, holiday=holiday)
            off_duty_data = [{'date': off_duty_instance.date} for off_duty_instance in off_duty_instances]

            holiday_data = {
                'name': holiday.name,
                'assigned_staff': staff_member.username,
                'off_duty_instances': off_duty_data,
                'total_off_duty_instances': off_duty_instances.count(),
                'total_holidays_assigned': staff_member.holidays.count(),
                'remaining_holidays': staff_member.holidays.count() - staff_member.offduty_set.count(),
            }
            holiday_info.append(holiday_data)

    return render(request, 'off_duty_read_only.html', {'holiday_info': holiday_info, 'holidays': holidays})


@login_required(login_url='account:login')
def off_duty_read_only1(request):
    # Get holidays assigned to the logged-in user
    user_holidays = Holiday.objects.filter(staff=request.user)

    holiday_info = []
    for holiday in user_holidays:
        off_duty_instances = OffDuty.objects.filter(staff=request.user, holiday=holiday)
        off_duty_data = [{'date': off_duty_instance.date} for off_duty_instance in off_duty_instances]

        holiday_data = {
            'name': holiday.name,
            'assigned_staff': request.user.username,
            'off_duty_instances': off_duty_data,
            'total_off_duty_instances': off_duty_instances.count(),
            'total_holidays_assigned': request.user.holidays.count(),
            'remaining_holidays': request.user.holidays.count() - request.user.offduty_set.count(),
        }
        holiday_info.append(holiday_data)

    return render(request, 'off_duty_read_only.html', {'holiday_info': holiday_info, 'holidays': user_holidays})



@login_required(login_url='account:login')
# @user_passes_test(is_admin, login_url='account:login')
def register_holiday(request):
    error_message = None

    if not request.user.is_staff:
        # Display an error message and render the same page
        error_message = "You don't have permission to perform this action."
        messages.error(request, error_message)
        form = OffDutyForm(user=request.user)
        return render(request, 'off_duty.html', {'form': form, 'error_message': error_message})
    if request.method == 'POST':
        form = HolidayForm(request.POST)
        if form.is_valid():
            holiday = form.save()

            # Assign selected staff to the holiday
            selected_staff = form.cleaned_data['staff']
            holiday.staff.set(selected_staff)

            # Include the logic for printing details in the console
            print(f"Holiday: {holiday.name}")
            print(f"Date: {holiday.date}")

            if holiday.staff.exists():
                print("Assigned Staff:")
                for staff_member in holiday.staff.all():
                    print(f"Staff Member: {staff_member.username}")
                    print(f"Total Off-Duty Instances: {staff_member.offduty_set.count()}")

                    # Calculate total number of holidays assigned to offduty.staff
                    total_holidays_assigned = staff_member.holidays.count()
                    print(f"Total Holidays Assigned: {total_holidays_assigned}")

                    # Deduct staff_member.offduty_set.count() from total_holidays_assigned
                    remaining_holidays = total_holidays_assigned - staff_member.offduty_set.count()
                    print(f"Remaining Holidays: {remaining_holidays}")

            else:
                print("No staff assigned to this holiday.")

            print("\n")  # Adding a newline for better readability in the console

            return redirect('/register_holiday')  # Redirect to the same page or a success page
    else:
        form = HolidayForm()

    assignments = Holiday.objects.all()
    return render(request, 'register_holiday.html', {'form': form, 'assignments': assignments})