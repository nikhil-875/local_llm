import os
from flask import Flask, render_template, request, jsonify

# Optional heavy imports are deferred to first request to speed initial load
_model = None
_tokenizer = None


def _load_model_and_tokenizer():
    global _model, _tokenizer
    if _model is not None and _tokenizer is not None:
        return _model, _tokenizer

    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch

    model_name = os.environ.get("MODEL_NAME", "openai/gpt-oss-20b")

    # Choose dtype based on device availability
    if torch.cuda.is_available():
        torch_dtype = torch.float16
        device_map = "auto"
    else:
        # CPU fallback will be extremely slow or may OOM for 20B models
        torch_dtype = torch.float32
        device_map = None

    _tokenizer = AutoTokenizer.from_pretrained(model_name)
    _model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map=device_map,
        torch_dtype=torch_dtype,
    )

    return _model, _tokenizer


def generate_response(prompt: str, max_new_tokens: int = 200) -> str:
    from transformers import StoppingCriteriaList
    import torch

    model, tokenizer = _load_model_and_tokenizer()

    inputs = tokenizer(prompt, return_tensors="pt")

    # Move tensors to model device if necessary
    if hasattr(model, "device"):
        inputs = {k: v.to(model.device) for k, v in inputs.items()}

    output_tokens = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
    )

    text = tokenizer.decode(output_tokens[0], skip_special_tokens=True)
    # Return only the completion beyond the prompt if present
    if text.startswith(prompt):
        return text[len(prompt):].strip()
    return text.strip()


app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "Missing 'prompt'"}), 400

    try:
        reply = generate_response(prompt)
        return jsonify({"response": reply})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    # Bind to 127.0.0.1 to avoid firewall prompts; change to 0.0.0.0 if needed
    app.run(host="127.0.0.1", port=8000, debug=True, threaded=True)


