.. _decorators-chapter:

=================
Waffle Decorators
=================

Two types of :ref:`objects <objects-chapter>` :ref:`Flags
<objects-flags>` and :ref:`Switches <objects-switches>` allow you to
wrap an entire view with a decorator. If the Flag or Switch is
**inactive** the view will return a 404 page.

.. note::
   The decorators will raise a Django Http404 exception, and all the
   normal processing will happen based on that.


Wrap a whole view in a Flag::

    from waffle.decorators import waffle_flag

    @waffle_flag('flag_name')
    def my_view(request):
        # View only available if flag is active.

...or a Switch::

    from waffle.decorators import waffle_switch

    @waffle_switch('switch_name')
    def my_view(request):
        # View only available if switch is active.

.. note::
   You can reverse the effect, i.e. return a 404 if the Flag or Switch
   is **active** by prepending the name of the object with a "!".

::

    @waffle_flag('!flag_name')
    def my_view(request):
        # View is only available if flag is INactive.

