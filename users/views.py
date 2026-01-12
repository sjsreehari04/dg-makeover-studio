from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'ADMIN':
            return redirect('dg_admin_dashboard')
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # 🔑 ROLE-BASED REDIRECT (THIS IS THE KEY)
            if user.role == 'ADMIN':
                return redirect('dg_admin_dashboard')
            else:
                return redirect('dashboard')

        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'login.html')
