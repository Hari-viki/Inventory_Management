from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

def validation_quality(value):
    if value>10:
        raise ValidationError('Quality cannot be more than 10')
    
class Inventory_Management(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()
    quality=models.IntegerField(validators=[validation_quality])

    def __str__(self):
        return self.name
    
