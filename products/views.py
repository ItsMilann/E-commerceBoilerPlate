from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import Product,Refund, Order, OrderProduct, BillingAddress, Payment, OrderStatus, RefCode
from .forms import CheckOutForm, RefundForm
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import stripe
import random
import string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests as req


stripe.api_key = settings.STRIPE_SECRET_KEY

def create_ref_code():
    ref_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return ref_code

class Index(View):
    def get(self, *args, **kwargs):
        object = Product.objects.all()
        context = {'obj':object}
        return render(self.request, 'home.html', context)


class Blog(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'blog_single.html')


class ProductDetailView(View):
    def get(self, request, id=None, *args, **kwargs):
        context = {}
        if id is not None:
            id_= self.kwargs.get('id')
            object = get_object_or_404(Product, id=id_)
            context['obj'] = object
        return render(request, 'product-detail.html', context)


@login_required
def add_to_cart(request, id):  
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=id)
        order_product, created = OrderProduct.objects.get_or_create(
                                                        product=product,
                                                        user=request.user,
                                                        ordered=False)
        order_qs = Order.objects.filter(user=request.user, ordered = False)
        if order_qs.exists():
            order = order_qs[0]
            if order.product.filter(product__id=product.id).exists():
                order_product.quantity += 1
                order_product.save()
                messages.success(request, "Product's quantity updated.")
                return redirect('home')
            else:
                order.product.add(order_product)
                messages.success(request, "This product has been added to your cart.")
        else:
            order = Order.objects.create(user=request.user)
            order.product.add(order_product)
            messages.success(request, "Product added to your cart.")
        return redirect('home')
    else:
        messages.success(request, "Log in to add this item in your cart.")
        return redirect('login')


@login_required
def remove_from_cart(request, id):
    product = get_object_or_404(Product, id=id)
    order_product = OrderProduct.objects.get_or_create(
                                                    product = product,
                                                    user = request.user,
                                                    ordered = False
    )[0]
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.product.filter(product__id=product.id).exists():
            order.product.remove(order_product)
            messages.success(request, "Product removed from your cart.")
            return redirect('cart' )
        else:
            messages.warning(request, 'You do not have this product in your cart.')
    else:
        messages.warning(request, 'You do not have this product in your cart.')
    return redirect('cart' )


@login_required
def plus_one(request, id):  
    product = get_object_or_404(Product, id=id)
    order_product= OrderProduct.objects.get_or_create(
                                                    product=product,
                                                    user=request.user,
                                                    ordered=False)[0]
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.product.filter(product__id=product.id).exists():
            order_product.quantity += 1
            order_product.save()
            messages.success(request, "Product's quantity updated.")
            return redirect('cart')


@login_required
def minus_one(request, id):
    product = get_object_or_404(Product, id=id)
    order_product = OrderProduct.objects.get_or_create(
                                                    product = product,
                                                    user = request.user,
                                                    ordered = False,
                                                    )[0]
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.product.filter(product__id=product.id).exists():
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
                messages.success(request, "Product's quantity updated.")
                return redirect('cart' )
            else:
                order.product.remove(order_product)
                messages.success(request, 'Product removed from your cart.')
                return redirect('cart' )
    else:
        messages.success(request, 'Product removed from your cart.')
        return redirect('cart' )
        

