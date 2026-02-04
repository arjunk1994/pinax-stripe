from importlib.metadata import PackageNotFoundError, version


default_app_config = "pinax.stripe.apps.AppConfig"
try:
    __version__ = version("pinax-stripe")
except PackageNotFoundError:
    __version__ = "0.0.0"
