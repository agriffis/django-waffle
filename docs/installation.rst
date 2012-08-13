.. _installation-chapter:

============
Installation
============

To start using Waffle, you just need to add it to your
``INSTALLED_APPS`` and ``MIDDLEWARE_CLASSES``, and make sure to add
the ``request`` context processor::

    TEMPLATE_CONTEXT_PROCESSORS = (
        # ...
        'django.core.context_processors.request',
        # ...
    )

    INSTALLED_APPS = (
        # ...
        'waffle',
        # ...
    )

    MIDDLEWARE_CLASSES = (
        # ...
        'waffle.middleware.WaffleMiddleware',
        # ...
    )

Since Waffle will be setting cookies on response objects, you probably
want it *below* any middleware that tweaks cookies before sending them
out.

If you want to use Waffle in :ref:`JavaScript <javascript-chapter>`,
you'll also need to add it to your root URL config::

    # urls.py

    urlpatterns = patterns('',
        # ...
        (r'^', include('waffle.urls')),
        # ...
    )

And then include the script via the named ``wafflejs`` URL::

    <script src="{% url wafflejs %}"></script>
