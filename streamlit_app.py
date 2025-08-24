import os
import streamlit as st


# Reuse the existing model loading and generation logic from the Flask app
from app import generate_response  # noqa: E402


def main() -> None:
    st.set_page_config(page_title="Local Chat (Streamlit)", page_icon="💬", layout="centered")

    st.title("Local Chat")
    st.caption(
        "Runs a local Hugging Face causal LM. Set MODEL_NAME env var to change the model."
    )

    with st.expander("Model info", expanded=False):
        st.write(
            """
            - Default model: `openai/gpt-oss-20b`
            - Override via environment variable before launch:
              - Windows PowerShell: `$env:MODEL_NAME = "openai/gpt-oss-20b"`
              - Linux/macOS: `export MODEL_NAME=openai/gpt-oss-20b`
            """
        )

    prompt = st.text_area(
        "Prompt",
        value="You are a helpful assistant.\n\nUser: Write a short haiku about local LLMs.\nAssistant:",
        height=180,
    )

    col_left, col_right = st.columns([2, 1])
    with col_left:
        max_new_tokens = st.slider("Max new tokens", min_value=16, max_value=1024, value=200, step=16)
    with col_right:
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.5, value=0.7, step=0.05)

    disabled = not prompt.strip()
    generate_clicked = st.button("Generate", type="primary", disabled=disabled)

    if generate_clicked:
        with st.spinner("Generating..."):
            # generate_response currently ignores temperature; keep API stable and simple
            # If you want to wire temperature/top_p, modify app.generate_response accordingly
            try:
                reply = generate_response(prompt, max_new_tokens=max_new_tokens)
            except Exception as exc:  # Surface any model loading issues to the UI
                st.error(f"Error: {exc}")
                return

        st.subheader("Response")
        st.write(reply)


if __name__ == "__main__":
    main()


