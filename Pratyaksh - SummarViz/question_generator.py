import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from sentence_transformers import SentenceTransformer, util
import textwrap

# Load models once to improve efficiency
t5_model_name = "valhalla/t5-small-qg-prepend"
tokenizer = T5Tokenizer.from_pretrained(t5_model_name)
model = T5ForConditionalGeneration.from_pretrained(t5_model_name)
similarity_model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_questions(text, num_questions=5, top_k=50, top_p=0.95):
    """
    Generates insightful and unique questions from input text.
    """
    input_text = f"question: {text} </s>"
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

    outputs = model.generate(
        inputs,
        max_length=150,
        num_return_sequences=num_questions * 2,  # Generate more for better filtering
        do_sample=True,
        top_k=top_k,
        top_p=top_p,
        temperature=0.7,
        repetition_penalty=1.5,
        early_stopping=True
    )

    decoded_outputs = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    
    valid_questions = filter_valid_questions(decoded_outputs)
    unique_questions = remove_similar_questions(valid_questions)

    return unique_questions[:num_questions]

def filter_valid_questions(questions):
    """
    Filters out generic or incorrect questions.
    """
    filtered = []
    for q in questions:
        q = q.strip()
        if q.endswith("?") and not is_generic_question(q):
            filtered.append(q)
    return filtered

def is_generic_question(question):
    """
    Returns True if the question is vague or irrelevant.
    """
    generic_phrases = [
        "What questions are raised",
        "What types of questions",
        "What kind of information",
        "What does this article say",
        "What are some of the questions",
        "What do these questions generate"
    ]
    return any(phrase in question for phrase in generic_phrases)

def remove_similar_questions(questions, threshold=0.75):
    """
    Removes semantically similar questions using embeddings.
    """
    embeddings = similarity_model.encode(questions, convert_to_tensor=True)
    unique_questions = []
    seen_vectors = []

    for idx, emb in enumerate(embeddings):
        if all(util.cos_sim(emb, seen)[0][0] < threshold for seen in seen_vectors):
            unique_questions.append(questions[idx])
            seen_vectors.append(emb)

    return unique_questions
