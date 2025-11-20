"""
Describes the configuration allowed in the dotenv file.
"""

from functools import cached_property
import re

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from langchain_core.language_models import BaseChatModel
from langchain.chat_models import init_chat_model

class ModelConfig(BaseModel):
    """Configuration for a given cloud model.
    
    Attributes:
        name (str): the name of the model you wish to use
        provider (str): what model provider do you intend to use ?
            (mistralai, google-genai, openai, ollama, ...)
    """

    name: str 
    provider: str

    @cached_property
    def model(self) -> BaseChatModel: 
        """Return an initialized model to interact with."""

        return init_chat_model(
                model          = self.name,
                model_provider = self.provider,
            )


class Settings(BaseSettings):
    """Describes the available settings for the .env file

    Attributes:
        models (list[ModelConfig]): the list of model configurations that are
            made available to the tools during the demo.
            
            **IMPORTANT** There is no model pre initialized for you in this
            list. This means that you __MUST__ provide a .env file, otherwise
            there will be no model configured for you to use.

    Examples:
        # This dotenv file creates a config where only one
        # model is specified (gemini 2.5 flash lite).

        export MODELS_0__NAME=gemini-2.5-flash-lite
        export MODELS_0__PROVIDER=google-genai
    """

    model_config = SettingsConfigDict(
        env_file             = ".env",
        env_file_encoding    = "utf8",
        env_nested_delimiter = "__",
        extra                = "allow",
    )

    models: dict[str, ModelConfig] = dict()

