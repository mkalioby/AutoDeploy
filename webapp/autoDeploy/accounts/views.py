from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.conf import settings

def log_user_in(request,username):
    from django.contrib.auth.models import User
    user=User.objects.get(username=username)
    user.backend='django.contrib.auth.backends.ModelBackend'
    login(request, user)

    if "redirect" in request.POST:
        return redirect(request.POST["redirect"])
    else:
        return redirect(settings.BASE_URL)

def check(request):
    if request.method=="POST":
        print("In Check")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        err=""
        if user is not None:
            if user.is_active:
                if "mfa" in settings.INSTALLED_APPS:
                    from mfa.helpers import has_mfa
                    res =  has_mfa(request,username=username)
                    if res: return res
                    return log_user_in(request,username)
            else:
                err="This user is NOT activated yet."
        else:
            err="The username or the password is wrong."
        print("Error:", err)
        return render(request,"login.html",{"err":err})
    else:
        return render(request,"login.html")

def signOut(request):
    logout(request)
    return render(request,"logout.html")