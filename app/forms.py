from django import forms
from .models import UserTable,PostTable,ContactTable
import re

class UserLogForm(forms.ModelForm):
    class Meta:
        model = UserTable
        fields = ['name','email']

    # dp = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control ','placeholder':'Profile pic'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Name'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Email'}))


class UserRegForm(forms.ModelForm):
    class Meta:
        model=UserTable
        fields='__all__'
    dp = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control ','placeholder':'Profile pic'}),required=False)
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control ','placeholder':'Name'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control ','placeholder':'Email'}))



class Post(forms.ModelForm):
    CATEGORY_LIST=(
        ('education','education'),
        ('Knowledge','knowledge'),
        ('entertainment','entertainment'),
        ('fitness','fitness')
    )
    category=forms.ChoiceField(choices=CATEGORY_LIST,widget=forms.Select(attrs={'class':'form-control'}),required=True)
    link=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Copy & paste Embeded Link of the video !'}),required=True)
    def clean_link(self):
        link = self.cleaned_data['link']

        # Define a regular expression pattern to check for the presence of <iframe> tag
        pattern = r'<iframe.*?</iframe>'

        if not re.search(pattern, link):
            raise forms.ValidationError("Link should include an <iframe> tag.")

        return link
    class Meta:
        model=PostTable
        fields=['topic','content','link','category']
    topic=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Topic of the content'}),required=False)
    content=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Message body..'}),required=True)



class ContactForm(forms.ModelForm):
    class Meta:
        model=ContactTable
        fields='__all__'
    email=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    statement=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Statemets'}))

    


#update posts
# write separate form class to update 
# eg:
# class UpdatePost(forms.ModelForm):
#     defined customized field  that you want to update
