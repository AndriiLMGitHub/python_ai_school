from django.shortcuts import render, redirect


def start_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'intro.html', {})


def my_handler404(request, exception):
    return render(request, 'app/404.html')
