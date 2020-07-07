from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from apps.bookmark.models import Bookmark



@login_required
def dashboard(request):

    bookmarks = request.user.bookmarks.all().order_by('-created_at')[0:5]
    categories = request.user.categories.all().order_by('-created_at')[0:5]

    context = {
        'bookmarks': bookmarks,
        'categories': categories
    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required
def settings(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        plan = request.POST.get('plan', '')

        user = request.user

        if username != request.user.username:
            users = User.objects.filter(username=username)

            if len(users):
                messages.error(request, 'The username already exists!')
            else:
                user.username = username

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        user.userprofile.plan = plan
        user.userprofile.save()

        messages.success(request, 'The changes have been saved')

        return redirect('settings')

    return render(request, 'dashboard/settings.html')
