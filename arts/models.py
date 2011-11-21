from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from sorl.thumbnail import ImageField

import settings

class Artist(models.Model):
    user = models.OneToOneField(User)
    about = models.TextField()
    portrait = ImageField(upload_to=settings.UPLOAD_TO_PORTRAITS)
    
    @models.permalink
    def get_absolute_url(self):
        return('profiles_profile_detail', None, {
            'username': self.user.username 
        })
    
    def __unicode__(self):
        return u'{0}: {1}'.format(self.user.username, self.user.email)

class Art(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    on_sale = models.BooleanField()
    pub_date = models.DateTimeField('date published', editable=False)
    artist = models.ForeignKey(Artist, related_name='related_artist')
    contributors = models.ManyToManyField(Artist, related_name='related_contributors',
                                          blank=True, null=True)
    slug = models.SlugField()
    image = ImageField(upload_to=settings.UPLOAD_TO_ARTS)
    
    class Meta:
        ordering = ['-pub_date']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return('art_detail', None, {
            'year': self.pub_date.strftime('%Y'),
            'month': self.pub_date.strftime('%m'),
            'day': self.pub_date.strftime('%d'),
            'slug': self.slug
        })
        
    @property
    def artists_html(self):
        html_pattern = u'<a href="mailto:{0}">{1}</a>, '
        html = html_pattern.format(self.artist.user.email, self.artist.user.username)
        for c in self.contributors.all():
            html += html_pattern.format(c.user.email, c.user.username)
        return html[:-2]
 
    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = datetime.now()
        super(Art, self).save(*args, **kwargs)
