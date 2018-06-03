pygments-cache
==============
A fast, drop-in replacement for pygments ``get_*()`` and ``guess_*()`` funtions.

The following pygments API functions are currently supplied here::

    from pygments_cache import get_lexer_for_filename, guess_lexer_for_filename
    from pygments_cache import get_formatter_for_filename, get_formatter_by_name
    from pygments_cache import get_style_by_name
    from pygments_cache import get_filter_by_name

The cache itself is stored at the location given by the ``$PYGMENTS_CACHE_FILE``
environment variable, or by default at ``~/.local/share/pygments-cache/cache.py``.
The cache file is created on first use, if it does not already exist.

If a pygements extentsion is not found in the cache, the API functions listed here
will fallback to the original pygments version and the extension will be added to
the cache for future use. That is, the cache will discover and save new extensions
as you would expect.

If you ever need to reset the cache for some reason, simply delete the
``$PYGMENTS_CACHE_FILE`` from your file system. The next time you call one of
the API functions, the cache will be regenerated. Alternatively, you may
manually rebuild the cache (after removing the file) with the ``load_or_build()``
function.

The cache itself is fully accessible as the ``pygments_cache.CACHE`` dict.

This project is implement as single file, making it easy to redistribute.
Feel free to copy this file to your own project!

Comparison
----------
**NOTE:** All of the following tests were in `xonsh <http://xon.sh>`_.

**TL;DR Table:** All timings in seconds.

==================  ========  ===========
                    cold      hot
==================  ========  ===========
``pygments``        0.48      3.09e-3
``pygments_cache``  0.03      9.90e-6
**speedup**         **16x**   **306x**
==================  ========  ===========


From a **cold start** (i.e. the first import and use), pygments can take a long
time (about half a second) to get a single lexer, as seen below:

.. code-block:: console

    $ time -p python -c! from pygments.lexers import get_lexer_for_filename; get_lexer_for_filename('index.html')
    real 0.48
    user 0.46
    sys 0.01

The pygments-cache project speeds this up considerably, assuming the cache file already exists.
The timing can be seen here:

.. code-block:: console

    $ time -p python -c! from pygments_cache import get_lexer_for_filename; get_lexer_for_filename('index.html')
    real 0.03
    user 0.03
    sys 0.00

This represents a **16x** speedup. However, most of the 0.03 sec is actually coming from Python itself starting
up and shutting down.

A more fair test is to look at how long the ``get_lexer_for_filename()`` function takes to run
once Python has been started and the function imported.

From a **hot start**, pygments itself tok about 3 ms, as seen below:

.. code-block:: console

    $ from pygments.lexers import get_lexer_for_filename
    $ timeit! get_lexer_for_filename('index.html')
    100 loops, best of 3: 3.09 ms per loop

Alternatively, pygments-cache took only 9.9 µs, as seen below.

.. code-block:: console

    $ from pygments_cache import get_lexer_for_filename
    $ timeit! get_lexer_for_filename('index.html')
    100000 loops, best of 3: 9.9 µs per loop

This is a speedup of **306x**!
