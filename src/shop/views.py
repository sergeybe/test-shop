import logging

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.forms import Form
from django.db import transaction
from django.views.generic import (
    TemplateView, ListView, FormView, CreateView, UpdateView
)
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme

from .models import Product, Order
from .forms import AddToCartForm, RegistrationForm, OrderForm, ProfileEditForm
from .decorators import redirect_to_http, redirect_to_https

logger = logging.getLogger(__name__)


class RedirectFieldNameMixin:
    """Mixin for redirect query field."""
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_success_url(self):
        """Get success url from redirect field."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '/')
        )

        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=(
                self.request.get_host(),
            ),
            require_https=self.request.is_secure(),
        )

        return redirect_to if url_is_safe else '/'


class RegistrationView(CreateView):
    """Registration View."""
    form_class = RegistrationForm
    template_name = 'shop/sign_up_page.html'
    success_url = reverse_lazy('profile_page')


@method_decorator(redirect_to_http, name='get')
class ProductView(ListView):
    """Production View."""
    template_name = 'shop/product_page.html'
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()

        category_id = self.kwargs.get('category_id')

        if category_id:
            queryset = queryset.filter(category__id=category_id)

        return queryset.select_related('category')


@method_decorator(redirect_to_https, name='get')
@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    """Profile View."""
    template_name = 'shop/profile_page.html'


@method_decorator(redirect_to_http, name='get')
@method_decorator(login_required, name='dispatch')
class ProfileEditView(UpdateView):
    """Profile edit view."""
    template_name = 'shop/profile_edit_page.html'
    form_class = ProfileEditForm
    success_url = reverse_lazy('profile_page')

    def get_object(self, queryset=None):
        return self.request.user


class CartView(ListView):
    """Cart view."""
    template_name = 'shop/cart_page.html'
    model = Product

    def get_queryset(self):
        """Get cart from session and construct queryset with quantity."""
        queryset = super().get_queryset()

        try:
            cart = self.request.session['cart']
        except KeyError:
            cart = {}

        queryset = queryset.filter(
            id__in=cart.keys()
        ).select_related(
            'category'
        )

        # Ugly but easy.

        for item in queryset:
            item.quantity = cart[str(item.id)]

        return queryset


class AddToCartView(RedirectFieldNameMixin, FormView):
    """View for add product to view."""
    http_method_names = ['post', 'options']
    form_class = AddToCartForm

    def form_valid(self, form):
        """Process valid form."""
        # Use model form only validation and save in session instead of db.
        # This is simplest way to make it. Of course in the real world
        # we should use models like Cart and CartItem.

        self.save_product_in_cart(
            form.cleaned_data['product_id'],
            form.cleaned_data['quantity'],
        )

        logger.debug(
            'AddToCartView.form_valid %r, %r',
            form.cleaned_data,
            self.request.session,
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        """Process invalid form."""
        # Doing as valid. Silence is golden :)
        logger.warning('AddToCartView.form_invalid %r', form.errors)
        return super().form_valid(form)

    def save_product_in_cart(self, product_id, quantity):
        """Save product in session."""
        try:
            cart = self.request.session['cart']
        except KeyError:
            cart = {}

        # Serializer of session works correctly only with str.
        product_id = str(product_id)

        try:
            cart[product_id] += quantity
        except KeyError:
            cart[product_id] = quantity

        self.request.session['cart'] = cart


class ClearCartView(RedirectFieldNameMixin, FormView):
    """View to clear cart."""
    http_method_names = ['post', 'options']
    form_class = Form

    def form_valid(self, form):
        """Process valid form."""
        self.request.session['cart'] = {}
        return super().form_valid(form)

    def form_invalid(self, form):
        """Process invalid form."""
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class OrderCreateView(CreateView):
    """View for create order from cart."""
    template_name = 'shop/create_order_page.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders_page')

    def get_initial(self):
        """Return the initial data from user profile."""
        initial = super().get_initial()

        initial.update(
            self.request.user.get_for_checkout()
        )

        return initial

    def clear_cart(self):
        """Clear cart."""
        self.request.session['cart'] = {}

    @transaction.atomic
    def form_valid(self, form):
        """Process valid form."""
        order = form.save(commit=False)
        order.user = self.request.user
        order.save()

        try:
            cart = self.request.session['cart']
        except KeyError:
            # TODO: Does cart is empty?
            return super().form_valid(form)

        for product_id, quantity in cart.items():
            order.orderitem_set.create(
                product_id=product_id,
                quantity=quantity,
            )

        # Clear cart on commit
        transaction.on_commit(lambda: self.clear_cart())

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class OrderView(ListView):
    """View for order list."""
    template_name = 'shop/orders_page.html'
    model = Order

    def get_queryset(self):
        """Get queryset of orders."""
        queryset = super().get_queryset()

        queryset = queryset.filter(
            user=self.request.user
        ).select_related(
            'user',
        )

        return queryset
