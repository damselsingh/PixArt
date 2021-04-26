from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import feeds, SignUpForm, LoginForm, EditUserChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import People
from django.contrib import messages
from django.contrib.auth.models import Group
from django.core.cache import cache
# Create your views here.

def home(request):
     if not request.user.is_authenticated:
          return render(request, 'pinterest/home.html')
     else:
          return HttpResponseRedirect('/post/')

     
def post(request):
     if request.user.is_authenticated:
          user = request.user
          full_name = user.get_username()
          if full_name == '':
               full_name = 'Anonymous'
          ct = cache.get('count', version=user.pk)
          if request.method == 'POST':
               image = request.FILES['image']
               name = full_name
               caption = request.POST['caption']
               new = People(image=image, name=name, caption=caption, user=request.user)
               new.save()
               messages.success(request, 'successfully posted!')
               return HttpResponseRedirect('/feeds/')
          else:
               form = feeds()
          return render(request, 'pinterest/post.html', {'forms' : form, 'full_name': full_name,'ct': ct})
     else:
          return HttpResponseRedirect('/login/')
        
 
def feed(request):
     if request.user.is_authenticated:
          post = People.objects.order_by('-id')
          return render(request, 'pinterest/feeds.html', {'post': post})
     else:
          messages.success(request, 'login first!')
          return HttpResponseRedirect('/login/')
          


def about(request):
     return render(request, 'pinterest/about.html')

def contact(request):
     return render(request, 'pinterest/contact.html')

def user_login(request):
     if not request.user.is_authenticated:
          if request.method == "POST":
               form = LoginForm(request=request, data=request.POST)
               if form.is_valid():
                    uname = form.cleaned_data['username']
                    upass = form.cleaned_data['password']
                    user = authenticate(username=uname, password=upass)
                    if user is not None:
                         login(request, user)
                         messages.success(request, 'Logged in Succesfully!!')
                         return HttpResponseRedirect('/post/')
                    else:
                         messages.error(request, 'username or password is invaid.')
          else:
               form = LoginForm()
          return render(request, 'pinterest/login.html', {'form': form})
     else:
          return HttpResponseRedirect('/post/')


def user_logout(request):
     logout(request)
     messages.success(request, 'Logged out Succesfully!!')
     return HttpResponseRedirect('/login/')
     



def signup(request):
     if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Users')
            user.groups.add(group)  
            form = SignUpForm() 
            login(request, user) 
            messages.success(request, 'You are logged in') 
            return HttpResponseRedirect('/post/')               
     else :
         form = SignUpForm()
     return render(request, 'pinterest/signup.html', {'form': form})

def user_profile(request):
     if request.user.is_authenticated:
          if request.method == 'POST':
               form = EditUserChangeForm(request.POST, instance=request.user) 
               if form.is_valid():
                    form.save()
                    messages.success(request, 'Updated Successfully!!')
                    return HttpResponseRedirect('/post/')
          else:
               form = EditUserChangeForm(instance=request.user)
          return render(request, 'pinterest/profile.html', {'name': request.user, 'form': form})
     else : 
          return HttpResponseRedirect('/login/')

def change_password(request):
     if request.user.is_authenticated:
          if request.method == 'POST':
               form = PasswordChangeForm(user=request.user, data=request.POST)
               if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                    return HttpResponseRedirect('/profile/')
          else:
               form = PasswordChangeForm(user=request)
          return render(request, 'pinterest/password.html', {'form': form})
     else:
          return HttpResponseRedirect('/login/')
                

def your_uploads(request):
     if request.user.is_authenticated:
          user=request.user
          post = People.objects.filter(user=user).order_by('-id')
          return render(request, 'pinterest/your_uploads.html', {'post': post})
     else:
          return HttpResponseRedirect('/')

def delete_post(request, pk):
     if request.user.is_authenticated:
          deldata = People.objects.get(id=pk)
          deldata.delete()
          messages.success(request, 'deleted Successfully!!')
          return HttpResponseRedirect('/your-uploads/')
     else:
          return HttpResponseRedirect('/')