from django.db import models

# Create your models here.
class Host(models.Model):
    '''存储所有主机'''
    hostname = models.CharField(max_length=64, blank=True, null=True)
    ip_addr = models.GenericIPAddressField(unique=True)
    port = models.PositiveSmallIntegerField(default=22)
    enabled = models.BooleanField(default=True)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "<{}>{}".format(self.hostname, self.ip_addr)