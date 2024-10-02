from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import News, Comment
from .forms import NewsForm, CommentForm

# Вью для отображения списка новостей
def news_list(request):
    news = News.objects.all().order_by('-created_at')
    return render(request, 'news/news_list.html', {'news': news})

# Вью для отображения детальной информации о новости
def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    comments = Comment.objects.filter(news=news_item).order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news_item
            comment.created_at = timezone.now()
            comment.save()
            return redirect('news_detail', pk=news_item.pk)
    else:
        form = CommentForm()

    return render(request, 'news/news_detail.html', {'news_item': news_item, 'comments': comments, 'form': form})

# Вью для добавления новой новости
def news_add(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.created_at = timezone.now()
            news.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm()
    return render(request, 'news/news_add.html', {'form': form})