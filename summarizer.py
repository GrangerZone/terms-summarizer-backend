# summarizer.py

from transformers import pipeline

# Load summarization pipeline once at startup
summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str, min_length: int = 200, max_length: int = 300) -> str:
    """
    Summarizes input text into something between 200 and 300 words.
    """
    if not text.strip():
        return "Error: No text provided for summarization."

    # Hugging Face models work on token lengths, not exact words.
    # We approximate by setting min_length and max_length.
    try:
        summary = summarizer_pipeline(
            text,
            min_length=min_length,
            max_length=max_length,
            do_sample=False
        )
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error during summarization: {str(e)}"
