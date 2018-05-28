"""Tests for pygments cache"""
import pytest

import pygments_cache
from pygments_cache import build_cache


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
    ])
def test_lexer_exts(cache, filename, modname, clsname):
    obsmod, obscls = cache['lexers']['exts'][filename]
    assert modname == obsmod
    assert clsname == obscls
