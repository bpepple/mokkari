import pytest
from mokkari import exceptions, publishers_list


def test_known_publishers(talker):
    marvel = talker.publisher(1)
    assert marvel.name == "Marvel"
    assert (
        marvel.image
        == "https://static.metron.cloud/media/publisher/2018/11/11/marvel.jpg"
    )
    assert marvel.wikipedia == "Marvel_Comics"
    assert marvel.founded == 1939


def test_publisherlist(talker):
    publishers = talker.publishers_list()
    assert len(publishers.publishers) > 0


def test_bad_publisher(talker):
    with pytest.raises(exceptions.ApiError):
        talker.publisher(-1)


def test_bad_response_data():
    with pytest.raises(exceptions.ApiError):
        publishers_list.PublishersList({"results": {"name": 1}})
