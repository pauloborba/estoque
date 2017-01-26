from __future__ import unicode_literals

from django.db import models

class Item(models.Model):
    item_name = models.CharField(max_length=30)
    qty = models.IntegerField()

    def __str__(self):
        return self.item_name.encode('ascii', 'ignore')

    class Meta:
        ordering = ['item_name']
