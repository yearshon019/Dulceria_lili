from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})
