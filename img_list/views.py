from django.http import HttpResponseRedirect
from django.shortcuts import render
from img_list.forms import ImageForm, ParamsForm
from img_list.models import Image


def homepage(request):
    images = Image.objects.all()
    not_exist = False
    if len(images) == 0:
        not_exist = True
    return render(request, 'img_list/homepage.html', {'images': images, 'not_exist': not_exist})


def add(request):
    status = False
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid() and (len(form.files) == 0 or form.data['url'] == '') and (len(form.files) != 0 or form.data['url'] != ''):
            form.save_base()
            return HttpResponseRedirect('/')
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
            img = form.resize(img)
    else:
        form = ParamsForm()

    return render(request, 'img_list/pic.html', {'image': img, 'form': form})
