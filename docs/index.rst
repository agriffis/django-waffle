.. _project-details:

=============
django-waffle
=============

Waffle is a feature-flipper for Django. It helps you run AB tests, roll out new
features to your users in a number of ways, sample data, and more.

Waffle has :ref:`three types of objects <objects-chapter>`: :ref:`Flags
<objects-flags>`, :ref:`Switches <objects-switches>`, and :ref:`Samples
<objects-samples>` that can be used to control the features of your website,
who sees them, and how they work.

Feature-flippers are particularly useful for continuous integration and
deployment, where you may be merging incomplete code into master. One of the
oldest and best posts about this sort of development is from Flickr_. I
recommend reading it.


:Version:       |release|
:Code:          https://github.com/jsocol/django-waffle
:License:       BSD; see LICENSE file
:Issues:        https://github.com/jsocol/django-waffle/issues

Contents:

.. toctree::
   :maxdepth: 2

   installation
   usage
   objects
   testing-waffles
   contributing


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Flickr: http://code.flickr.com/blog/2009/12/02/flipping-out/
