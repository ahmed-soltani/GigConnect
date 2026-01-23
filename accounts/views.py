from django.contrib.auth import (login as auth_login,)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .forms import MySignUpForm, UpdateUserForm
from .models import MyUser

class SignUpView(CreateView):
    form_class = MySignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class MyLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form): # This is an overridden method from LoginView
        """Security check complete. Log the user in. PERFORM CUSTOM CODE."""
        auth_login(self.request, form.get_user())
        # form.get_user().execute_after_login()  # Custom code # method currently empty
        return HttpResponseRedirect(self.get_success_url())


class MyUserListView(UserPassesTestMixin, ListView):
    model = MyUser
    context_object_name = 'all_myusers'
    template_name = 'user_list.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_cs


@login_required
def profile_view(request):
    return render(request, 'user_detail.html', { 'myuser': request.user })


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = MyUser
    form_class = UpdateUserForm
    template_name = 'user_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user
