from django import forms
from django.conf import settings


# class ProfileImageUploadWidget(forms.FileInput):

class ProfileImageUploadForm(forms.Form):
    upload_image = forms.ImageField(widget=forms.FileInput(attrs={'accept': 'image/png, image/gif, image/jpeg'}), required=True)

    def clean_upload_image(self):
        upload_image = self.cleaned_data.get('upload_image')
        if upload_image.size > settings.MAX_IMAGE_SIZE:
            raise forms.ValidationError(
                f'Максимальный размер загружаемых фотографий не может превышать {settings.MAX_IMAGE_SIZE}MB')
        return upload_image