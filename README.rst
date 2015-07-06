django-rest-tools
=================

|Build Status| |Coverage Status| |Requirements Status|

Install last stable version from pypi
-------------------------------------

.. code-block:: bash

    pip install django-rest-tools

Install development version
---------------------------

.. code-block:: bash

    pip install https://github.com/quiqueporta/django-rest-tools/tarball/master

Filters
-------

NearToPointFilter
~~~~~~~~~~~~~~~~~

``views.py:``

.. code-block:: python

    from django_rest_tools.filters import NearToPointFilter

    class LocationsList(generics.ListAPIView):

        queryset = Location.objects.all()
        serializer_class = LocationListSerializer
        filter_backends = (NearToPointFilter,)
        point_field_filter = 'location'

We can then filter in the URL.

eg:.
``/location/?max_distance=40&lat=-40.4862&long=-0.39536``


.. |Build Status| image:: https://travis-ci.org/quiqueporta/django-rest-tools.svg?branch=master
    :target: https://travis-ci.org/quiqueporta/django-rest-tools

.. |Coverage Status| image:: https://coveralls.io/repos/quiqueporta/django-rest-tools/badge.svg?branch=master
  :target: https://coveralls.io/r/quiqueporta/django-rest-tools?branch=master

.. |Requirements Status| image:: https://requires.io/github/quiqueporta/django-rest-tools/requirements.svg?branch=master
     :target: https://requires.io/github/quiqueporta/django-rest-tools/requirements/?branch=master
     :alt: Requirements Status
