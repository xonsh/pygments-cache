"""A fast drop-in replacement for pygments get_*() and guess_*() funtions.
"""
import os


# Global storage variables
CACHE = None


def _discover_lexers():
    import inspect
    from pygments.lexers import get_all_lexers, find_lexer_class
    # maps file extension (and names) to (module, classname) tuples
    ext = {}
    lexers = {'ext': ext}
    for longname, aliases, filenames, mimetypes in get_all_lexers():
        cls = find_lexer_class(longname)
        mod = inspect.getmodule(c)
        val = (mod.__name__, cls.__name__)
        for filename in filenames:
            if filename.startswith('*.'):
                filename = filename[1:]
            if '*' in filename:
                continue
            ext[filename] = val
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

