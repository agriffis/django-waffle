.. _settings-chapter:

===============
Global Settings
===============

There are a few global settings you can define to adjust Waffle's
behavior.


``WAFFLE_COOKIE``:
    The format for the cookies Waffle sets. Must contain
    ``%s``. Defaults to ``dwf_%s``.
``WAFFLE_FLAG_DEFAULT``:
    When a Flag is undefined in the database, Waffle considers it
    ``False``.  Set this to ``True`` to make Waffle consider undefined
    flags ``True``.  Defaults to ``False``.
``WAFFLE_SWITCH_DEFAULT``:
    When a Switch is undefined in the database, Waffle considers it
    ``False``.  Set this to ``True`` to make Waffle consider undefined
    switches ``True``.  Defaults to ``False``.
``WAFFLE_SAMPLE_DEFAULT``:
    When a Sample is undefined in the database, Waffle considers it
    ``False``.  Set this to ``True`` to make Waffle consider undefined
    samples ``True``.  Defaults to ``False``.
``WAFFLE_MAX_AGE``:
    How long should Waffle cookies last? (Integer, in seconds.)
    Defaults to ``2529000`` (one month). See :ref:`cookies
    <cookies-chapter>` for more
    details.
``WAFFLE_OVERRIDE``:
    Whether Flags can be controlled from the query string. Defaults to
    ``False``. See :ref:`Testing with Waffle <testing-chapter>` for more
    details.
``WAFFLE_SECURE``:
    Whether to set the ``secure`` flag on cookies. Defaults to
    ``False``.
``WAFFLE_CACHE_PREFIX``:
    Waffle tries to store objects in cache pretty aggressively. If you
    ever upgrade and change the shape of the objects (for example
    upgrading from <0.7.5 to >0.7.5) you'll want to set this to
    something other than ``'waffle:'``.
``WAFFLE_TESTING_COOKIE``:
    Waffle allows specialized A/B testing on a per-flag basis. This
    requires setting a cookie. You can customize the cookie name here.
    Like ``WAFFLE_COOKIE`` it must contain ``%s``. By default it is
    ``dwft_%s``.
