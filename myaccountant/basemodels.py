from __future__ import unicode_literals
import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_by = models.ForeignKey(User, related_name='%(class)s_created_on', on_delete=False)
    updated_by = models.ForeignKey(User, related_name='%(class)s_updated_on', on_delete=False)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_by_id = 1
            self.created_on = datetime.datetime.now()
        self.updated_on = datetime.datetime.now()
        self.updated_by_id = 1
        super(BaseModel, self).save(*args, **kwargs)

