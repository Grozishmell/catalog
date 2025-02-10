from django import forms
from .models import Review
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, '⭐' * i) for i in range(1, 11)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-stars'})
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль")

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Пароли не совпадают!")

        return cleaned_data
    

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш логин'}),
        label="Логин"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш пароль'}),
        label="Пароль"
    )

    def clean(self):
        cleaned_data = super().clean()  # Получаем очищенные данные
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Аутентификация пользователя без проверки пустых полей
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Неверное имя пользователя или пароль.")

        self.user = user  # Сохраняем пользователя, если он найден
        return cleaned_data

    def get_user(self):
        """Возвращает аутентифицированного пользователя"""
        return getattr(self, 'user', None)