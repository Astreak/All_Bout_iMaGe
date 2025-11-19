import os
import shutil
shutil.rmtree("image")


import numpy as np
from transformers import AutoTokenizer

def predict_text_simple(session, text, max_length=128):
    """
    Minimal DistilBERT-ONNX inference:
      - Hard-coded categories
      - Tokenize -> ONNX -> softmax -> top label

    Args:
        session: onnxruntime.InferenceSession loaded on your model.onnx
        text (str): input text
        max_length (int): tokenizer truncation length

    Returns:
        dict: {"label": <category>, "score": <float>}
    """
    # Hard-coded categories (index 0..3 must match your model's class order)
    CATEGORIES = ["finance", "risk", "trading", "others"]

    # 1) Tokenize (NumPy int64 for ORT)
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased", use_fast=True)
    enc = tokenizer(text, return_tensors="np", padding=True, truncation=True, max_length=max_length)
    input_ids = enc["input_ids"].astype(np.int64)
    attention_mask = enc["attention_mask"].astype(np.int64)

    # 2) Build feed dict from model input names
    input_names = [i.name for i in session.get_inputs()]
    feed = {}
    if "input_ids" in input_names:
        feed["input_ids"] = input_ids
    if "attention_mask" in input_names:
        feed["attention_mask"] = attention_mask
    if "token_type_ids" in input_names:
        feed["token_type_ids"] = np.zeros_like(input_ids, dtype=np.int64)  # DistilBERT rarely needs this

    # 3) Run model
    output_names = [o.name for o in session.get_outputs()]
    outputs = session.run(output_names, feed)
    name_to_idx = {n: i for i, n in enumerate(output_names)}
    logits = outputs[name_to_idx["logits"]] if "logits" in name_to_idx else outputs[0]  # [1, C]

    # 4) Softmax and argmax
    logits = logits.astype(np.float32)
    logits -= logits.max(axis=1, keepdims=True)
    probs = np.exp(logits)
    probs /= probs.sum(axis=1, keepdims=True)
    probs = probs[0]  # [C]

    top = int(np.argmax(probs))
    label = CATEGORIES[top] if top < len(CATEGORIES) else f"LABEL_{top}"
    return {"label": label, "score": float(probs[top])}