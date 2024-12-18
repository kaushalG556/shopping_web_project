from django.urls import path,reverse_lazy
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,PasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
urlpatterns = [
   
    path('',ProductView.as_view(),name='home'),
    
    path('product-detail/<int:pk>', product_detail, name='product-detail'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    
    path('cart/',show_cart,name='showcart'),
    path('pluscart/',plus_cart,name='pluscart'),
    path('minuscart/',minus_cart,name='minuscart'),
    path('removecart/',remove_cart),

    
    path('buy/', buy_now, name='buy-now'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('address/', address, name='address'),
    path('orders/', orders, name='orders'),
    path('mobile/', mobile, name='mobile'),
    path('mobile/<slug:data>',mobile,name='mobiledata'), 
    
    path('laptop/', laptop, name='laptop'),
    path('laptop/<slug:data>',laptop,name='laptopdata'), 

     
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html'\
        ,authentication_form=LoginForm,next_page='home'),name='login'),
    
    
    
    path('logout/',logout, name='logout'),
    
    

    
    path('changepassword/',auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html',\
        form_class=PasswordChangeForm,success_url='/pwdchangedone/'),name='changepassword'),
    
    path('pwdchangedone/',auth_views.PasswordChangeView.as_view(template_name='app/pwdchangedone.html'),\
        name='pwdchangedone'),
    #######################################################
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="app/password_reset.html",
             form_class=MyPasswordResetForm,
             success_url=reverse_lazy('password_reset_done')
         ),
         name="reset_password"),

    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name="app/password_reset_done.html"), 
         name="password_reset_done"),

    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='app/password_reset_confirm.html', 
             success_url=reverse_lazy('password_reset_complete')
         ), 
         name="password_reset_confirm"),

    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="app/password_reset_complete.html"), 
         name="password_reset_complete"),
    
    path('search/',search_products, name='search_results'),

    
    
    
    #######################################################
    
    # path('password-reset/',auth_views.PasswordResetView.\
    #     as_view(template_name='app/password_reset.html',\
    #     form_class=MyPasswordResetForm),name='password_reset'),
    
    # path('password-reset/done/',auth_views.PasswordResetDoneView.\
    #     as_view(template_name='app/password_reset_done.html'),\
    #      name='password_reset_done'),
    
    # path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.\
    #     as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),\
    #      name='password_reset_confirm'),
    
    #  path('password-reset-complete/',auth_views.PasswordResetCompleteView.\
    #     as_view(template_name='app/password_reset_complete.html'),\
    #      name='password_reset_done'),
    
     
    
    
    path('checkout/', checkout, name='checkout'),
    path('paymentdone/',payment_done,name='paymentdone'),
    
    path('registration/',customerregistration.as_view(),name='customerregistration')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
