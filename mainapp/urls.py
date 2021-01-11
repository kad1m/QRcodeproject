from django.urls import path
from .views import Index, SecondPage, AddCategory, DownloadQR, EditProduct, DeleteCategory, DeleteProduct, how_it_work, about_us, contact_us, CategoryView,profile, ProductView, MenuView, AddProduct, EditCategory, CategoryDetail, Register, home, stripe_config, create_checkout_session, cancel_subscription, create_checkout_session1, success, cancel, stripe_webhook

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('menu/<int:id>', SecondPage.as_view(), name='second_page'),
    path('profile/', profile, name='profile'),
    path('add-category/', AddCategory.as_view(), name='add_category'),
    path('categories/', CategoryView.as_view(), name='category'),
    path('category-detail/<slug>', CategoryDetail.as_view(), name='category_detail'),
    path('delete-category/<slug>', DeleteCategory.as_view(), name='delete_category'),
    path('add-product/<slug>', AddProduct.as_view(), name='add_product'),
    path('edit-product/<slug>', EditProduct.as_view(), name='edit_product'),
    path('delete-product/<slug>', DeleteProduct.as_view(), name='delete_product'),
    path('product/', ProductView.as_view(), name='product'),
    path('edit-category/<slug>', EditCategory.as_view(), name='edit_category'),
    path('sign-up/', Register.as_view(), name='sign_up'),
    path('menu/<slug>', MenuView.as_view(), name='menu'),
    path('home', home, name='home'),
    path('config/', stripe_config),
    path('create-checkout-session/', create_checkout_session),
    path('create-checkout-session1/', create_checkout_session1),
    path('success/', success),  # new
    path('cancel/', cancel),
    path('webhook/', stripe_webhook),
    path('cancel-sub/', cancel_subscription, name='cancel_subscription'),
    path('about-us/', about_us, name='about_us'),
    path('contact-us/', contact_us, name='contact_us'),
    path('how-it-work/', how_it_work, name='how_it_work'),
    path('download/', DownloadQR.as_view(), name='download'),
]