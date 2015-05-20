from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, render_to_response,redirect
from django.contrib.auth import authenticate, login,logout
from django.template import RequestContext
from autoDeploy import settings



def check(request):
    if request.method=="POST":
        print "In Check"
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        err=""
        print "Hi"
        if user is not None:
            if user.is_active:
                login(request, user)
                if "redirect" in request.POST:
                    return redirect(settings.BASE_URL+request.POST["redirect"])
                else:
                    return redirect("/")
                # Redirect to a success page.
            else:
                err="This user is NOT activated yet."
        else:
            err="The username or the password is wrong."
        print "Error:", err
        return render_to_response("account/login.html",{"err":err},context_instance=RequestContext(request))
    else:
        return render_to_response("account/login.html",context_instance=RequestContext(request))

def signOut(request):
    logout(request)
    return render_to_response("account/logout.html",context_instance=RequestContext(request))