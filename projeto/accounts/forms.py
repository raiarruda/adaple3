from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
User = get_user_model()


class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmação de Senha', widget=forms.PasswordInput
    )
    
    def add_to_group(User):
        grupo_aluno, criado = Group.objects.get_or_create(name='aluno')
        user.group.add()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise formsy.ValidationError('A confirmação não está correta')
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            #adicina no grupo mas retorna erro
            #grupo_aluno, criado = Group.objects.get_or_create(name='aluno')
            #grupo_aluno.user_set.add(user)
            
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email']
