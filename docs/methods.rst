.. _methods-chapter:

======================
Using Waffle in Python
======================


Waffle has only a few public methods, one for each type of :ref:`Waffle
object <objects-chapter>`. These are all available in the ``waffle``
namespace::

    import waffle


.. _methods-flag:

``waffle.flag_is_active(request, flag_name)``
=============================================

``flag_is_active`` examines the request and properties of the :ref:`Flag
<objects-flag>` and determines whether to return ``True`` (the Flag is
"active") or ``False`` (the Flag is "inactive").

For example::

    import waffle

    def my_view(request):
        if waffle.flag_is_active(request, 'my-flag'):
            # Behavior if flag is active.
        else:
            # Behavior if flag is inactive.

Multiple calls to ``flag_is_active`` with the same Flag and request
object (e.g. within the same view) will return the same value.


.. _methods-switch:

``waffle.switch_is_active(switch_name)``
========================================

For :ref:`Switches <objects-switches>`, just use the
``switch_is_active`` method::

    import waffle

    def myview(request):
        if waffle.switch_is_active('my-switch'):
            return 'switch is active'
        return 'switch is inactive'

Because it doesn't need a ``request`` object, ``switch_is_active`` can
be used anywhere.


.. _methods-sample:

``waffle.sample_is_active(sample_name)``
========================================

For :ref:`Samples <objects-samples>`, use ``sample_is_active``. Similar
to ``switch_is_active``, ``sample_is_active`` can be used anywhere,
since it does not require a ``request`` object::

    import waffle

    def myview(request):
        if waffle.sample_is_active('my-sample'):
            # Some percent of requests.
