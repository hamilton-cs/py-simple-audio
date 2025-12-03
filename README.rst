NOTE: THIS PROJECT IS NOT CONSISTENTLY MAINTAINED
==============================


 This version of the simpleaduio library has replaced the continuous integration pipeline to
 support more recent versions of various operating systems. We have worked on this as part
 of a senior capstone project, and will therefore no longer be actively maintining it after
 December 2025.

 This version of the package is optimized for Mac, Windows and Linux for Python versions 3.10,
 3.11, and 3.12.

simpleaudiohamiltoncs Package
===================

The simplaudio package provides cross-platform, dependency-free audio playback
capability for Python 3 on OSX, Windows, and Linux.

MIT Licensed.

`Documentation at RTFD <http://simpleaudiohamiltoncs.readthedocs.io/>`_
--------------------------------------------------------------

Installation
------------

This project is currently a work in progress, and can therefore be
installed through TestPyPI. This will be updated upon release when
the project is uploaded to PyPI.

Installation (make sure the ``pip`` command is the right one for
your platform and Python version)::

   pip install -i https://test.pypi.org/simple/simpleaudiohamiltoncs==1.0.6

See documentation for additional installation information.

Quick Function Check
--------------------

.. code-block:: python

   import simpleaudiohamiltoncs.functionchecks as fc

   fc.LeftRightCheck.run()

See documentation for more on function checks.

Simple Example
--------------

.. code-block:: python

   import simpleaudiohamiltoncs as sa

   wave_obj = sa.WaveObject.from_wave_file("path/to/file.wav")
   play_obj = wave_obj.play()
   play_obj.wait_done()

Support
-------

For usage and how-to questions, first checkout the tutorial in the
documentation. If you're still stuck, post a question on
`StackOverflow <http://stackoverflow.com/>`_
and **tag it 'pysimpleaudiohamiltoncs'**.

For bug reports, please create an
`issue on Github <https://github.com/hamiltron/py-simple-audio/issues>`_
.

Big Thanks To ...
-----------------

Jonas Kalderstam

Christophe Gohlke

Tom Christie

Many others for their contributions, documentation, examples, and more.
