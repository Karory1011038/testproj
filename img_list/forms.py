import os
from django import forms
from PIL import Image as IMG
from img_list.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', 'url')

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['url'].required = False

    def save_base(self):
        self.save()
        image = Image.objects.last()
        image.get_remote_image()


class ParamsForm(forms.Form):
    width = forms.CharField(max_length=100, label='Ширина', required=False)
    height = forms.CharField(max_length=100, label='Высота', required=False)

    def resize(self, img):
        if self.data['width'] == '':
            size = (10000, int(self.data['height']))
        elif self.data['height'] == '':
            size = (int(self.data['width']), 10000)
        else:
            size = (int(self.data['width']), int(self.data['height']))
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
        return img
