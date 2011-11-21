from django.conf import settings

UPLOAD_TO_ARTS = getattr(settings, 'ARTS_UPLOAD_TO_ARTS', 'arts/%Y/%m')
UPLOAD_TO_PORTRAITS = getattr(settings, 'ARTS_UPLOAD_TO_PORTRAITS', 'portraits')

GALLERY_THUMB_SIZES = getattr(settings, 'ARTS_GALLERY_THUMB_SIZES',
                               { 'small': '170x170', 'medium': '600x600' })

if not hasattr(settings, 'AUTH_PROFILE_MODULE'):
    settings.AUTH_PROFILE_MODULE = 'arts.Artist'
