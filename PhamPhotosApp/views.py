from django.contrib.auth.models import User
from django.forms.widgets import Media
from django.http import request
from django.shortcuts import redirect, render
from .forms import UserRegistrationForm, MediaSubmit, VideoSubmit, ExchangeSubmit
from django.contrib import messages
from .models import photos, purchases, users, payments, creditpurchases, videos, videopurchases, exchange, savedphoto, savedvideo
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
    Media = photos.objects.all().filter(approved=True).order_by('?')[:30]
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
        form2 = VideoSubmit(request.POST,request.FILES)
        form = MediaSubmit(request.POST, request.FILES)
        if form.is_valid():
            ob = form.save(commit=False)
            ob.owner = request.user
            ob.price = 50
            ob.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'account created for {username}!')
            return redirect('home')
        if form2.is_valid():
            ob = form2.save(commit=False)
            ob.owner = request.user
            ob.price = 100
            ob.save()
            username = form2.cleaned_data.get('username')
            messages.success(request, f'account created for {username}!')
            return redirect('video')
    else:
        form = MediaSubmit()
        form2 = VideoSubmit()
    return render(request, 'PhamPhotosApp/submit.html', {'form':form,'form2':form2})


@login_required
def ProfilePage(request):
   # photo_ids = photos.objects.all().filter(owner_id=request.user.id)
   # pic_owner = purchases.objects.values_list('price', flat=True).get(id=pk)
    user = User.objects.all().filter(id=request.user.id)
    purchase = purchases.objects.all().filter(User=request.user.users).order_by('-id')
    purchasess = purchases.objects.all()
    uploads = photos.objects.all().filter(owner=request.user).order_by('-id')
    payment = payments.objects.all().filter(user=request.user).order_by('-id')
    credits = creditpurchases.objects.all().filter(user=request.user).order_by('-id')

    #video short_description


    videopurchase = videopurchases.objects.all().filter(User=request.user.users).order_by('-id') #video purchases
    videoupload = videos.objects.all().filter(owner=request.user).order_by('-id') #video uploads
   


  
    if payment.exists():
        if credits.exists():
            return render(request, 'PhamPhotosApp/profile.html', {'profile':user,'uploads':uploads,'pur':purchase,'num':purchasess,'items':payment,'creditss':credits,'videopurchase':videopurchase,'videoupload':videoupload})

        else:
            credits = False
            return render(request, 'PhamPhotosApp/profile.html', {'profile':user,'uploads':uploads,'pur':purchase,'num':purchasess,'items':payment,'creditss':credits,'videopurchase':videopurchase,'videoupload':videoupload})

    else:
        payment = False
        return render(request, 'PhamPhotosApp/profile.html', {'profile':user,'uploads':uploads,'pur':purchase,'num':purchasess,'items':payment,'creditss':credits,'videopurchase':videopurchase,'videoupload':videoupload})
    
    



class PhotoDetail(DetailView):
   
    context_object_name='obj'
    template_name="detailview.html"
    model = photos
    
    
def search(request):
        if request.method == 'GET' and request.GET.get('search'):
            search = request.GET.get('search')
            record = photos.objects.all().filter(title__icontains=search,approved=True).order_by('?')
            amt = len(record)
            return render(request, 'PhamPhotosApp/search.html',{'all':record, 'amount':amt,'search':search})
    
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
    
    if request.user.id != pic_owner:
        if cost <= tokens:
            commission = cost*40/100
            onew = otokens + (cost - commission)
            paied = cost-commission
            new = tokens - cost
            user.update(tokens=new)
            p = videopurchases(User=request.user.users,Photo_id=pk,downloaded=False,paied=paied)
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
    
    tokens = body['credits']
    current_credits = users.objects.values_list('tokens', flat=True).get(user=request.user)
    total = current_credits + float(tokens)
    user = users.objects.all().filter(user_id=request.user.id)
    user.update(tokens=total)
    cost = body['cost']
    database = creditpurchases(user=request.user,creditamount=tokens,cost=cost)
    database.save()
    return redirect('home')
        
def video(request):
    vids = videos.objects.all().filter(approved=True).order_by('?')#here
    return render(request, 'PhamPhotosApp/video.html',{'vids':vids})



class VideoDetail(DetailView):
   
    context_object_name='obj'
    template_name="videodetail.html"
    model = videos

