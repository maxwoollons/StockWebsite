from re import template
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.homey, name='homey'),
    path('login/',auth_views.LoginView.as_view(template_name='PhamPhotosApp/login.html',redirect_authenticated_user=True) , name="login"),
    path('logout/',auth_views.LogoutView.as_view(template_name='PhamPhotosApp/logout.html') , name="logout"),
    path('register/', views.register),
    path('submit/', views.SubmitMedia),
    path('profile/', views.ProfilePage),
    path('<int:pk>',views.PhotoDetail.as_view(template_name='PhamPhotosApp/detailview.html') , name="detail"),
    path('search/', views.search, name='search'),
    path('profile/del/<int:pk>', views.delete, name='delete'),
    path('purchase/<int:pk>', views.purchase, name='buy'),
    path('purchase/success', views.success, name='success'),
    path('credits/', views.credits, name='credits'),
    
    
    
]