from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

@login_required
def usuarios_organizacion(request):
    """Vista que muestra usuarios de la misma organización"""
    try:
        # Obtener la organización del usuario actual
        user_org = request.user.userprofile.organization
        
        # Filtrar usuarios que pertenecen a la misma organización
        usuarios_misma_org = User.objects.filter(
            userprofile__organization=user_org
        ).select_related('userprofile', 'userprofile__organization')
        
        context = {
            'usuarios': usuarios_misma_org,
            'organizacion': user_org,
        }
        return render(request, 'core/usuarios_organizacion.html', context)
    
    except AttributeError:
        # Si el usuario no tiene UserProfile asociado
        context = {
            'usuarios': [],
            'organizacion': None,
            'error': 'No tienes una organización asociada. Contacta al administrador.'
        }
        return render(request, 'core/usuarios_organizacion.html', context)

@login_required  
def perfil(request):
    """Vista del perfil del usuario"""
    try:
        user_profile = request.user.userprofile
        context = {
            'user_profile': user_profile,
        }
    except AttributeError:
        context = {
            'user_profile': None,
            'error': 'No tienes un perfil asociado. Contacta al administrador.'
        }
    return render(request, 'core/perfil.html', context)