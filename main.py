from settings import Settings, ModelConfig

from langchain_google_genai import ChatGoogleGenerativeAI

def model(cfg: ModelConfig) -> ChatGoogleGenerativeAI:
    '''creates an actual instance of the model.'''

    return ChatGoogleGenerativeAI(
        model   = cfg.name,
        api_key = cfg.key,
    )

def main():
    cfg = Settings()
    mod = model(cfg.MODEL_A)
    
    rsp = mod.invoke(
            """Raconte moi une bonne blague pour me détendre ce soir."""
    )
    print(f"{rsp.content}")


if __name__ == "__main__":
    main()
