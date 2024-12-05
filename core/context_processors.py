from django.conf import settings


def environment_variables(request):
    return {
        'ENVIRONMENT_DEV': settings.ENVIRONMENT_DEV,
        'ENVIRONMENT_HML': settings.ENVIRONMENT_HML,
        'ENVIRONMENT_PRD': settings.ENVIRONMENT_PRD,
    }
