from functools import lru_cache
from naccbis.common.settings import Settings


@lru_cache()
def get_settings():
    return Settings(app_name="api")
