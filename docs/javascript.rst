.. _javascript-chapter:

==========================
Using Waffle in JavaScript
==========================

To use Waffle from JavaScript, first follow the :ref:`installation
instructions <installation-chapter>` and add the ``wafflejs`` script tag
to the footer of your pages.

.. warning::
   Be careful of tools like django-compressor_ which might try to minify
   Waffle's JavaScript and concatenate it with other sources. Waffle's
   JS needs to load and run separately for each page view to work
   correctly.

.. _django-compressor: http://django_compressor.readthedocs.org/en/latest/index.html

Once you've loaded the JavaScript, you can use the global ``waffle``
object. Just pass in a Flag, Switch, or Sample name. As in the Python
API, if the object is undefined, it will always be ``false``.

::

    if (waffle.flag('some_flag')) {
        // Flag is active.
    } else {
        // Flag is inactive.
    }

    if (waffle.switch('some_switch')) {
        // Switch is active.
    } else {
        // Switch is inactive.
    }

    if (waffle.sample('some_sample')) {
        // Sample is active.
    } else {
        // Sample is inactive.
    }

``waffle.sample(foo)`` will return the same value *on a given request*
but that value may not persist across multiple requests.
