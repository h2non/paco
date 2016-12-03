# -*- coding: utf-8 -*-
from paco.utils import isiter


def test_isiter():
    assert isiter(()) is True
    assert isiter([]) is True
    assert isiter('foo') is False
    assert isiter(bytes()) is False
    assert isiter(True) is False
