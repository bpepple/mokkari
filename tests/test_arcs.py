import pytest
import requests_mock
from mokkari import arcs_list, exceptions


def test_known_arc(talker):
    heroes = talker.arc(1)
    assert heroes.name == "Heroes In Crisis"
    assert (
        heroes.image
        == "https://static.metron.cloud/media/arc/2018/11/12/heroes-in-crisis.jpeg"
    )


def test_arcslist(talker):
    arcs = talker.arcs_list()
    arc_iter = iter(arcs)
    assert next(arc_iter).name == "52"
    assert next(arc_iter).name == "A Court of Owls"
    assert len(arcs) == 28


def test_bad_arc(talker):
    with requests_mock.Mocker() as r:
        r.get(
            "https://metron.cloud/api/arc/-8/",
            text='{"response_code": 404, "detail": "Not found."}',
        )

        with pytest.raises(exceptions.ApiError):
            talker.arc(-8)


def test_bad_response_data():
    with pytest.raises(exceptions.ApiError):
        arcs_list.ArcsList({"results": {"name": 1}})
