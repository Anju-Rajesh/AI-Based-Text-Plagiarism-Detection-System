import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
import math


# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def calculate_vocabulary_richness(words):
    if not words:
        return 0
    return len(set(words)) / len(words)

def calculate_repetition_pattern(words):
    if not words:
        return 0
    word_counts = Counter(words)
    # Average frequency of the top 3% of words
    num_top = max(1, math.ceil(len(word_counts) * 0.03))
    most_common = word_counts.most_common(num_top)
    avg_freq = sum(count for word, count in most_common) / num_top
    # Normalize by total words
    return min(1.0, avg_freq / (len(words) / 10) if len(words) > 0 else 0)

def analyze_text_ai(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    
    if not words or not sentences:
        return 0, "Unknown"
    
    # 1. Burstiness / Sentence Length Variation
    # AI tends to have more uniform sentence lengths (low variation).
    # Humans vary sentence length significantly (high variation).
    sent_lengths = [len(word_tokenize(s)) for s in sentences]
    if len(sent_lengths) > 1:
        avg_sent_length = sum(sent_lengths) / len(sent_lengths)
        sent_length_var = sum((l - avg_sent_length)**2 for l in sent_lengths) / len(sent_lengths)
        sent_length_std = math.sqrt(sent_length_var)
        # Coefficient of Variation (CV) is a better metric than raw variance as it accounts for scale
        sent_len_cv = sent_length_std / avg_sent_length if avg_sent_length > 0 else 0
    else:
        sent_len_cv = 0

    # 2. Vocabulary Richness (TTR)
    # AI often uses a consistent vocabulary.
    vocab_richness = calculate_vocabulary_richness(words)
    
    # 3. Repetition Patterns
    repetition = calculate_repetition_pattern(words)
    
    # --- Continuous Scoring Logic ---
    # We define probabilities based on these metrics.
    
    # Sentence Variation Score (Higher CV = Human, Lower CV = AI)
    # Typical Human CV is ~0.5 to 0.7. AI is often < 0.4.
    # Sigmoid-like mapping:
    # If CV < 0.3 -> High AI Score
    # If CV > 0.6 -> Low AI Score
    # We'll map CV 0.2 (very uniform) -> 100% AI score
    # CV 0.6 (very varied) -> 0% AI score
    burstiness_score = max(0, min(100, (0.6 - sent_len_cv) * (100 / 0.4)))
    
    # Vocab Score (Lower TTR = AI, Higher TTR = Human)
    # TTR varies by text length, so this is weak. 
    # But generally TTR < 0.4 is repetitive/AI-like (or simple human).
    # TTR > 0.7 is rich/Human.
    vocab_score = max(0, min(100, (0.7 - vocab_richness) * (100 / 0.3)))
    
    # Repetition Score (Higher = AI)
    # > 0.2 is high repetition
    repetition_score = max(0, min(100, (repetition - 0.1) * (100 / 0.2)))
    
    # Weighted Average
    # Burstiness is best proxy for style. Repetition is a strong signal for bad AI or spam.
    # Weights: Burstiness 50%, Vocab 20%, Repetition 30%
    ai_score = (burstiness_score * 0.5) + (vocab_score * 0.2) + (repetition_score * 0.3)
    
    # Length Penalty
    # If text is too short, confidence should be lower (or score essentially random/neutral).
    # But for now, we just return the calculation.
    
    # Formatting
    ai_score = round(ai_score, 2)
    
    if ai_score > 85:
        conclusion = "Highly Likely AI-generated"
    elif ai_score > 60:
        conclusion = "Likely AI-generated"
    elif ai_score > 40:
        conclusion = "Uncertain / Mixed"
    else:
        conclusion = "Likely Human-written"
        
    return ai_score, conclusion




