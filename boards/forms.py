from django import forms
from .models import Topic,Post

class NewTopicForm(forms.ModelForm):
    subject = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Teclea asunto'}),
        required=True,
        max_length=255,
        help_text='Como máximo 255 carcteres.')
    message = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 5, 'placeholder': 'Qué tienes en mente?'}), 
        max_length=4000,
        required=True,
        help_text='Como máximo 4000 caracteres.')

    class Meta:
        model = Topic
        fields = ['subject', 'message']

    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message',]