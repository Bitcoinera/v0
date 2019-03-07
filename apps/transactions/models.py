from django.db import models


class Transaction(models.Model):
    key = models.CharField(max_length=500, blank=False, null=False)
    value = models.CharField(max_length=500, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value

    class Meta:
        ordering = ('created',)

