from __future__ import unicode_literals
from ..login.models import User
from django.db import models

class quoteManager(models.Manager):
    def quote_Validator(self, postData):
        errors = {}
        if len(postData['quoted_by']) == 0:
            errors['Quoted_by'] = "Person quoted is blank"
        if len(postData['quote']) == 0:
            errors['Quote'] = "Quote is blank"
        return errors
# Create your models here.
class Quotes(models.Model):
    quoted_by = models.CharField(max_length=255)
    quote = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, related_name = "added_quotes")
    faveorited_by = models.ManyToManyField(User, related_name = "faveorites")
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    objects = quoteManager()