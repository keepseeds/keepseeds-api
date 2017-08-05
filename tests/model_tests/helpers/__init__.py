import mock


def filter_by_query(mock_object):
    mock_query = mock.MagicMock()
    mock_query.filter_by.return_value = mock_object
    return mock_query


def filter_query(mock_object):
    mock_filter = mock.MagicMock()
    mock_filter.filter.return_value = mock_object
    return mock_filter


def first_query(mock_object):
    mock_first = mock.MagicMock()
    mock_first.first.return_value = mock_object
    return mock_first


def all_query(mock_objects):
    mock_all = mock.MagicMock()
    mock_all.all.return_value = mock_objects
    return mock_all


def filter_by_filter_query(mock_object):
    return filter_by_query(filter_query(mock_object))


def filter_by_first_query(mock_object):
    return filter_by_query(first_query(mock_object))


def filter_by_filter_first_query(mock_object):
    return filter_by_filter_query(first_query(mock_object))


def filter_by_filter_all_query(mock_objects):
    return filter_by_filter_query(all_query(mock_objects))

