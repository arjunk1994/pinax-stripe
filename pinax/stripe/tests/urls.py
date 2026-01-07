from django.urls import re_path
from django.contrib import admin

from ..urls import urlpatterns


class FakeViewForUrl(object):
    def __call__(self):
        raise Exception("Should not get called.")


urlpatterns += [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^the/app/$", FakeViewForUrl, name="the_app"),
    re_path(r"^accounts/signup/$", FakeViewForUrl, name="signup"),
    re_path(r"^password/reset/confirm/(?P<token>.+)/$", FakeViewForUrl,
        name="password_reset"),
]
