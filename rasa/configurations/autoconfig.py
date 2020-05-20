from typing import Text, Dict, Any, List

from rasa.constants import CONFIG_AUTOCONFIGURABLE_KEYS
from rasa.importers.importer import TrainingDataImporter  # not needed in 1st iteration

from rasa.utils import io as io_utils


def get_autoconfiguration(config):

    autoconfig_keys = CONFIG_AUTOCONFIGURABLE_KEYS
    missing_keys = [k for k in autoconfig_keys if k not in config]

    create_config_for_keys(config, missing_keys)

    return config


# In future iterations, this will need access to the training data.
# => pass a TrainingDataImporter as argument?
# Would that work? get_autoconfiguration is called in RasaFileImporter.__init__
# Can the RasaFileImporter pass itself as an argument while still in its own constructor?
def create_config_for_keys(config: Dict[Text, Any], keys: List[Text],) -> None:
    import pkg_resources

    default_config_path = pkg_resources.resource_filename(
        __name__, "default_config.yml"
    )

    default_config = io_utils.read_config_file(default_config_path)

    if not config.get("autoconfigured"):
        config["autoconfigured"] = set()

    for key in keys:
        config[key] = default_config[key]
        config["autoconfigured"].add(key)


def dump_config(config: Dict[Text, Any], config_path: Text) -> None:
    # only write sections that are in config.autoconfigured
    io_utils.write_yaml_file(config, config_path)
