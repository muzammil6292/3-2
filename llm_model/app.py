from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from utils.parallel import run_parallel, generate_report
from datetime import datetime

st.set_page_config(page_title="LLM Comparison Tool", page_icon="🚀", layout="wide")

st.sidebar.title("LLM Comparison")
st.sidebar.markdown("Choose models and options")
models_available = ["ChatGPT", "Gemini", "LLaMA"]
selected_models = st.sidebar.multiselect("Models", models_available, default=models_available)

show_raw = st.sidebar.checkbox("Show raw responses", value=False)
st.sidebar.markdown("---")
st.sidebar.caption("Made with Streamlit")

st.header("🚀 LLM Comparison Tool")
st.write("Compare multiple LLMs using a single unified prompt and export results.")

if "responses" not in st.session_state:
    st.session_state.responses = {}
    st.session_state.report_path = None

prompt = st.text_area("Enter your prompt", height=200, placeholder="Explain Python decorators with an example")

col_controls, _ = st.columns([1, 3])
with col_controls:
    if st.button("Compare Models", key="compare"):
        if not prompt.strip():
            st.warning("Please enter a prompt")
        else:
            with st.spinner("Running models in parallel..."):
                st.session_state.responses = run_parallel(prompt)
                st.session_state.report_path = generate_report(prompt, st.session_state.responses)
            st.success("✅ Comparison completed successfully!")

    if st.button("Clear", key="clear"):
        st.session_state.responses = {}
        st.session_state.report_path = None

if st.session_state.responses:
    # Filter responses by selected models (display-only)
    filtered = {m: st.session_state.responses.get(m, "") for m in selected_models}

    cols = st.columns(len(filtered) if len(filtered) > 0 else 1)
    for i, (model, resp) in enumerate(filtered.items()):
        with cols[i]:
            st.subheader(model)
            st.write(resp if resp else "(no response)")
            if show_raw:
                with st.expander("Raw response"):
                    st.code(resp or "")

    if st.session_state.report_path:
        with open(st.session_state.report_path, "rb") as f:
            st.download_button(label="📥 Download comparison report (CSV)", data=f, file_name=f"llm_report_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.csv", mime="text/csv")
else:
    st.info("Run a comparison to see model outputs here.")
