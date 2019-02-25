from django.db import models

# Create your models here.

class Source(models.Model):
    url = models.URLField(max_length=255, unique=True)
    name = models.CharField(max_length=64)

    def __repr__(self):
        return "<Source '{}'>".format(self.url)