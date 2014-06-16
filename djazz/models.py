from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Post(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    uid = models.SlugField(max_length=150, null=True, blank=True)
    author = models.ForeignKey(User, related_name="post_author",
                               null=True, blank=True,
                               on_delete=models.SET_NULL)
    date_create = models.DateTimeField()
    last_editor = models.ForeignKey(User, related_name="post_editor",
                                    null=True, blank=True,
                                    on_delete=models.SET_NULL)
    date_update = models.DateTimeField()
    content = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)
    formatter = models.CharField(max_length=150, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    
    def __unicode__(self):
        unic = "%d" % self.id
        if self.title:
            unic += " - %s" % str(self.title)
        return unic
    
    def get_formatter(self):
        from .formatters import get_formatter
        
        if not self.formatter:
            return None
        
        return get_formatter(self.formatter)
