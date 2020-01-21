from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns =[
    path('', views.Index.as_view(), name='home'),
    path('accounts/logout', user_views.logout_view, name = 'loggout'),
    path('accounts/profile/', user_views.ProfileView.as_view(), name= 'profile'),
    path('accounts/register/', user_views.Register.as_view(), name= 'signup'),
    path('accounts/profile/update/', user_views.ProfileUpdateView.as_view(), name= 'profile_update'),
    path('<int:id>/', views.ProductDetailView.as_view(), name = 'product_detail'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name = 'add_to_cart'),
    path('minus-one/<int:id>/', views.minus_one, name = 'minus_one'),
    path('plus-onet/<int:id>/', views.plus_one, name = 'plus_one'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name = 'remove_from_cart'),
    path('cart/', views.OrderSummary.as_view(), name = 'cart'),
    path('checkout/', views.CheckOut.as_view(), name = 'checkout'),
    path('checkout/stripe/', views.StripePayment.as_view(), name = 'pay_with_stripe'),
    path('checkout/esewa/', views.Esewa.as_view(), name = 'pay_with_esewa'),
    path('refund/', views.RequestRefund.as_view(), name = 'refund'),
    path('blog/', views.Blog.as_view(), name = 'blog'),
    path('esewa_payment_failed/', views.esewa_failed, name = 'esewa_failed'),
    path('esewa_payment_success/', views.esewa_success, name = 'esewa_success'),
    path('search_results/', views.MakeQuery.as_view(), name = 'search_results')
]

if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
