from __future__ import unicode_literals

from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.category_name.encode('ascii', 'ignore')

    class Meta:
        ordering=['category_name']

class Item(models.Model):
    item_name = models.CharField(max_length=30, unique=True)
    enough = models.BooleanField(default=True)
    category = models.ForeignKey(Category);

    def __str__(self):
        return self.item_name.encode('ascii', 'ignore')

    class Meta:
        ordering = ['item_name']
