from django.db import models

class ProxyIp(models.Model):
    ip=models.CharField("IP",primary_key=True,max_length=20)
    port=models.CharField("PORT",max_length=5)
    time=models.CharField("time",max_length=30)
    def __str__(self):
        return self.ip
    def to_dict(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
