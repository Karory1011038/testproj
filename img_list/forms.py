from django import forms

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
    width = forms.CharField(max_length=100, label='Ширина',required=False)
    height = forms.CharField(max_length=100, label='Высота',required=False)
