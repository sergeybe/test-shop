from functools import wraps
from urllib.parse import urlparse

from django.http import HttpResponsePermanentRedirect


def redirect_to_http(view_func):
    """Decorator that make redirect to http if needs."""
    @wraps(view_func)
    def _wrapped_view_func(request, *args, **kwargs):

        if request.is_secure():
            # Change schema to http and redirect 301
            url = request.build_absolute_uri()
            http_url = urlparse(url)._replace(scheme='http').geturl()

            return HttpResponsePermanentRedirect(http_url)

        return view_func(request, *args, **kwargs)
    return _wrapped_view_func


def redirect_to_https(view_func):
    """Decorator that make redirect to https if needs."""
    @wraps(view_func)
    def _wrapped_view_func(request, *args, **kwargs):

        if not request.is_secure():
            # Change schema to https and redirect 301
            url = request.build_absolute_uri()
            https_url = urlparse(url)._replace(scheme='https').geturl()

            return HttpResponsePermanentRedirect(https_url)

        return view_func(request, *args, **kwargs)
    return _wrapped_view_func
