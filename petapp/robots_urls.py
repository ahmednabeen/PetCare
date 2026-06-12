from django.urls import path
from django.http import HttpResponse

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Allow: /",
        "",
        "Sitemap: https://petcare.com/sitemap.xml" if not request.get_host().startswith('127.') else f"Sitemap: http://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

urlpatterns = [
    path('', robots_txt),
]
