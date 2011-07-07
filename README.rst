jasmine-splinter-runner
=======================

`Jasmine <http://pivotal.github.com/jasmine/>`_ runner based on `splinter <http://splinter.cobrateam.info>`_.

Installing
----------

You can install ``jasmine-splinter-runner`` using pip: ::

    $ [sudo] pip install jasmine-splinter-runner

Using
-----

After install it, all you need to do is run the command ``jasmine-splinter`` in your terminal: ::

    $ jasmine-splinter URI

Where URI can be a file path (ex: ../runner.html) or an URL (http://localhost/runner.html).

You can use some options:

    -b BROWSER_DRIVER, --browser-driver=BROWSER_DRIVER
                    splinter browser driver (check splinter docs for available drivers)


By default this command will look for a file called ``SpecRunner.html`` and run these specs.

Development
-----------

* source hosted at `github <http://github.com/cobrateam/jasmine-splinter-runner>`_.
* report issues on `github issues <http://github.com/cobrateam/jasmine-splinter/runner/issues>`_.
