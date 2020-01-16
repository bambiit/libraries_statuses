from django.db import models
from django.contrib.postgres.fields import JSONField
import json


# Create your models here.
class Libraries(models.Model):
    name = models.TextField(unique=True, null=False)
    description = models.TextField(null=True)
    depends = JSONField(null=True)
    reverse_depends = JSONField(null=True)

    def get_depends_as_array(self):
        if not self.depends:
            return None
        return json.loads(self.depends)

    def get_reverse_depends_as_array(self):
        if not self.reverse_depends:
            return None
        return json.loads(self.reverse_depends)