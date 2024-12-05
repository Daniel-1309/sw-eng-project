from django.apps import AppConfig


class RegisterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "register"

class YourAppConfig(AppConfig):
    name = 'yourapp'

    def ready(self):
        from register import signals  
