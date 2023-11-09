import json

from pydantic import ConfigDict, BaseModel, field_validator, constr


class BugzillaConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')

    URL: constr(strip_whitespace=True, min_length=1)
    api_key: constr(strip_whitespace=True, min_length=1)
    field_data_plugin_name: constr(strip_whitespace=True, min_length=1)


class JiraConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')

    URL: constr(strip_whitespace=True, min_length=1)
    token_auth: constr(strip_whitespace=True, min_length=1)
    field_data_plugin_name: constr(strip_whitespace=True, min_length=1)


class BugjiraConfigDict(BaseModel):
    model_config = ConfigDict(extra='forbid')

    bugzilla: BugzillaConfig
    jira: JiraConfig
    # The field_data_path attribute is optional since it is only used by
    # the default field data generator plugin.
    field_data_path: str = None


class Config(BaseModel):
    """A BaseModel to validate config dicts"""

    config_dict: dict

    @field_validator("config_dict")
    def validate_minimum_config(cls, v):
        BugjiraConfigDict(**v)
        return v

    @staticmethod
    def from_config(config_path=None, config_dict=None):
        """Returns a config dict based on either a json file specified by
        the config_path parameter or a dict specified by the config_dict
        parameter. If both a path and a dict are provided, use the dict to
        generate the config.

        :param config_path: Full path to a valid json config file, defaults to
            None
        :type config_path: str, optional
        :param config_dict: A dict containing configuration settings, defaults
            to None
        :type config_dict: dict, optional
        :raises ValueError: If no parameters are supplied
        :return: A validated config dict for connecting to the bugzilla and
            jira backends
        :rtype: dict
        """
        if config_dict is not None:
            return Config(config_dict=config_dict).config_dict
        if config_path is not None:
            with open(config_path) as conf:
                config_dict = json.loads(conf.read())
                return Config(config_dict=config_dict).config_dict
        raise ValueError(
            "from_config requires config_path or config_dict parameters"
        )
