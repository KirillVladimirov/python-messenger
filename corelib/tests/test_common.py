import pytest
from datetime import datetime
import time


@pytest.mark.xfail()
def test_failed():
    assert False


def test_date():
    assert datetime


# def test_date1():
#     assert datetime.fromtimestamp(time.time()) == datetime.now()
