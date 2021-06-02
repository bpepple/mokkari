import pytest
import requests_mock
from mokkari import exceptions, series_list


def test_known_series(talker):
    death = talker.series(1)
    assert death.name == "Death of the Inhumans"
    assert death.sort_name == "Death of the Inhumans"
    assert death.volume == 1
    assert death.year_began == 2018
    assert death.year_end == 2018
    assert death.issue_count == 5
    assert (
        death.image
        == "https://static.metron.cloud/media/issue/2018/11/11/6497376-01.jpg"
    )
    assert death.series_type.name == "Mini-Series"
    assert death.publisher_id == 1


def test_serieslist(talker):
    series = talker.series_list()
    series_iter = iter(series)
    assert next(series_iter).id == 1530
    assert next(series_iter).id == 1531
    assert next(series_iter).id == 1532
    assert len(series) == 28


def test_bad_series(talker):
    with requests_mock.Mocker() as r:
        r.get(
            "https://metron.cloud/api/series/-1/",
            text='{"response_code": 404, "detail": "Not found."}',
        )
        with pytest.raises(exceptions.ApiError):
            talker.series(-1)


def test_bad_response_data():
    with pytest.raises(exceptions.ApiError):
        series_list.SeriesList({"results": {"name": 1}})
