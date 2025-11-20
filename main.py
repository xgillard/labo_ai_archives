"""Exercise for the lab session."""

import base64
import streamlit as st

from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import (
    ContentBlock,
    HumanMessage, 
    ImageContentBlock, 
    TextContentBlock,
)

from docling.document_converter import DocumentConverter
from docling_core.types.io import DocumentStream

from streamlit.runtime.uploaded_file_manager import UploadedFile

from settings import Settings

load_dotenv()

@st.fragment
def page_header(settings: Settings):
    """Draw the page title as well as the model select box.

        **Important**
        The chosen model is stored in the session.
    """

    with st.container():
        left, right = st.columns([5, 1], vertical_alignment="bottom")

        with left:
            st.title("AI & Archives Lab")

        with right:
            model_key = right.selectbox(
                label   = "Model",
                options = settings.models.keys(),
            )
            model = settings.models[model_key]
            st.session_state["model"] = model.model

        st.divider()

def to_markdown(attach: UploadedFile) -> TextContentBlock:
    converter = DocumentConverter()
    stream = DocumentStream(name=attach.name, stream=attach)
    doc = converter.convert(stream).document
    text = doc.export_to_markdown()
    return TextContentBlock(type="text", text=text, extras={"file": attach.name})

def as_content_block(attach: UploadedFile) -> ContentBlock:
    """turns a file into a content block."""

    name    = Path(attach.name)
    match name.suffix.lower():
        case '.pdf' | '.doc' | '.docx' | '.odt' :
            return to_markdown(attach)
        case '.jpg' | '.jpeg':
            mime = 'image/jpeg'
            encoded = base64.b64encode(attach.getbuffer())
            return ImageContentBlock(
                type="image",
                mime_type=mime,
                base64=encoded.decode(encoding="utf8"),
            )
        case '.png':
            mime = 'image/png'
            encoded = base64.b64encode(attach.getbuffer())
            return ImageContentBlock(
                type="image",
                mime_type=mime,
                base64=encoded.decode(encoding="utf8"),
            )
        case _:
            raise ValueError("unknown image type")


def as_human_message(text: str, files: list[UploadedFile]) -> HumanMessage:
    """Turns the prompt into a human message."""
    
    return HumanMessage(content_blocks=[
        *(as_content_block(a) for a in files), 
        TextContentBlock(type="text", text=text),
    ])

def render_session(parent):
    """Display the chat conversation with the user."""

    messages = st.session_state.get("messages", [])
    if messages:
        with parent:
            for msg in messages:
                with st.chat_message(msg.type):
                    for block in msg.content_blocks:
                        match block["type"]:
                            case 'text':
                                if fname := block.get("extras", {}).get("file"):
                                    st.write(f" -- {fname} --")
                                else:
                                    st.write(block["text"])
                            case "image":
                                st.write(" -- image --")


def main():
    cfg = Settings()

    page_header(cfg)
    
    c_messages = st.container()
    render_session(c_messages)

    if prompt := st.chat_input(
        accept_file=True,
        file_type=[".jpg", ".jpeg", ".png", ".pdf", ".doc", ".docx", ".odt"],
    ):
        hist = st.session_state.get("messages", [])
        msg  = as_human_message(prompt.text, prompt.files)
        hist.append(msg)

        with st.chat_message("human"):
            for block in msg.content_blocks:
                match block["type"]:
                    case 'text':
                        if fname := block.get("extras", {}).get("file"):
                            st.write(f" -- {fname} --")
                        else:
                            st.write(block["text"])
                    case "image":
                        st.write(" -- image --")

        model = st.session_state["model"]
        rsp   = model.invoke([*hist, msg])
        hist.append(rsp)
        st.session_state["messages"] = hist
        st.chat_message("ai").write(rsp.content)
    

if __name__ == "__main__":
    main()
