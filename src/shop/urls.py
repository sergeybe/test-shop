from django.urls import path
from . import views


urlpatterns = [
    path(
        '',
        views.ProductView.as_view(),
        name='all_products_page',
    ),
    path(
        'category/<int:category_id>/',
        views.ProductView.as_view(),
        name='product_page',
    ),
    path(
        'profile/',
        views.ProfileView.as_view(),
        name='profile_page',
    ),
    path(
        'profile/edit/',
        views.ProfileEditView.as_view(),
        name='profile_edit_page',
    ),
    path(
        'cart/',
        views.CartView.as_view(),
        name='cart_page',
    ),
    path(
        'cart/add/',
        views.AddToCartView.as_view(),
        name='add_to_cart',
    ),
    path(
        'cart/clear/',
        views.ClearCartView.as_view(),
        name='clear_cart',
    ),
    path(
        'cart/order/',
        views.OrderCreateView.as_view(),
        name='create_order',
    ),
    path(
        'orders/',
        views.OrderView.as_view(),
        name='orders_page',
    ),
    path(
        'signup/',
        views.RegistrationView.as_view(),
        name='sign_up',
    ),
]
