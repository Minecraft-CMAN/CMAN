import tests
import shutil
from configs import Config


def test_getsetitem():
    # remove config flile
    shutil.rmtree('./runtime/configs')

    config = Config()
    config.__setitem__('key', 'value')
    assert config.__getitem__('key', None) == 'value'
    assert config.__getitem__('unk_key', 'ok') == 'ok'
