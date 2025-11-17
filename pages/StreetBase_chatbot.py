import os
from openai import OpenAI
from sentence_transformers import SentenceTransformer, util
from PyPDF2 import PdfReader
import torch
import re

os.environ["TOKENIZERS_PARALLELISM"] = "false"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

embedder = SentenceTransformer("all-MiniLM-L6-v2")

# PDF Extraction
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            t = re.sub(r"\s+", " ", t)
            text += t.strip() + "\n"
    return text


def chunk_text(text, words_per_chunk=800):
    words = text.split()
    return [
        " ".join(words[i:i + words_per_chunk])
        for i in range(0, len(words), words_per_chunk)
    ]

def init_bot(pdf_path="StreetBase_KB.pdf"):
    print("📄 Loading PDF...")
    pdf_text = extract_text_from_pdf(pdf_path)

    if not pdf_text.strip():
        raise ValueError("PDF extraction returned empty text.")

    chunks = chunk_text(pdf_text)
    print(f"🔧 Creating embeddings for {len(chunks)} chunks...")

    chunk_embeddings = embedder.encode(chunks, convert_to_tensor=True)

    print("🤖 Chatbot Backend Ready!")
    return chunks, chunk_embeddings

def answer_query(query, chunks, chunk_embeddings):

    query_emb = embedder.encode(query, convert_to_tensor=True)

    similarities = util.cos_sim(query_emb, chunk_embeddings)[0]
    best_index = torch.argmax(similarities).item()
    best_chunk = chunks[best_index]

    prompt = f"""
Use the following PDF context to answer clearly and accurately.

CONTEXT:
{best_chunk}

QUESTION:
{query}

ANSWER:
"""

    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=[
            {"role": "system", "content": "You are an expert assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.2
    )

    return response.choices[0].message.content
