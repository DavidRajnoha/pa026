import pytest

from source.data_parsing.load_oris import load_interval, load_concurrent_categories, load_last_start, load_metadata, \
    load_ids, load_ignored_categories
from source.data_parsing.oris_client import OrisClient


@pytest.fixture(scope="module")
def data():
    def _data(oris_race_id: int):
        oris = OrisClient()
        data = oris.get(method="getEventStartLists", eventid=oris_race_id)['Data']
        return data
    return _data


def test_load_interval(data):
    assert load_interval(data("5662")) == 3
    assert load_interval(data("4931")) == 1


def test_load_concurrent(data):
    assert load_concurrent_categories(data("5662"), {"HDR", "P", "T"}, interval=3) == [4, 4, 4]
    assert load_concurrent_categories(data("4931"), {"HDR", "P", "T"}, interval=1) == [5]


def test_load_last_start(data):
    assert load_last_start(data("5662")) == 103


def test_load_metadata():
    # interval, concurrent, efficiency, last_start, entries = load_metadata("5662", ["HDR", "P"])
    # assert interval == 3
    # assert concurrent == [4, 4, 4]

    interval, concurrent, efficiency, last_start, entries = load_metadata("4931", {"HDR", "P"})
    assert interval == 1
    assert concurrent == [3]


def test_load_metadata_failing():
    interval, concurrent, efficiency, last_start, entries = load_metadata("4925", {"HDR", "P", "T"})
    assert interval == 2
    assert concurrent == [6, 4]


def test_load_ids():
    ids = load_ids(date_from="2018-01-01", date_to="2019-01-01")
    print(ids)
    assert len(ids) == 130


def test_load_ignored():
    ignored = load_ignored_categories("5662")
    assert "HDR" in ignored
    assert "P" in ignored

    ignored = load_ignored_categories("4464")
    assert "P2" in ignored
    assert "P4" in ignored
    assert "HDR" in ignored


