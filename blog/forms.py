# https://docs.djangoproject.com/en/4.0/topics/forms/
# https://docs.djangoproject.com/en/4.0/ref/forms/fields/
# https://docs.djangoproject.com/en/4.0/ref/forms/widgets/
# https://docs.djangoproject.com/en/4.0/topics/forms/modelforms/

from django import forms    
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder':'Nome', 'size': 10, 'title': 'Your name' }), 
            'email': forms.EmailInput(attrs={'placeholder':'E-mail',}),
            'body': forms.Textarea(attrs={'placeholder':'Comentário', }),
            }
        labels = {
            'name': (''),
            'email': (''),
            'body': (''),
            }
    

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title' , 'tag', 'body',)
        widgets = {
            'title' : forms.TextInput(attrs={'placeholder':'Título'}),
            'body' : forms.Textarea(attrs={'placeholder' : 'Descrição'}),
            'tag' : forms.Select(attrs={'class' : 'text',})
        }
        labels = {
            'title' : (''),
            'body' : (''), 
        }

        #https://docs.djangoproject.com/en/4.0/ref/models/fields/#error-messages
        error_messages = {
            'title' : {
                'unique' : ('Já existe uma publicação com este título')
            },
        }


    #Validação form customizada
    #https://docs.djangoproject.com/en/4.0/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")

        if Post.objects.filter(title__iexact=title).exists():
            msg = "Já existe uma publicação com este título"
            self.add_error('title', msg)




# Esse form não tem model, por isso é feito apenas com forms.Form
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label='', widget=forms.TextInput(attrs={'placeholder':'Nome'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder':'E-mail de'}))
    to = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder':'E-mail para'}))
    comments = forms.CharField(label='', required=False, widget=forms.Textarea(attrs={'placeholder':'Comentário'}))





