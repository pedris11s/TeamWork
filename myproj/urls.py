from django.conf.urls import include, url
from django.contrib import admin
#from django_pdfkit import PDFView

urlpatterns = [
    url(r'^teamwork/', include('teamwork.urls')),
    url(r'^admin/', admin.site.urls),
    #url(r'^mypdf/$', PDFView.as_view(template_name='404.html'), name='my-pdf'),
]