from scripts.config import config


def test_config():
    config_dict = config()
    assert len(config_dict) != 0