class OrderSummary(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            object = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': object
            }
            return render(self.request, 'products/cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'Your cart is empty.')
            return redirect('home')


class CheckOut(LoginRequiredMixin,View):
    def get(self, *args, **kwagrs):
        form = CheckOutForm()
        context = {
            'form':form
        }
        return render(self.request, 'products/checkout.html', context)

    def post(self, *args, **kwagrs):
        form = CheckOutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered = False)
            if form.is_valid():
                context = {
                    'form':form
                }
                country = form.cleaned_data.get('country')
                town = form.cleaned_data.get('town')
                street_address = form.cleaned_data.get('street_address')
                appartment_address= form.cleaned_data.get('appartment_address')
                zip_code = form.cleaned_data.get('zip_code')
                ship_to_different_address = form.cleaned_data.get('ship_to_different_address')
                save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user = self.request.user,
                    country = country,
                    town = town,
                    street_address = street_address,
                    appartment_address = appartment_address,
                    zip_code = zip_code,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                messages.success(self.request, 'Form subbmitted!')
                if payment_option == 'esewa':
                    return redirect('pay_with_esewa')
                if payment_option == 'stripe':
                    return redirect('pay_with_stripe')
            else:
                messages.warning(self.request, 'Something went wrong!')
                return redirect('checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, 'Something went wrong!')
            return redirect('checkout')
        return render(self.request, 'products/checkout.html', context)


class StripePayment(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context={
                'obj': order
            }
            return render(self.request, 'payment.html', context)
        else:
            messages.warning(self.request, 'Fill up the form first.')
            return redirect('checkout')
    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        total = order.get_grand_total() *100 # amount in cents/paisa
        token = self.request.POST.get('stripeToken')
        ref_code = create_ref_code()
        try:
            charge = stripe.Charge.create(
                amount= total,
                currency='usd', #nrs not supported
                source=token,
                            )
            #createCharge
            payment = Payment()
            payment.charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = total
            payment.payment_method = 'stripe'
            payment.save()
            order_product = order.product.all()
            order_product.update(ordered=True)
            for product in order_product:
                product.save()
            # adding payment to order
            order.payment = payment
            order.ordered =True
            order.reference_code = ref_code
            order.save()
            order_status = OrderStatus()
            order_status.user = self.request.user
            order_status.pre_processing = True
            order_status.save()
            messages.success(self.request, f'Order Successful with reference code: {ref_code}')
            return redirect('home')
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You do not have active order.')
            return redirect('home')
        except stripe.error.CardError as e:
            messages.warning(self.request, 'Card Error!')
            return redirect('pay_with_stripe')
        except stripe.error.RateLimitError as e:
            messages.warning(self.request, 'Too many requests made too quickly')
            return redirect('pay_with_stripe')
        except stripe.error.InvalidRequestError as e:
            messages.warning(self.request, 'Invalid parameters were supplied to Stripe API')
            return redirect('pay_with_stripe')
        except stripe.error.AuthenticationError as e:
        # (maybe you changed API keys recently)
            messages.warning(self.request, "Authentication with Stripe's API failed")
            return redirect('pay_with_stripe')
        except stripe.error.APIConnectionError as e:
            messages.warning(self.request, 'Network communication with Stripe failed')
            return redirect('pay_with_stripe')
        except stripe.error.StripeError as e:
            messages.warning(self.request, 'Something very terrible happended! You were not charged, though.')
            return redirect('pay_with_stripe')
        except Exception as e:
            messages.warning(self.request, 'Something went wrong!')
            return redirect('pay_with_stripe')

class Esewa(View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if order.billing_address:
                order = Order.objects.get(user=self.request.user, ordered=False)
                total = order.get_grand_total()
                ref_code = create_ref_code()
                ref_code_obj = RefCode()
                ref_code_obj.code = ref_code
                ref_code_obj.save()
                url ="https://uat.esewa.com.np/epay/main/"
                d = {'amt': total,
                    'pdc': 0,
                    'psc': 0,
                    'txAmt': 0,
                    'tAmt': total,
                    'pid':str(ref_code),
                    'scd':'epay_payment',
                    'su':'http://http://127.0.0.1:8000/epay_payment_success/',
                    'fu':'http://http://127.0.0.1:8000/esewa_payment_failed/'
                    }
                context = {
                    'obj':order,
                    'd':d
                }
                return render(self.request, 'esewa.html', context)
            else:
                messages.warning(self.request, 'Fill up the form first.')
                return redirect('checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You do not have any existing order.')
            return redirect('home')


def esewa_success(request):
    order = Order.objects.get(user=request.user, ordered=False)
    total = order.get_grand_total()
    ref_code_qs = RefCode.objects.filter('code')
    ref_code = ref_code_qs[0]
    url ="https://uat.esewa.com.np/epay/transrec"
    d = {
        'amt': total,
        'scd': 'epay_payment',
        'rid': str(ref_code),
        'pid':'ee2c3ca1-696b-4cc5-a6be-2c40d929d453',
    }
    resp = req.post(url, d)
    ref_code_qs.delete()
    if resp.status_code == 200:
        order = Order.objects.get(user=request.user, ordered=False)
        total = order.get_grand_total()
        ref_code = create_ref_code()
        payment = Payment()
        payment.user = request.user
        payment.amount = total
        payment.payment_method = 'esewa'
        payment.save()
        order_product = order.product.all()
        order_product.update(ordered=True)
        for product in order_product:
            product.save()
        # adding payment to order
        order.payment = payment
        order.ordered =True
        order.reference_code = ref_code
        order.save()
        order_status = OrderStatus()
        order_status.user = request.user
        order_status.pre_processing = True
        order_status.save()
        messages.success(request, 'Order Succesful!')
        return redirect('home')
    else:
        messages.warning(request, 'Payment verification failed.')
        return redirect('home')

def esewa_failed(request):
    messages.success(request, 'Payment failed! Try again later.')
    return redirect('home')

class RequestRefund(LoginRequiredMixin, View):
    def get(self, *args, **kwagrs):
        form = RefundForm()
        context = {
            'form':form
        }
        return render(self.request, 'refund_request.html', context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            order_status = OrderStatus()
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            try:
                order = Order.objects.get(reference_code = ref_code)
                order.save
                order_status.refund_requested = True
                order_status.save()
                refund=Refund()
                refund.order = order
                refund.message=message
                refund.save()
                messages.info(self.request, 'Request Submitted!')
                return redirect('home')
            except ObjectDoesNotExist:
                messages.warning(self.request, 'Invalid Request!')
                return redirect('home')