"""
Describes the configuration allowed in the dotenv file.
"""

from pydantic import BaseModel
from pydantic_settings import BaseSettings

class ModelConfig(BaseModel):
    """Configuration for a given cloud model."""

    name: str 
    key: str

class Settings(BaseSettings):
    """Describes the available settings for the .env file

    Examples:
        export MODEL_A__NAME=gemini-2.5-flash-lite
        export MODEL_A__KEY=DONT_EXPECT_THIS_TO_BE_MY_SECRET

    """

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf8"
        env_nested_delimiter: str = "__"

    MODEL_A: ModelConfig = ModelConfig(name="gemini-3.5-flash-lite"  , key="USE_YOUR_OWN_TOKEN")
    MODEL_B: ModelConfig = ModelConfig(name="open-mistral-nemo-2407" , key="USE_YOUR_OWN_KEY")
    MODEL_C: ModelConfig = ModelConfig(name="gemini-3.0-pro-preview" , key="USE_YOUR_OWN_TOKEN")
    MODEL_D: ModelConfig = ModelConfig(name="mistral-large"          , key="USE_YOUR_OWN_KEY")
    MODEL_E: ModelConfig = ModelConfig(name="gpt-oss-20b"            , key="USE_YOUR_OWN_KEY")
