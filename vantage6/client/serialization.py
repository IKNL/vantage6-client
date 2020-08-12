import json
import pickle

_serializers = {}


def serialize(data, data_format):
    """
    Lookup data_format in serializer mapping and return the associated
    :param data: the data to be serialized
    :param data_format:
    :return:
    """
    try:
        return _serializers[data_format.lower()](data)
    except KeyError as e:
        raise Exception(f'Serialization of {data_format} has not been implemented.')


def serializer(data_format):
    """
    Register function as serializer by adding it to the `_serializers` map with key `data_format`.

    :param data_format:
    :return:
    """

    def decorator_serializer(func):
        # Register deserialization function
        _serializers[data_format] = func

        # Return function without modifications so it can also be run without retrieving it from `_serializers`.
        return func

    return decorator_serializer


@serializer('json')
def serialize_json(file):
    return json.dump(file)


@serializer('pickle')
def serialize_pickle(file):
    return pickle.dump(file)
