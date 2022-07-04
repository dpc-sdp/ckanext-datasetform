=============
ckanext-datasetform
=============

.. This CKAN extension adds a simple form to each dataset that sends an email
   to the author/maintainer of the current dataset.


------------
Requirements
------------

CKAN 2.6.3


------------
Installation
------------

To install ckanext-datasetform:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

     cd /usr/lib/ckan/default/src/ckanext-datasetform
     python setup.py develop

2. Add ``datasetform`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/development.ini``).

     ckan.plugins = stats text_view image_view recline_view datasetform

3. Enable Email settings.
     email_to = ckan_email@example.com
     #error_email_from = ckan-errors@example.com
     smtp.server = <SMTP_SERVER>
     smtp.starttls = True
     smtp.user = <SMTP_USERNAME>
     smtp.password = <SMTP_PASSWORD>
     #smtp.mail_from =

4. Restart CKAN.


---------------
Config Settings
---------------

    ## Dataset Contact form settings
    # Recipient email for each package. Use the field name from dataset, eg. maintainer_email or author_email.
    ckan.package.contact_recipient = maintainer_email


If `ckan.package.contact_recipient` is not set, the form will fall back to using the CKAN setting `ckan.package.default_recipient_email` and then `email_to`.

------------------------
Development Installation
------------------------

To install ckanext-datasetform for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/salsadigitalauorg/ckanext-datasetform.git
    cd ckanext-datasetform
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.datasetform --cover-inclusive --cover-erase --cover-tests


---------------------------------
Registering ckanext-datasetform on PyPI
---------------------------------

ckanext-datasetform should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-datasetform. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags

