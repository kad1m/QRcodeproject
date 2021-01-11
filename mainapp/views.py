from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
import stripe
from django.http import JsonResponse, FileResponse
from .forms import CreateQrCodeForm, CreateQrCodeForMenuForm, CategoryForm, ProductForm
from .models import CafeMenu, Category, Product, Customer, User
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, CustomerForm
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

stripe.api_key = settings.STRIPE_SECRET_KEY


class Index(View):
    def get(self, request):
        return render(request, 'index.html')


class Register(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': RegisterForm(),
        }
        return render(request, 'registration/sign_up.html', context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = self.request.POST['username']
            password = self.request.POST['password1']
            # authenticate user then login
            user = authenticate(username=username, password=password)
            b = Customer(user=user, company_name=self.request.POST['company'])
            b.save()
            login(self.request, user)
            return redirect('category')
        else:
            context = {
                'form': RegisterForm(),
            }
            return render(request, 'registration/sign_up.html', context)


class SecondPage(View):
    def get(self, request, *args, **kwargs):
        object = get_object_or_404(Customer, id=kwargs['id'])
        link2 = request.build_absolute_uri()
        qrcode_image = qrcode.make(link2)
        canvas = Image.new('RGB', (qrcode_image.pixel_size, qrcode_image.pixel_size), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_image)
        fname = f'qr_code-{link2}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        object.qr_code.save(fname, File(buffer))
        canvas.close()
        try:
            subscription = stripe.Subscription.retrieve(object.stripeSubscriptionId)
        except:
            return HttpResponse('oops')
        if subscription.status == 'active':
            products = Product.objects.filter(owner=object)
            categories = Category.objects.filter(owner=object)
            context = {
                'products': products,
                'categories': categories,
                'customer': object,
                'object': object
            }

            return render(request, 'sp.html', context)
        else:
            return render(request, 'oops.html')


class AddCategory(View):
    def get(self, request):
        if request.user.is_authenticated:
            context = {
                'forms': CategoryForm
            }

            return render(request, 'add_category.html', context)
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = CategoryForm(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.owner = Customer.objects.get(user=request.user)
                category.save()
            return redirect('category')
        else:
            return redirect('login')


class CategoryDetail(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            category = Category.objects.get(id=int(kwargs['slug']))
            product = Product.objects.filter(category=category)
            context = {
                'category': category,
                'product': product
            }
            return render(request, 'category-detail.html', context)
        else:
            return redirect('login')


class EditCategory(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            category = Category.objects.get(id=int(kwargs['slug']))
            context = {
                'forms': CategoryForm(instance=category)
            }
            return render(request, 'edit_category.html', context)
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            category = Category.objects.get(id=int(kwargs['slug']))
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                category = form.save(commit=False)
                category.save()
            return redirect('category')
        else:
            return redirect('login')


class DeleteCategory(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            category = Category.objects.get(id=int(kwargs['slug']))
            category.delete()
            return redirect('category')
        else:
            return redirect('login')


class CategoryView(View):
    def get(self, request):
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user.id)
            categories = Category.objects.filter(owner__company_name=customer.company_name)
            context = {
                'categories': categories
            }
            return render(request, 'category_view.html', context)
        else:
            return redirect('login')


class AddProduct(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            category = Category.objects.get(id=int(kwargs['slug']))
            context = {
                'forms': ProductForm,
                'category': category,
            }
            return render(request, 'add_product.html', context)
        else:
            return redirect('login')


    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.owner = Customer.objects.get(user=request.user)
                category = Category.objects.get(id=int(kwargs['slug']))

                product.category = category
                product.save()
            return redirect('category_detail', kwargs['slug'])
        else:
            return redirect('login')


class EditProduct(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product = Product.objects.get(id=int(kwargs['slug']))
            context = {
                'forms': ProductForm(instance=product),
                'product': product
            }
            return render(request, 'edit_product.html', context)
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product = Product.objects.get(id=int(kwargs['slug']))
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
            return redirect('category_detail', product.category.id)
        else:
            return redirect('login')


class DeleteProduct(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product = Product.objects.get(id=int(kwargs['slug']))
            product.delete()
            return redirect('category_detail', product.category.id)
        else:
            return redirect('login')


class ProductView(View):
    def get(self, request):
        if request.user.is_authenticated:
            stripe_customer = Customer.objects.get(user=request.user)
            products = Product.objects.filter(owner=stripe_customer)
            categories = Category.objects.filter(owner=stripe_customer)
            context = {
                'products': products,
                'categories': categories,
                'customer': stripe_customer
            }
            return render(request, 'product_view.html', context)
        else:
            return redirect('login')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.get(company_name=kwargs['slug'])
            products = Product.objects.filter(owner=customer)
            categories = Category.objects.filter(owner=customer)
            context = {
                'products': products,
                'categories': categories
            }

            return render(request, 'product_view.html', context)
        else:
            return redirect('login')


@login_required
def profile(request):
    try:
        # Retrieve the subscription & product
        stripe_customer = Customer.objects.get(user=request.user)

        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)

        product = stripe.Product.retrieve(subscription.plan.product)

        # Feel free to fetch any additional data from 'subscription' or 'product'
        # https://stripe.com/docs/api/subscriptions/object
        # https://stripe.com/docs/api/products/object

        return render(request, 'profile.html', {
            'subscription': subscription,
            'product': product,
            'subscription_end': datetime.fromtimestamp(subscription.current_period_end)
        })

    except:
        stripe_customer = Customer.objects.get(user=request.user)
        return render(request, 'profile.html', {'customer': stripe_customer})


@login_required
def home(request):
    try:
        # Retrieve the subscription & product
        stripe_customer = Customer.objects.get(user=request.user)

        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)

        product = stripe.Product.retrieve(subscription.plan.product)


        # Feel free to fetch any additional data from 'subscription' or 'product'
        # https://stripe.com/docs/api/subscriptions/object
        # https://stripe.com/docs/api/products/object

        return render(request, 'home.html', {
            'subscription': subscription,
            'product': product,
            'subscription_end': datetime.fromtimestamp(subscription.current_period_end)
        })
    except:
        print('no user')
        return render(request, 'home.html')


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID,
                        'quantity': 1,

                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def create_checkout_session1(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID2,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@login_required
def success(request):
    return render(request, 'success.html')


@login_required
def cancel(request):
    return render(request, 'cancel.html')


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        # Get the user and create a new StripeCustomer
        user = User.objects.get(id=client_reference_id)
        customer = Customer.objects.get(user=user)
        customer.stripeCustomerId = stripe_customer_id
        customer.stripeSubscriptionId = stripe_subscription_id
        customer.save()

        print(user.username + ' just subscribed.')

    return HttpResponse(status=200)


@login_required()
def cancel_subscription(request):
    if request.user.is_authenticated:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        customer = Customer.objects.get(user=request.user.id)
        res = stripe.Subscription.delete(customer.stripeSubscriptionId)
        if res.status == 'canceled':
            customer.stripeSubscriptionId = ''
            customer.save()
            return render(request, 'cancel.html')
        else:
            return HttpResponse('oops')
    else:
        return redirect('login')


def about_us(request):
    return render(request, 'about-us.html')


def contact_us(request):
    return render(request, 'contact-us.html')


def how_it_work(request):
    return render(request, 'gallery.html')


class DownloadQR(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user.id)
            if customer.stripeSubscriptionId:
                file = open(customer.qr_code.path, 'rb')
                response = FileResponse(file, content_type='application/force-download')
                return response
            else:
                return redirect('home')
        else:
            return redirect('login')
