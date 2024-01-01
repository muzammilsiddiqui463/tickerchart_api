from django.db import models

class Data(models.Model):
    Symbol = models.CharField(max_length=255)
    close = models.CharField(max_length=255)
    volume = models.CharField(max_length=255,default='')
    open = models.CharField(max_length=255)
    high = models.CharField(max_length=255)
    low = models.CharField(max_length=255)

    def __str__(self):
        return self.Symbol
