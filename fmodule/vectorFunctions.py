import torch
from transformers import AutoTokenizer, AutoModel
import torch.nn.functional as F

_model = None
_tokenizer = None
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_embedding_model_and_tokenizer(
    model_ckpt="sentence-transformers/all-MiniLM-L6-v2"
):
    global _model, _tokenizer

    if _model is None or _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
        _model = AutoModel.from_pretrained(model_ckpt)
        _model.to(_device)
        _model.eval()

    return _model, _tokenizer

def get_model_and_tokenizer():
    if _model is None or _tokenizer is None:
        raise RuntimeError("Embedding model not loaded")
    return _model, _tokenizer

def generate_embeddings(texts, batch_size=32, max_length=512):
    model, tokenizer = get_model_and_tokenizer()
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i : i + batch_size]

        encoded_input = tokenizer(
            batch_texts,
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors="pt",
        )

        encoded_input = {k: v.to(_device) for k, v in encoded_input.items()}

        with torch.no_grad():
            model_output = model(**encoded_input)

        sentence_embeddings = mean_pooling(
            model_output, encoded_input["attention_mask"]
        )
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

        all_embeddings.extend(sentence_embeddings.cpu().tolist())

    return all_embeddings

# -------------------- #

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output.last_hidden_state
    input_mask_expanded = (
        attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    )
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
        input_mask_expanded.sum(1), min=1e-9
    )