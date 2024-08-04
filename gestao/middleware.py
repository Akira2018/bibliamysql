# seuapp/middleware.py
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils import timezone
from django.conf import settings
from datetime import datetime

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity_str = request.session.get('last_activity')
            if last_activity_str:
                last_activity = datetime.fromisoformat(last_activity_str)
                if (timezone.now() - last_activity).seconds > settings.SESSION_COOKIE_AGE:
                    logout(request)
                    return redirect('login')  # redirecionar para a página de login
        response = self.get_response(request)
        request.session['last_activity'] = timezone.now().isoformat()
        return response

