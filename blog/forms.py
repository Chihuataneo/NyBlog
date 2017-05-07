from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class ShareFileForm(forms.Form):
    title = forms.CharField(max_length=80)
    category = forms.CharField(max_length=80)
    imgurl = forms.CharField(max_length=256)
    introduction = forms.CharField(max_length=500)
    downloadurl = forms.CharField(max_length=256)
