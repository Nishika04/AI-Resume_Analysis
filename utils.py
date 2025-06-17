import fitz
import re

def read_all_pdf_pages(pdf_path):
    text = ''
    with fitz.open(pdf_path) as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
    return text

def extract_relevant_sections(text):
    section_aliases = {
        "summary": ["summary", "objective", "about me", "career objective"],
        "skills": ["skills", "technical skills", "tools & technologies"],
        "experience": ["experience", "work history", "professional background", "employment"],
        "education": ["education", "academic background", "qualifications"],
        "projects": ["projects", "notable work", "academic projects"]
    }

    extracted_sections = {}
    lower_text = text.lower()

    for section, aliases in section_aliases.items():
        for alias in aliases:
            pattern = rf"{alias}\s*[:\-]?\s*(.*?)(?=\n(?:{'|'.join([re.escape(a) for a in sum(section_aliases.values(), [])])})\s*[:\-]|\Z)"
            match = re.search(pattern, lower_text, re.DOTALL)
            if match:
                content = match.group(1).strip()
                if content:
                    extracted_sections[section] = content
                    break
    return extracted_sections

def generate_short_resume(extracted_sections):
    return "\n\n".join(
        f"{section.capitalize()}:\n{content}" for section, content in extracted_sections.items()
    )

import hashlib

import hashlib

def generate_cache_hash(resume_content: str, job_desire: str) -> str:
    """Create a stable hash based on resume content and desired job"""
    hash_input = (resume_content + job_desire).encode('utf-8')
    return hashlib.md5(hash_input).hexdigest()

import os
import json

def load_or_create_task(task, output_filename, cache_hash):
    # Create cache directory for this unique hash
    cache_dir = os.path.join("resume-report", cache_hash)
    os.makedirs(cache_dir, exist_ok=True)

    # Full path to the output file
    output_path = os.path.join(cache_dir, os.path.basename(output_filename))

    if os.path.exists(output_path):
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                if output_path.endswith(".json"):
                    json.load(f)
                elif output_path.endswith(".txt"):
                    if not f.read().strip():
                        raise ValueError("Empty file")
            print(f"[CACHE HIT] Loaded cached result from {output_path}")
            return None  # Skip task
        except Exception as e:
            print(f"[CACHE CORRUPTED] {output_path}: {e}, regenerating...")

    print(f"[CACHE MISS] Generating result for {output_path}")
    return task