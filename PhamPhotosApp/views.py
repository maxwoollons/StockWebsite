from django.contrib.auth.models import User
from django.forms.widgets import Media
from django.http import request
from django.shortcuts import redirect, render
from .forms import UserRegistrationForm, MediaSubmit
from django.contrib import messages
from .models import photos, purchases, users
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
import PIL



def login_excluded(redirect_to):
    """ This decorator kicks authenticated users out of a view """ 
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect('home') 
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper


def home(request):
    Media = photos.objects.all().filter(approved=True)[:30]
    return render(request, 'PhamPhotosApp/home.html', {'photos':Media})


def login(request):
    if request.user.is_authenticated:
      
        return redirect('home')
    else:
       
        return render(request, 'PhamPhotosApp/login.html')

@login_excluded('app:redirect_to_view')
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.filter(username=username)
            for a in user:
                OK = users(user=a,tokens=0)
                OK.save()
                messages.success(request, f'account created for {username}!')
                return redirect('home')
    else:
        form = UserRegistrationForm()
        
    return render(request, 'PhamPhotosApp/register.html', {'form':form})


@login_required
def SubmitMedia(request):
    if request.method == 'POST':
        form = MediaSubmit(request.POST, request.FILES)
        if form.is_valid():
            ob = form.save(commit=False)
            ob.owner = request.user
            ob.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'account created for {username}!')
            return redirect('home')
    else:
        form = MediaSubmit()
    return render(request, 'PhamPhotosApp/submit.html', {'form':form})


@login_required
def ProfilePage(request):
    user = User.objects.all().filter(id=request.user.id)
    purchase = purchases.objects.all().filter(User=request.user.users)
    uploads = photos.objects.all().filter(owner=request.user)
    return render(request, 'PhamPhotosApp/profile.html', {'profile':user,'uploads':uploads,'pur':purchase})



class PhotoDetail(DetailView):
   
    context_object_name='obj'
    template_name="detailview.html"
    model = photos
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        a = photos.objects.all().filter(id=self.kwargs["pk"]).values_list('photo', flat=True)
        
        image = PIL.Image.open("media/" + a[0])
        
        w,h = image.size
        context['height'] = h
        context['width'] = w
        return context
    
    
def search(request):
        if request.method == 'GET' and request.GET.get('search'):
            search = request.GET.get('search')
            record = photos.objects.all().filter(title__icontains=search,approved=True)
            amt = len(record)
            return render(request, 'PhamPhotosApp/search.html',{'all':record, 'amount':amt})
    
@login_required
def delete(request, pk):
    if photos.objects.all().filter(id=pk,owner=request.user):
        img = photos.objects.all().filter(id=pk,owner=request.user)
        img.delete()
        return render(request, 'PhamPhotosApp/delete.html')
    else:
        return redirect('home')
    
    
@login_required
def purchase(request, pk):
    tokens = request.user.users.tokens
    user = users.objects.all().filter(user_id=request.user.id)
    pic_owner = photos.objects.values_list('owner_id', flat=True).get(id=pk)
    cost = photos.objects.values_list('price', flat=True).get(id=pk)
    ouser = users.objects.all().filter(user_id=pic_owner)
    otokens = users.objects.values_list('tokens', flat=True).get(user=pic_owner)
    print(pic_owner)
    if request.user.id != pic_owner:
        if cost <= tokens:
            new = tokens - cost
            user.update(tokens=new)
            p = purchases(User=request.user.users,Photo_id=pk,downloaded=False)
            p.save()
            onew = otokens + cost
            ouser.update_or_create(tokens=onew) #admin gets 40%
            
            return redirect('success')
        else:
            return redirect('home')
             
             
            
    else:
        return redirect('home')
                 
    
            
    
def success(request):
    return render(request, 'PhamPhotosApp/successful.html')