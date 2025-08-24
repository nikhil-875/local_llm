# Local Chat (OSS 20B) – Python + Flask

Simple local chat UI with a locally loaded OSS 20B model via Hugging Face Transformers.

## Requirements
- 16+ GB RAM (32 GB recommended)
- NVIDIA GPU with ≥16 GB VRAM for practical 20B usage
- ~50 GB free disk
- Python 3.10+

## Quickstart (Windows PowerShell)
```powershell
# From repo root
cd .\local_chat

# Create & activate venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install deps (CPU wheel by default; GPU users see note below)
pip install -r requirements.txt

# Optional: choose model (default: openai/gpt-oss-20b)
$env:MODEL_NAME = "openai/gpt-oss-20b"

# Run
python app.py
```
Open `http://127.0.0.1:8000` in your browser.

## Streamlit UI (optional)
```powershell
# From repo root
cd .\local_chat
\.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:MODEL_NAME = "openai/gpt-oss-20b"
streamlit run streamlit_app.py
```
The app will open in your browser (usually `http://localhost:8501`).

## GPU note
If you want the CUDA GPU wheel for PyTorch, follow the official selector at
`https://pytorch.org/get-started/locally/` and install the recommended `torch`
package for your CUDA version, then `pip install transformers accelerate`.

## WSL2 (optional)
For Windows, WSL2 + NVIDIA CUDA can improve stability/perf. Ensure proper GPU driver
installation and CUDA passthrough, then follow the same steps inside WSL.

## Model customization
Set `MODEL_NAME` to any causal LM on Hugging Face Hub:
```powershell
$env:MODEL_NAME = "openai/gpt-oss-20b"
```
Restart the app after changing.

## Security
The server binds to `127.0.0.1` only. Do not expose publicly.
