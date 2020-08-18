from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse, render
from .forms import UserForm, ProfileForm
# Create your views here.


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return HttpResponseRedirect(reverse('accounts:profile'))
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'digitaldairy/html/user-profile.html')

    else:
        return render(request, 'digitaldairy/html/user-profile.html')