@login_required
def vidpurchase(request,pk):
    tokens = request.user.users.tokens
    user = users.objects.all().filter(user_id=request.user.id)
    pic_owner = videos.objects.values_list('owner_id', flat=True).get(id=pk)
    cost = videos.objects.values_list('price', flat=True).get(id=pk)
    ouser = users.objects.all().filter(user_id=pic_owner) #
    owneruser = User.objects.get(id=pic_owner) #
    title = videos.objects.values_list('title', flat=True).get(id=pk)
    otokens = users.objects.values_list('tokens', flat=True).get(user=pic_owner)
  
    if request.user.id != pic_owner:
        if cost <= tokens:
            commission = cost*40/100
            onew = otokens + (cost - commission)
            paied = cost-commission
            new = tokens - cost
            user.update(tokens=new)
            p = videopurchases(User=request.user.users,video_id=pk,downloaded=False,paied=paied)
            p.save()
            
            ouser.update(tokens=onew)
            q = payments(user=owneruser,amount=paied,title=title)
            q.save()
            
            return redirect('success')
        else:
            return redirect('home')
             
             
            
    else:
        return redirect('home')
    


def delvid(request, pk):
    if videos.objects.all().filter(id=pk,owner=request.user):
        vid = videos.objects.all().filter(id=pk,owner=request.user)
        vid.delete()
        return render(request, 'PhamPhotosApp/delete.html') 
    else:
        redirect('home')

    
def searchvid(request):
        if request.method == 'GET' and request.GET.get('search'):
            search = request.GET.get('search')
            record = videos.objects.all().filter(title__icontains=search,approved=True)
            amt = len(record)
            return render(request, 'PhamPhotosApp/searchvid.html',{'all':record, 'amount':amt,'search':search})




def profsearch(request,pk):
    owner_user = User.objects.get(id=pk)
    photo = photos.objects.all().filter(owner_id=pk,approved=True)
    video = videos.objects.all().filter(owner_id=pk,approved=True)
    amt = len(photo)+len(video)
    return render(request, 'PhamPhotosApp/profilesearch.html',{'vid':video, 'pic':photo, 'userr':owner_user,'amt':amt})
        
    
@login_required
def exchangepage(request):
    tokens = users.objects.values_list('tokens', flat=True).get(user_id=request.user.id)
    worth = tokens / 100 * 0.50
    past = exchange.objects.all().filter(user=request.user)
    if request.method == 'POST':
        form = ExchangeSubmit(request.POST)
        
        if form.is_valid():
            
            amount = form.cleaned_data.get('amount')
            tokens = users.objects.values_list('tokens', flat=True).get(id=request.user.id)
            print(amount)
            print(tokens)
            if amount >= 50:
                if amount <= worth:
                    ob = form.save(commit=False)
                    ob.user = request.user
                    ob.save()
                    return redirect('exchange')
                else:
                    return redirect('exchange')
            else:
                return redirect('exchange')
    else:
        form = ExchangeSubmit()
    return render(request, 'PhamPhotosApp/exchange.html',{'form':form,'tokens':tokens,'worth':worth,'past':past})



def deleteex(request,pk):
    if exchange.objects.all().filter(id=pk,user=request.user):
        img = exchange.objects.all().filter(id=pk,user=request.user)
        img.delete()
        return redirect('exchange')
    else:
        return redirect('exchange')


def cat(request,pk):
    cat = pk
    photo = photos.objects.all().filter(category__icontains=pk,approved=True).order_by('?')
    return render(request, 'PhamPhotosApp/cat.html', {'cat':cat,'photos':photo})


def vcat(request,pk):
    cat = pk
    video = videos.objects.all().filter(category__icontains=pk,approved=True).order_by('?')
    return render(request, 'PhamPhotosApp/vcat.html', {'cat':cat,'photos':video})


def psave(request,pk):
    photo_id = pk
    user = request.user
    if savedphoto.objects.all().filter(user=user,image_id=photo_id):
        return redirect('saved')
    else:
    
        h = savedphoto(user=user,image_id=photo_id)
        h.save() 
        return redirect('saved')
    
@login_required
def saved(request):
    user = request.user
    img = savedphoto.objects.all().filter(user=user) 
    vid = savedvideo.objects.all().filter(user=user) 
    
    return render(request, 'PhamPhotosApp/saved.html',{'photo':img,'video':vid})


def vsave(request,pk):
    photo_id = pk
    user = request.user
    if savedvideo.objects.all().filter(user=user,image_id=photo_id):
        return redirect('saved')
    else:
    
        h = savedvideo(user=user,image_id=photo_id)
        h.save() 
        return redirect('saved')
    
    
def dsp(request,pk):
    if savedphoto.objects.all().filter(id=pk,user=request.user):
        img = savedphoto.objects.all().filter(id=pk,user=request.user)
        img.delete()
        return redirect('saved')
    else:
        return redirect('saved')
    
    
def dsv(request,pk):
    if savedvideo.objects.all().filter(id=pk,user=request.user):
        img = savedvideo.objects.all().filter(id=pk,user=request.user)
        img.delete()
        return redirect('saved')
    else:
        return redirect('saved')