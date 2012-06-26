from django.conf import settings
import inspect

def setting(name, default=None):
    """Return setting value for given name or default value.
    As of now, setting can be a callable- e.g. in settings.py:
    def callable_setting(key):
        def inner_fn():
            from site_settings.helpers import get_setting
            return get_setting(key)
        return inner_fn
    THUMBNAIL_SETTING = callable_setting('SOCIAL_AUTH_SETTING')
    """
    ret = getattr(settings, name, default)
    if callable(ret):
        argspec = inspect.getargspec(ret)
        if len(argspec[0])==0:
            ret = ret()
    return ret
