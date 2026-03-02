from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    category = models.CharField(max_length=50)
    tags = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return self.name
