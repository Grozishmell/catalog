from rest_framework import viewsets, permissions
from .serializers import ItemSerializer, ReviewSerializer
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Review
from .forms import ReviewForm, RegisterForm, LoginForm
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


def home(request):
    items = Item.objects.all()
    return render(request, 'core/home.html', {'items' : items})


def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    reviews = item.reviews.all()
    average_rating = item.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    form = ReviewForm()

    # Проверяем, есть ли у аутентифицированного пользователя отзыв на этот предмет
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('account_login')
        
        # Если пользователь уже оставил отзыв, не обрабатываем форму
        if user_review:
            messages.error(request, "Вы уже оставили отзыв.")
            return redirect('item_detail', item_id=item.id)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.user = request.user
            review.save()
            return redirect('item_detail', item_id=item.id)
        else:
            print(form.errors)  # Выведет ошибки формы в консоль

    return render(request, 'core/item_detail.html', {
        'item': item,
        'reviews': reviews,
        'average_rating': round(average_rating, 1),
        'form': form if request.user.is_authenticated and not user_review else None,  # форма только для аутентифицированных пользователей, которые не оставили отзыв
        'user_review': user_review
    })



def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()  # создаем пустую форму при GET-запросе

    return render(request, "core/register.html", {"form": form})
    

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)  # Важно передавать request
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            print(form.errors)  # Выводим ошибки формы в консоль
            messages.error(request, "Ошибка валидации формы.")
    else:
        form = LoginForm()

    return render(request, "core/login.html", {"form": form})

    

@login_required
def logout_view(request):
    logout(request)
    return redirect("home")