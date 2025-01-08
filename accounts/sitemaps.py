from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import CustomUser

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        # Listați aici toate numele URL-urilor statice din proiect
        return ['index', 'login', 'register', 'profile']

    def location(self, item):
        return reverse(item)

class UserSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return CustomUser.objects.filter(is_active=True)

    def location(self, obj):
        return f'/account/user/{obj.id}/'

    def lastmod(self, obj):
        return obj.date_joined