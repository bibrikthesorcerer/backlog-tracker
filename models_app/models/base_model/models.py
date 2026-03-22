from django.db import models

class MetaAbstract(models.Model):
    """
    MetaAbstract is an Abstract model which adds common metadata to models.
    """
    created_at = models.fields.DateTimeField(auto_now_add=True)
    updated_at = models.fields.DateTimeField(auto_now=True)
    
    class Meta:
        abstract=True
        
class BaseModel(MetaAbstract):
    """
    BaseModel is an Abstract model from which non-abstract models should inherit instead of Django's models.Model
    """
    class Meta:
        abstract=True