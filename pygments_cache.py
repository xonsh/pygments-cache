"""A fast drop-in replacement for pygments ``get_*()`` and ``guess_*()`` funtions.

The cache itself is stor
"""
import os
import importlib


# Global storage variables
__version__ = '0.0.0'
CACHE = None


def _discover_lexers():
    import inspect
    from pygments.lexers import get_all_lexers, find_lexer_class
    # maps file extension (and names) to (module, classname) tuples
    exts = {}
    lexers = {'exts': exts}
    for longname, aliases, filenames, mimetypes in get_all_lexers():
        cls = find_lexer_class(longname)
        mod = inspect.getmodule(cls)
        val = (mod.__name__, cls.__name__)
        for filename in filenames:
            if filename.startswith('*.'):
                filename = filename[1:]
            if '*' in filename:
                continue
            exts[filename] = val
    return lexers


def build_cache():
    """Does the hard work of building a cache from nothing."""
    cache = {}
    cache['lexers'] = _discover_lexers()
    return cache


def cache_filename():
    """Gets the name of the cache file to use."""
    # Configuration variables read from the environment
    if 'PYGMENTS_CACHE_FILE' in os.environ:
        return os.environ['PYGMENTS_CACHE_FILE']
    else:
        return os.path.join(os.environ.get('XDG_DATA_HOME',
                                           os.path.join(os.path.expanduser('~'),
                                                        '.local', 'share')),
                            'pygments-cache',
                            'cache.py'
                            )


def load(filename):
    """Loads the cache from a filename."""
    global CACHE
    with open(filename) as f:
        s = f.read()
    ctx = globals()
    CACHE = eval(s, ctx, ctx)
    return CACHE


def write_cache(filename):
    """Writes the current cache to the file"""
    from pprint import pformat
    s = pformat(cache)
    with open(filename, 'w') as f:
        f.write(s)


def load_or_build():
    """Loads the cache from disk. If the cache does not exist,
    this will build and write it out.
    """
    global CACHE
    fname = cache_filename()
    if os.path.exists(fname):
        load(fname)
    else:
        import sys
        print('pygments cache not found, building...', file=sys.stderr)
        CACHE = build_cache()
        print('...writing cache to ' + fname, file=sys.stderr)
        write_cache(fname)

#
# pygments interface
#

def get_lexer_for_filename(filename, text='', **options):
    """Gets a lexer from a filename (usually via the filename extension).
    This mimics the behavior of ``pygments.lexers.get_lexer_for_filename()``
    and ``pygments.lexers.guess_lexer_for_filename()``.
    """
    if CACHE is None:
        load_or_build()
    exts = CACHE['lexers']['exts']
    fname = os.path.basename(filename)
    key = fname if fname in exts else os.path.splitext(fname)[1]
    if key in exts:
        modname, clsname = exts[key]
        mod = importlib.import_module(modname)
        cls = getattr(mod, clsname)
        lexer = cls()
    else:
        # couldn't find lexer in cache, fallback to the hard way
        import inspect
        from pygments.lexers import guess_lexer_for_filename
        lexer = guess_lexer_for_filename(filename, text, **options)
        # add this filename to the cache for future use
        cls = type(lexer)
        mod = inspect.getmodule(cls)
        exts[fname] = (mod.__name__, cls.__name__)
        write_cache(cache_filename())
    return lexer


guess_lexer_for_filename = get_lexer_for_filename
