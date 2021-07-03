import os
from urllib import request

from django.core.files import File
from django.db import models


# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='', verbose_name='Файл', null=True)
    url = models.CharField(max_length=250, verbose_name='Ссылка', null=True)

    def get_remote_image(self):
        if self.url and not self.image:
            result = request.urlretrieve(self.url)
            self.image.save(
                    os.path.basename(self.url),
                    File(open(result[0], 'rb'))
                    )
            self.save()
