from django.db import models

class Data(models.Model):
    Symbol = models.CharField(max_length=255)
    close = models.CharField(max_length=255)
    volume = models.CharField(max_length=255,default='')
    open = models.CharField(max_length=255)
    high = models.CharField(max_length=255)
    low = models.CharField(max_length=255)
    added = models.DateTimeField(auto_now_add=True)  # Add this line

    def __str__(self):
        return f"{self.Symbol} - {self.added}"
