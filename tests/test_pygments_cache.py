"""Tests for pygments cache"""
import pytest

import pygments_cache
from pygments_cache import build_cache

pygments_cache.DEBUG = True
CACHE = None


def refresh_cache():
    global CACHE
    CACHE = build_cache()
    pygments_cache.CACHE = CACHE


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


@pytest.mark.parametrize('filename, modname, clsname', [
    ('text', 'pygments.formatters.other', 'NullFormatter'),
    ('tex', 'pygments.formatters.latex', 'LatexFormatter'),
    ('latex', 'pygments.formatters.latex', 'LatexFormatter'),
    ])
def test_formatter_names(cache, filename, modname, clsname):
    obsmod, obscls = cache['formatters']['names'][filename]
    assert modname == obsmod
    assert clsname == obscls
