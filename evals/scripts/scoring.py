#!/usr/bin/env python3
"""Deterministic scoring metrics for the cognitive-skills eval harness.

No LLM calls. Every metric is reproducible from the output text alone:
- structural checks (presence of required sections / phrases)
- length characteristics (word and section counts)
- tf-idf cosine similarity against a per-task voice corpus

The harness uses these metrics to compare arms (`baseline`, `ceet`,
`generic`) on the same task. The host model is whatever is invoking the
skill; this scorer never calls a model.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Iterable


WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z'-]+")


def tokenize(text: str) -> list[str]:
    """Lower-case word tokens. Keeps apostrophes inside words."""
    return [w.lower() for w in WORD_RE.findall(text)]


def section_count(text: str) -> int:
    """Count Markdown headings (lines starting with `#`)."""
    return sum(1 for line in text.splitlines() if line.lstrip().startswith("#"))


def word_count(text: str) -> int:
    return len(tokenize(text))


def required_phrase_hits(text: str, phrases: Iterable[str]) -> dict[str, bool]:
    """Return {phrase: present} for each required phrase (case-insensitive)."""
    lc = text.lower()
    return {phrase: phrase.lower() in lc for phrase in phrases}


def required_section_hits(text: str, sections: Iterable[str]) -> dict[str, bool]:
    """Return {section: present} treating each entry as a heading substring."""
    headings = [
        line.lstrip("# ").strip().lower()
        for line in text.splitlines()
        if line.lstrip().startswith("#")
    ]
    return {section: any(section.lower() in h for h in headings) for section in sections}


def tf_idf(documents: list[list[str]]) -> list[dict[str, float]]:
    """Compute tf-idf weights for each document. Pure stdlib."""
    df: Counter[str] = Counter()
    for tokens in documents:
        df.update(set(tokens))
    n = len(documents)
    weights: list[dict[str, float]] = []
    for tokens in documents:
        tf = Counter(tokens)
        total = sum(tf.values()) or 1
        weights.append(
            {
                term: (count / total) * math.log((1 + n) / (1 + df[term]))
                for term, count in tf.items()
            }
        )
    return weights


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    dot = sum(a[t] * b[t] for t in common)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "of", "to", "in", "on",
    "for", "with", "is", "are", "was", "were", "be", "as", "at", "by",
    "this", "that", "it", "its", "from", "you", "your", "we", "our",
    "they", "their", "i", "my", "me", "have", "has", "had", "will",
    "would", "should", "can", "could", "may", "might", "do", "does",
    "did", "not", "no", "so", "than", "then", "there", "these", "those",
    "what", "which", "who", "when", "where", "how", "all", "any", "some",
    "one", "two", "three", "more", "less", "very", "also", "just",
    "only", "even", "into", "out", "up", "down", "over", "under",
}


def _tf_vector(tokens: list[str]) -> dict[str, float]:
    """Term-frequency vector with stopwords removed and length-normalized."""
    filtered = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    if not filtered:
        return {}
    counts = Counter(filtered)
    total = sum(counts.values())
    return {term: count / total for term, count in counts.items()}


def voice_alignment(output: str, corpus: str) -> float:
    """Cosine similarity of length-normalized TF vectors (stopwords removed).

    Higher = the output draws from the same vocabulary the CEET pack
    cultivates. We use plain TF cosine instead of TF-IDF because TF-IDF
    over a 2-document set cancels out exactly the vocabulary we want
    to score. This metric is meaningful as a *delta* between arms on
    the same task; it is not a standalone quality score.
    """
    output_tokens = tokenize(output)
    corpus_tokens = tokenize(corpus)
    if not output_tokens or not corpus_tokens:
        return 0.0
    return round(cosine(_tf_vector(output_tokens), _tf_vector(corpus_tokens)), 4)


def score_output(text: str, criteria: dict, corpus: str | None = None) -> dict:
    """Apply every metric defined in `criteria` to `text` and return a flat dict."""
    expected_phrases = criteria.get("requiredPhrases", [])
    expected_sections = criteria.get("requiredSections", [])
    min_words = criteria.get("minWords")
    max_words = criteria.get("maxWords")

    phrase_results = required_phrase_hits(text, expected_phrases)
    section_results = required_section_hits(text, expected_sections)
    words = word_count(text)
    sections = section_count(text)

    coverage_phrases = (
        sum(phrase_results.values()) / len(phrase_results) if phrase_results else 1.0
    )
    coverage_sections = (
        sum(section_results.values()) / len(section_results) if section_results else 1.0
    )

    length_ok = (
        (min_words is None or words >= min_words)
        and (max_words is None or words <= max_words)
    )

    voice_score = voice_alignment(text, corpus) if corpus else None

    return {
        "wordCount": words,
        "sectionCount": sections,
        "lengthWithinBounds": length_ok,
        "phraseCoverage": round(coverage_phrases, 4),
        "phraseHits": phrase_results,
        "sectionCoverage": round(coverage_sections, 4),
        "sectionHits": section_results,
        "voiceAlignment": voice_score,
        "compositeScore": round(
            (coverage_phrases + coverage_sections + (voice_score or 0)) / (3 if voice_score is not None else 2),
            4,
        ),
    }
