from django.conf import settings

def debug_mode(request):
    return {'debug': settings.DEBUG}

def mustaches(request):
    return {'mustachify': bool(request.GET.get('mustachify'))}
