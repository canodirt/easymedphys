from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from .forms import SignUpForm, LoginForm
from .models import CustomUser

def loginUser(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']


        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, email=email, password=password)
            print(email)
            print(password)
            print(user)
            print(form)
            # auth_login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # form['username']=request.POST['email']
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = CustomUser
    fields = ('first_name', 'last_name', 'email', 'campep', 'mdcb', 'occupation' )
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user
