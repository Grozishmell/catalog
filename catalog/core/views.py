from rest_framework import viewsets, permissions
from .serializers import ItemSerializer, ReviewSerializer
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Review, List_Items
from .forms import ReviewForm, RegisterForm, LoginForm
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q


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


def user_list_items(request):
    # Получаем фильтры и сортировку из запроса
    status_filter = request.GET.get('status', None)
    sort_order = request.GET.get('sort', 'asc')  # По умолчанию сортировка по возрастанию

    # Строим фильтр
    filter_conditions = Q(user=request.user)

    if status_filter and status_filter != 'not_watched':  # Исключаем "не смотрю"
        filter_conditions &= Q(status=status_filter)

    # Получаем все элементы, применяя фильтрацию
    user_items = List_Items.objects.filter(filter_conditions).select_related('item', 'review')

    # Сортируем
    if sort_order == 'desc':
        user_items = user_items.order_by('-item__release_date')  # по убыванию
    else:
        user_items = user_items.order_by('item__release_date')  # по возрастанию

    return render(request, 'core/profile.html', {'user_items': user_items})


def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    reviews = item.reviews.all().order_by('-created_at')  # Все отзывы, сортируем по дате
    average_rating = item.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    form = ReviewForm()

    user_review = None
    list_item_status = None  # Переменная для статуса пользователя

    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        if user_review:
            reviews = reviews.exclude(id=user_review.id)  # Убираем его из общего списка

        # Получаем статус для текущего пользователя
        list_item = List_Items.objects.filter(user=request.user, item=item).first()
        if list_item:
            list_item_status = list_item.status  # Статус пользователя для этого элемента

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('account_login')

        if user_review:
            messages.error(request, "Вы уже оставили отзыв.")
            return redirect('item_detail', item_id=item.id)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.user = request.user
            review.save()

            # Обновляем статус на "просмотрен", если нет отзыва
            status = 'watched'  # Устанавливаем статус "просмотрен"
            List_Items.objects.get_or_create(user=request.user, item=item, status=status)

            return redirect('item_detail', item_id=item.id)
        else:
            print(form.errors)

    return render(request, 'core/item_detail.html', {
        'item': item,
        'reviews': reviews,
        'average_rating': round(average_rating, 1),
        'form': form if request.user.is_authenticated and not user_review else None,
        'user_review': user_review,
        'list_item_status': list_item_status,
        'range': range(10),  # передаем range для звездочек
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


@login_required
def update_item_status(request, item_id):
    if request.method == 'POST' and request.content_type == 'application/json':
        import json
        data = json.loads(request.body)
        status = data.get('status')
        
        # Статус должен быть не равен "не смотрю"
        if status == 'not_watched':
            return JsonResponse({'success': False, 'message': 'Не можете установить статус "Не смотрю"'})

        item = get_object_or_404(Item, id=item_id)

        # Проверяем, есть ли уже запись о статусе фильма для этого пользователя
        list_item, created = List_Items.objects.get_or_create(user=request.user, item=item)

        # Если запись существует, обновляем статус
        if not created:
            list_item.status = status
            list_item.save()

        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)
