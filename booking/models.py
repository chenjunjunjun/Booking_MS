from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Department(models.Model):
    depart_name = models.CharField(max_length=20)
    depart_num = models.CharField(max_length=10)

    def __str__(self):
        return self.depart_name


class Staff(models.Model):
    staff_name = models.CharField(max_length=20)
    staff_number = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    password = models.CharField(max_length=100, default='123456')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.staff_name


class Magazines(models.Model):
    staff = models.ManyToManyField(Staff, blank=True)
    mag_name = models.CharField(max_length=20)
    price = models.FloatField()
    comment = models.TextField(max_length=200, default='', blank=True)
    number = models.CharField(max_length=10)

    def __str__(self):
        return self.mag_name
