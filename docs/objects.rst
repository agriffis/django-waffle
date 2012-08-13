.. _objects-chapter:

===============
Types of Waffle
===============


Waffle has three ways of controlling code flow, and so three types of
objects: :ref:`Flags <objects-flags>`, :ref:`Switches
<objects-switches>` and :ref:`Samples <objects-samples>`.

All of these can be created and controlled through the `Django admin
interface`_ as well as via a set of :ref:`management commands
<commands-chapter>`.

You should also check out the chapters on :ref:`Methods
<methods-chapter>`, :ref:`Templates <templates-chapter>`, and
:ref:`JavaScript <javascript-chapter>` for information on how to use
these objects.


.. _objects-flags:

Flags
=====

**Flags** are the, well, flagship of Waffle. They are designed to allow
you to change you product, whether it's restructuring the UI, changing a
code path, using a new feature, or whatever else you can imagine, and
then control the who sees the new version and who sees the old version.
(See Flickr's excellent `Flipping Out`_ post for more on this sort of
development.)

Flags are either "active" or "inactive" for a given request. There are a
number of triggers you can define that can cause a flag to be active.
One of these is simply random. If a flag is randomly activated or
deactivated for a request, a :ref:`cookie <cookies-chapter>` will be set
so the user will continue to get the same experience and won't flip back
and forth on subsequent requests.

You can check if a flag is active with the ``waffle.flag_is_active``
:ref:`method <methods-chapter>` in code, or various ways :ref:`in
templates <templates-chapter>` and in :ref:`JavaScript
<javascript-chapter>`.

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

**Rollout Mode** allows you to gradually enable a feature for all
users. In "normal" mode, a flag's value will be set in a cookie until
``WAFFLE_MAX_AGE`` whether the flag is active or not. In Rollout Mode,
an *inactive* flag will set a session cookie, and an *active* flag
will set a longer-lived cookie.

Every time a user starts a new session, they'll have a chance
(determined by the percentage of the flag) to have the feature turned
on "permanently". Once it's on, it should stay on, unless they clear
their cookies or use a different browser.

To guarantee an even rollout, it will likely be necessary to gradually
increase the flag's percentage as more and more users get stuck with
the *active* cookie.

Rollout Mode is enabled **per flag**.


.. _objects-switches:

Switches
========

**Switches** are boolean, they are always either on or off. They do not
depend on a request. They can be checked with the
``waffle.switch_is_active`` `method <methods-chapter>`.

Switches are also managed through the Django admin. Each ``Switch``
object has these properties:

``Name``:
    The name of the switch.
``Active``:
    Is the switch active or inactive.
``Note``:
    Describe where the switch is used.

Like Flags, Switches can be used in views, templates, or wrapped around
entire templates. But because they don't rely on a ``request`` objects,
Switches can also be used in crons, Celery tasks, daemons---basically
anywhere you can access the database.


.. _objects-samples:

Samples
=======

**Samples** are useful for datamining or other "some of the time" tasks
that are not linked to a user or request---that is, unlike Flags, they
do not set cookies and can't be reliably assumed to be a given value
for a given user.

Samples, also managed through the Django admin, have these properties:

``Name``:
    The name.
``Percent``:
    A number from 0.0 to 100.0 that determines how often the sample
    will be active.
``Note``:
    Describe where the sample is used.

Samples, like the other types, can be used in views, templates, and
JavaScript, but they cannot be used to wrap an entire view.
