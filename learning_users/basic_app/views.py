from django.shortcuts import render
from basic_app.forms import UserProfileInfoForm, UserForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def index(request):
    return render(request, 'basic_app/index.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged in, nice")


def register(request):

    # assume they are not registered
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # check if the data are valid
        if user_form.is_valid() and profile_form.is_valid():

            # set_password is a hasher method
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            # set up the one to one relationship
            # --> models.py user = models.OneToOneField(User, on_delete=models.CASCADE)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html', {'user_form': user_form,
                                                           'profile_form': profile_form,
                                                           'registered': registered})

def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # If the given credentials are valid, return a User object. --> checking in database
        user = authenticate(username=username, password=password)

        if user:
            # is_active gets false automatically after a while e.g. inactive > 6 months
            if user.is_active:
                # Persist a user id and a backend in the request. This way a user doesn't
                # have to reauthenticate on every request.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("some tried to login and failed")
            print("UserName: {} and password: {}" .format(username, password))
            return HttpResponse("invalid login details supplied!")
    else:
        return render(request, 'basic_app/login.html', {})












