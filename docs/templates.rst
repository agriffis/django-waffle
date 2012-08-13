.. _templates-chapter:

=========================
Using Waffle in Templates
=========================

Waffle comes with support for Django's built-in template language and
for Jinja2_ via jingo_.


.. _templates-django:

Django Templates
================

You'll need to load the ``waffle_tags`` template tag library, which
brings three block types: ``flag``, ``switch``, and ``sample``. Each of
these takes a single argument, the name of the respective object. For
example::

    {% load waffle_tags %}
    {% flag flag_name %}
      Content if flag is active
    {% endflag %}

All three block types also support an optional ``else`` block::

    {% load waffle_tags %}
    {% switch switch_name %}
      Switch is active!
    {% else %}
      Switch is inactive!
    {% endswitch %}




.. _templates-jinja2:

Jinja2 Templates
================

If you're using Jinja2_ templates via the jingo_ template adapter, then
the Waffle functions should be available automatically as long as
``waffle`` is in your ``INSTALLED_APPS`` list.

In Jinja2 templates, the three functions ``flag``, ``switch``, and
``sample`` are under the ``waffle`` namespace. You can use them with
standard ``{% if %}`` blocks, and they only take the name of the
respective object. For example::

    {% if waffle.flag('my-flag') %}
      My Flag is active!
    {% else %}
      My Flag is inactive!
    {% endif %}


.. _Jinja2: http://jinja.pocoo.org/
.. _jingo: https://github.com/jbalogh/jingo
