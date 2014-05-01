from django.db import models

class Picture(models.Model):
    image_path = models.CharField("path", max_length=100)
    image_catagory = models.CharField("catagory", max_length=10)
    image_group = models.CharField("group", max_length=20)
    image_praise = models.IntegerField("praise")
    image_step = models.IntegerField("step") 
    image_upload_date = models.DateTimeField("upload_date_time", auto_now=True)
    image_cover = models.IntegerField("cover")
