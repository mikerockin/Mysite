from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/'


def register(request):
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('story:post_list')
    context = {'form': form}
    return render(request, 'users/register.html', context)

