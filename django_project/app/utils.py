from transformers import pipeline, set_seed
from random import randint


summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
# summarizer = pipeline("summarization", model="google/pegasus-xsum")


def generate_summary(text):
    set_seed(randint(1, 1000))
    return summarizer(text, min_length=5, max_length=50, do_sample=True)[0]['summary_text']
