from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    # This will run when the project is reloaded
    def ready(self):
        from main.views import build_index
        from main.views import build_statistical_thesaurus

        # Reload the index on startup
        print('Building the inverted index...')
        build_index()
        print('Done.\n')

        print('Building statistical thesaurus and indexing it...')
        build_statistical_thesaurus()
        print('Done.\n')
