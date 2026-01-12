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
    
    # AI detection metrics (simplified heuristic for demo/local NLP)
    # 1. AI often uses more uniform sentence lengths
    sent_lengths = [len(word_tokenize(s)) for s in sentences]
    avg_sent_length = sum(sent_lengths) / len(sent_lengths)
    sent_length_var = sum((l - avg_sent_length)**2 for l in sent_lengths) / len(sent_lengths)
    
    # 2. Vocabulary richness (AI often has lower TTR than diverse human writing)
    vocab_richness = calculate_vocabulary_richness(words)
    
    # 3. Repetition patterns
    repetition = calculate_repetition_pattern(words)
    
    # Heuristic score calculation
    # Low variance in sentence length + high repetition + low vocab richness -> likely AI
    ai_score = 0
    
    # Variance check (lower variance = more robotic)
    if sent_length_var < 20: 
        ai_score += 30
    elif sent_length_var < 50:
        ai_score += 15
        
    # Vocab richness check (lower = more robotic)
    if vocab_richness < 0.4:
        ai_score += 30
    elif vocab_richness < 0.6:
        ai_score += 15
        
    # Repetition check (higher = more robotic)
    if repetition > 0.3:
        ai_score += 40
    elif repetition > 0.15:
        ai_score += 20
        
    # Cap at 100
    ai_score = min(99.9, ai_score)
    
    conclusion = "Likely AI-generated" if ai_score > 50 else "Likely Human-written"
    
    return round(ai_score, 2), conclusion
