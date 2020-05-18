from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    # This will run when the project is reloaded
    def ready(self):
        from main.views import reload_index

        # Reload the index on startup
        print('Building index...')
        reload_index()
        print('Done.\n')
