import os
import urllib
import uuid
from io import BytesIO

from django.core.files import File
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.shortcuts import render
from img_list.forms import ImageForm, ParamsForm
from img_list.models import Image
from PIL import Image as IMG

from urllib import request


def homepage(request):
    images = Image.objects.all()
    exist = False
    if len(images) == 0:
        exist = True
    return render(request, 'img_list/homepage.html', {'images': images, 'exist': exist})


def add(request):
    status = False
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid() and (form.files.__len__() == 0 or form.data['url'] == ''):
            form.save_base()
            return HttpResponseRedirect('homepage')
        else:
            status = True
    else:
        form = ImageForm()

    return render(request, 'img_list/add.html', {
        'form': form,
        'status': status
    })


def pic(request, id):
    images = Image.objects.all()
    img = images[id - 1]
    if request.method == 'POST':
        form = ParamsForm(request.POST)
        if form.is_valid() and (form.data['width'] != '' or form.data['height'] != ''):
            if form.data['width'] == '':
                size = (10000, int(form.data['height']))
            elif form.data['height'] == '':
                size = (int(form.data['width']), 10000)
            else:
                size = (int(form.data['width']), int(form.data['height']))
            im1 = IMG.open(img.image)
            if os.path.isfile('media/resized_' + img.image.name):
                os.remove('media/resized_' + img.image.name)
            source_image = im1.convert('RGB')
            source_image.thumbnail(size, IMG.ANTIALIAS)  # Resize to size
            source_image.save('media/resized_' + img.image.name, format='JPEG')  # Save resize image to bytes
            img = {
                'image': {
                    'name': img.image.name,
                    'url': '/media/resized_' + img.image.name
                }
            }
    else:
        form = ParamsForm()

    return render(request, 'img_list/pic.html', {'image': img, 'form': form})
