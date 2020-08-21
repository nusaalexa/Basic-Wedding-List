from django.contrib.auth.models import User
from django.db import models


class Gift(models.Model):
    name = models.CharField(max_length=250)
    brand = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    purchased = models.BooleanField(default=False)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name


class GiftList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list_name = models.CharField(max_length=250)
    gift = models.ManyToManyField(Gift)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('list_name',)

    def __str__(self):
        return "{} : {}".format(self.id, self.list_name)
