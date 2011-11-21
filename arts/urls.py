from django.conf.urls.defaults import *
from django.views.generic import list_detail, date_based

from settings import GALLERY_THUMB_SIZES
from views import manage_art
from models import Art
from forms import UserRegistrationForm, UserAuthenticationForm

art_list = {
    'queryset': Art.objects.all(),
    'allow_empty': False,
    'paginate_by': 9,
    'template_name': 'arts/art_list.html',
    'extra_context': { 'thumb_sizes': GALLERY_THUMB_SIZES },
}

art_detail = {
    'queryset': Art.objects.all(),
    'date_field': 'pub_date',
    'month_format': '%m',
    'slug_field': 'slug',
    'template_name': 'arts/art_detail.html',
    'extra_context': { 'thumb_sizes': GALLERY_THUMB_SIZES },
}

urlpatterns = patterns('',
    (r'^$', list_detail.object_list, art_list),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
            date_based.object_detail, art_detail, name='art_detail'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
            {'authentication_form': UserAuthenticationForm},
            name='registration_login'),
    url(r'^accounts/register/$', 'registration.views.register', 
            {'backend': 'registration.backends.default.DefaultBackend', 
             'form_class': UserRegistrationForm},
            name='registration_register'),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^upload_art/', manage_art,
            {'template_name': 'arts/upload_art.html'},
            name='arts_upload_art'),
    url(r'^edit_art/(?P<art_id>\d+)/$', manage_art, 
            {'template_name':'arts/edit_art.html'},
            name='arts_edit_art'),
    (r'^profiles/', include('profiles.urls')),
)
