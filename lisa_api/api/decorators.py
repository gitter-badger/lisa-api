from lisa_api.lisa.logger import logger
from rest_framework.reverse import reverse_lazy


def add_intent(intent):
    """
    Add an intent for the route
    """

    def decorator(a_view):

        # def _wrapped_view(request, *args, **kwargs):
        logger.debug(reverse_lazy(a_view))
        #    return a_view(request, *args, **kwargs)
        return a_view
    return decorator
