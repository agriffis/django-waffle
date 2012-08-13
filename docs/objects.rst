.. _objects-chapter:

==============
Ways to Waffle
==============


Waffle has three ways of controlling code flow, and so three types of objects:
:ref:`Flags <objects-flags>`, :ref:`Switches <objects-switches>` and
:ref:`Samples <objects-samples>`.

All of these can be created and controlled through the `Django admin
interface`_ as well as via a set of :ref:`management commands
<commands-chapter>`.


.. _objects-flags:

Flags
=====

Flags are the, well, flagship of Waffle. They are designed to allow you to
change you product, whether it's restructuring the UI, changing a code path,
using a new feature, or whatever else you can imagine, and then control the who
sees the new version and who sees the old version. (See Flickr's excellent
`Flipping Out`_ post for more on this sort of development.)

Flags are either "active" or "inactive" for a given request. There are a number
of triggers you can define that can cause a flag to be active. One of these is
simply random. If a flag is randomly activated or deactivated for a request, a
:ref:`cookie <cookies-chapter>` will be set so the user will continue to get
the same experience and won't flip back and forth on subsequent requests.

.. _Flipping Out: http://code.flickr.com/blog/2009/12/02/flipping-out/

Flag objects have the following properties:

``Name``:
    The name of the flag. Will be used to identify the flag
    everywhere.
``Everyone``:
    You can flip this flag on (``Yes``) or off (``No``) for everyone,
    overriding all other settings. Leave as ``Unknown`` to use
    normally.
``Testing``:
    Let's you override the flag value using the url querystring.
    See :ref:`Testing <testing-chapter>` for details.
``Percent``:
    A percentage of users for whom the flag will be active. This is
    maintained through cookies, so clever users can get around
    it. Still, it's the most common case.
``Superusers``:
    Is this flag always active for superusers?
``Staff``:
    Is this flag always active for staff?
``Authenticated``:
    Is this flag always active for authenticated users?
``Groups``:
    A list of group IDs for which this flag will always be active.
``Users``:
    A list of user IDs for which this flag will always be active.
``Rollout``:
    Activate Rollout mode? See :ref:`rollout-mode` for details.
``Note``:
    Describe where the flag is used.

You can combine multiple settings here. For example, you could offer a
feature to 12% of users *and* all superusers. When combining settings,
the flag will be active for the user if *any* of the settings matches
for them.


.. _rollout-mode:

Rollout Mode
------------


