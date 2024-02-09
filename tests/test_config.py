import tests
from configs import Config

config = Config()


def test_getsetitem():
    config.__setitem__('key', 'value')
    assert config.__getitem__('key', None) == 'value'
    assert config.__getitem__('unk_key', 'ok') == 'ok'
