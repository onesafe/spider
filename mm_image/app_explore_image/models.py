from django.db import models

class Picture(models.Model):
    image_name = models.CharField("name", max_length=50)
    image_praise = models.IntegerField("praise")
    image_step = models.IntegerField("step") 
    image_upload_date = models.DateTimeField("upload_date_time", auto_now=True)
