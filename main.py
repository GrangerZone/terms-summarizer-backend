from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/summarize")
async def summarize(file: UploadFile = File(...)):
    try:
        # 1. Extract text from PDF
        pdf_bytes = await file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text("text")

        if not text.strip():
            return {"summary": "No readable text found in PDF."}

        # 2. Summarize using sumy (LSA)
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()

        # Request 25 sentences for ~200 words
        summary_sentences = summarizer(parser.document, 25)

        # Join sentences into a single summary
        summary = " ".join(str(sentence) for sentence in summary_sentences)

        # 3. Ensure minimum ~200 words
        if len(summary.split()) < 200:
            # If too short, just use a larger chunk of text
            summary = text[:2000]  

        return {"summary": summary}

    except Exception as e:
        return {"error": str(e)}
