# summarizer_model.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

def load_summarizer(model_name="sshleifer/distilbart-cnn-12-6"):
    """Load a Hugging Face summarization model pipeline."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
    return summarizer
