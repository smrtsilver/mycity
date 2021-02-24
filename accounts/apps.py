from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name="کاربران"


    def ready(self):
        import accounts.signals