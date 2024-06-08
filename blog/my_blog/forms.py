from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from my_blog.models import Comment


class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget = forms.TextInput(
            attrs = {
                'class':'form-control',
                'id':'inputUsername',
                'type':'username',
                'placeholder':'Имя пользователя'
            }
        )
    )

    password  = forms.CharField(
        required = True,
        widget = forms.TextInput(
            attrs  = {
                'id':'inputPassword',
                'type':'password',
                'placeholder':'Пароль',
                'class':'form-control'
            }
        )
    )

    repeat_password = forms.CharField(
        required=True,
        widget = forms.TextInput(attrs={
            'id':'ReInputPassword',
            'placeholder':'Повторите пароль',
            'class':'form-control',
            'type':'password'
            }
        )
    )

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['repeat_password']

        if password != confirm_password:
            raise forms.ValidationError(
                "Пароли не совпадают"
            )

    def save(self):
        user = User.objects.create_user(
            username = self.cleaned_data['username'],
            password = self.cleaned_data['password'],
        )
        user.save()
        auth = authenticate(**self.cleaned_data)
        return auth


class AuthorizeForm(forms.Form):

    username = forms.CharField(
        max_length=100,
        required=True,
        widget = forms.TextInput(
            attrs= {
            'class': "form-control",
            'id': "inputUsername",
            }
        )
    )
    password = forms.CharField(
        required=True,
        widget = forms.TextInput(
            attrs ={
            'class': "form-control mt-2",
            'id': "inputPassword",
            }
        )
    )

class ContactForm(forms.Form):

    username = forms.CharField(
        max_length=100,
        required=True,
        widget= forms.TextInput(
            attrs={
                'id':'name',
                'class':"form-control",
                'placeholder':"Ваше имя"
            }
        )
    )

    email = forms.CharField(
        required=True,
        widget= forms.TextInput(
            attrs={
                'id':'email',
                'class':"form-control",
                'placeholder':"Ваша почта"
            }
        )
    )

    subject = forms.CharField(
        required=True,
        widget= forms.TextInput(
            attrs={
                'id':"subject",
                'class':"form-control",
                'placeholder':"Тема"
            }
        )
    )

    message = forms.CharField(
        required=True,
        widget= forms.Textarea(
            attrs={
                'id':"message",
                'rows':"5",
                'class':"form-control",
                'placeholder':"Ваше сообщение"
            }
        )
    )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields=('text',)
        widgets={
            'text':forms.Textarea(
                attrs={
                    'row':'3',
                    'class':'form-control mb-3'
                }
            )
        }



