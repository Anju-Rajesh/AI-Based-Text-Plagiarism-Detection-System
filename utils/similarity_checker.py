from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(text1, text2):
    """
    Compares two texts and returns their similarity percentage.
    Uses TF-IDF Vectorization and Cosine Similarity.
    """
    # 1. Validation: Ensure both texts have content
    if not text1.strip() or not text2.strip():
        return 0.0
    
    # 2. Vectorization (Convert words to math numbers)
    # TfidfVectorizer converts text into a meaningful matrix of numbers.
    vectorizer = TfidfVectorizer()
    
    try:
        # Fit and transform the texts into vectors
        tfidf = vectorizer.fit_transform([text1, text2])
        
        # 3. Calculate Cosine Similarity
        # Measures the angle between the two vectors.
        # Result is a matrix [[1.0, 0.85], [0.85, 1.0]]
        # We take the value at [0][1] which compares text1 vs text2
        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])
        
        # Convert 0.85 -> 85.0%
        return round(float(sim[0][0]) * 100, 2)
        
    except Exception as e:
        print(f"Error in similarity calculation: {e}")
        return 0.0








