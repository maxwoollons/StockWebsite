from django.contrib.auth.models import User
from django.forms.widgets import Media
from django.http import request
from django.shortcuts import redirect, render
from .forms import UserRegistrationForm, MediaSubmit
from django.contrib import messages
from .models import photos, purchases, users, payments, creditpurchases
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from PIL import Image
import PIL
import json


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
   # photo_ids = photos.objects.all().filter(owner_id=request.user.id)
   # pic_owner = purchases.objects.values_list('price', flat=True).get(id=pk)
    user = User.objects.all().filter(id=request.user.id)
    purchase = purchases.objects.all().filter(User=request.user.users)
    purchasess = purchases.objects.all()
    uploads = photos.objects.all().filter(owner=request.user)
    payment = payments.objects.all().filter(user=request.user)
    credits = creditpurchases.objects.all().filter(user=request.user)
    
    return render(request, 'PhamPhotosApp/profile.html', {'profile':user,'uploads':uploads,'pur':purchase,'num':purchasess,'items':payment,'creditss':credits})



class PhotoDetail(DetailView):
   
    context_object_name='obj'
    template_name="detailview.html"
    model = photos
    
    
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
    ouser = users.objects.all().filter(user_id=pic_owner) #
    owneruser = User.objects.get(id=pic_owner) #
    title = photos.objects.values_list('title', flat=True).get(id=pk)
    otokens = users.objects.values_list('tokens', flat=True).get(user=pic_owner)
    print(pic_owner)
    if request.user.id != pic_owner:
        if cost <= tokens:
            commission = cost*40/100
            onew = otokens + (cost - commission)
            paied = cost-commission
            new = tokens - cost
            user.update(tokens=new)
            p = purchases(User=request.user.users,Photo_id=pk,downloaded=False,paied=paied)
            p.save()
            
            ouser.update(tokens=onew)
            q = payments(user=owneruser,amount=paied,title=title)
            q.save()
            
            return redirect('success')
        else:
            return redirect('home')
             
             
            
    else:
        return redirect('home')
                 
    
            
    
def success(request):
    return render(request, 'PhamPhotosApp/successful.html')


def homey(request):
    return redirect('home')


def credits(request):
    return render(request, 'PhamPhotosApp/credits.html')

@login_required
def purchasepage(request, amt):
    if amt < 2:
        return redirect('credits')
    elif amt == 5:
        toke = 500
        name_pack = "$5 Credit Deal"
        return render(request, 'PhamPhotosApp/purchasepage.html',{'cost':amt,'credits':toke,'deal':name_pack})
    elif amt == 10:
        toke = 1100
        name_pack = "$10 Credit Deal"
        return render(request, 'PhamPhotosApp/purchasepage.html',{'cost':amt,'credits':toke,'deal':name_pack})
    elif amt == 20:
        toke = 3000
        name_pack = "$20 Credit Deal"
        return render(request, 'PhamPhotosApp/purchasepage.html',{'cost':amt,'credits':toke,'deal':name_pack})
    else:
        amt = amt
        toke = amt * 100
        name_pack = "Custom Amount"
        custom = True
        return render(request, 'PhamPhotosApp/purchasepage.html',{'cost':amt,'credits':toke,'deal':name_pack,'cus':custom})
    

def cusamt(request):
    if request.method == 'POST':
        amt = request.POST.get("amt", "")
        
        
        return redirect('./'+amt)


def paymentcomplete(request):
    body = json.loads(request.body)
    print(body)
    tokens = body['credits']
    current_credits = users.objects.values_list('tokens', flat=True).get(user=request.user)
    total = current_credits + float(tokens)
    user = users.objects.all().filter(user_id=request.user.id)
    user.update(tokens=total)
    cost = body['cost']
    database = creditpurchases(user=request.user,creditamount=tokens,cost=cost)
    database.save()
    return redirect('home')
        

    
        
    