from django.apps import AppConfig


class TrackerConfig(AppConfig):
    name = "tracker"

    def ready(self):
        # import audit module to register signal handlers
        try:
            from . import audit  # noqa: F401
        except Exception:
            pass
