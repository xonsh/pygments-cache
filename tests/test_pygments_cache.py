"""Tests for pygments cache"""
import os
import tempfile

import pytest

import pygments_cache
from pygments_cache import build_cache, load_or_build, get_lexer_for_filename

pygments_cache.DEBUG = True
CACHE = None


def refresh_cache():
    global CACHE
    CACHE = build_cache()
    pygments_cache.CACHE = CACHE


#
# Test cache creation
#

@pytest.fixture
def cache():
    if CACHE is None:
        refresh_cache()
    return CACHE


@pytest.mark.parametrize('filename, modname, clsname', [
    ('.yaml', 'pygments.lexers.data', 'YamlLexer'),
    ('CMakeLists.txt', 'pygments.lexers.make', 'CMakeLexer'),
    ('.py', 'pygments.lexers.python', 'Python3Lexer'),
    ])
def test_lexer_exts(cache, filename, modname, clsname):
    obsmod, obscls = cache['lexers']['exts'][filename]
    assert modname == obsmod
    assert clsname == obscls


@pytest.mark.parametrize('filename, modname, clsname', [
    ('.txt', 'pygments.formatters.other', 'NullFormatter'),
    ('.tex', 'pygments.formatters.latex', 'LatexFormatter'),
    ])
def test_formatter_exts(cache, filename, modname, clsname):
    obsmod, obscls = cache['formatters']['exts'][filename]
    assert modname == obsmod
    assert clsname == obscls


@pytest.mark.parametrize('name, modname, clsname', [
    ('text', 'pygments.formatters.other', 'NullFormatter'),
    ('tex', 'pygments.formatters.latex', 'LatexFormatter'),
    ('latex', 'pygments.formatters.latex', 'LatexFormatter'),
    ])
def test_formatter_names(cache, name, modname, clsname):
    obsmod, obscls = cache['formatters']['names'][name]
    assert modname == obsmod
    assert clsname == obscls


@pytest.mark.parametrize('name, modname, clsname', [
    ('murphy', 'pygments.styles.murphy', 'MurphyStyle'),
    ('monokai', 'pygments.styles.monokai', 'MonokaiStyle'),
    ])
def test_style_names(cache, name, modname, clsname):
    obsmod, obscls = cache['styles']['names'][name]
    assert modname == obsmod
    assert clsname == obscls


@pytest.mark.parametrize('name, modname, clsname', [
    ('gobble', 'pygments.filters', 'GobbleFilter'),
    ('highlight', 'pygments.filters', 'NameHighlightFilter'),
    ])
def test_filter_names(cache, name, modname, clsname):
    obsmod, obscls = cache['filters']['names'][name]
    assert modname == obsmod
    assert clsname == obscls


#
# Test Cache Creation
#
def test_load_or_build():
    # prep for test
    temp_dir = tempfile.TemporaryDirectory()
    cache_file = os.path.join(temp_dir.name, 'cache.py')
    os.environ['PYGMENTS_CACHE_FILE'] = cache_file
    pygments_cache.CACHE = None
    # first test building and writing cache
    load_or_build()
    assert pygments_cache.CACHE is not None
    assert 0 < len(pygments_cache.CACHE)
    assert os.path.isfile(cache_file)
    with open(cache_file) as f:
        s = f.read()
    ctx = {}
    read_in_cache = eval(s, ctx, ctx)
    assert pygments_cache.CACHE == read_in_cache
    # now that the cache file exists, reset in-memory cache and
    # verify loading worked
    pygments_cache.CACHE = None
    load_or_build()
    assert pygments_cache.CACHE == read_in_cache
    # cleanup
    temp_dir.cleanup()


#
# Test API
#

def test_get_lexer_for_filename():
    pass