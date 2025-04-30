import spacy
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text, top_n=10):
    # Process text
    doc = nlp(text)
    candidates = [token.lemma_.lower() for token in doc
                  if token.pos_ in ["NOUN", "PROPN", "ADJ"]
                  and not token.is_stop
                  and token.is_alpha]
    unique_words = list(set(candidates))

    if len(unique_words) < 2:
        return unique_words

    # Create word vectors
    word_vectors = [nlp(word).vector for word in unique_words]

    # Build similarity matrix
    sim_mat = np.zeros((len(unique_words), len(unique_words)))
    for i in range(len(unique_words)):
        for j in range(len(unique_words)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(
                    word_vectors[i].reshape(1, -1),
                    word_vectors[j].reshape(1, -1)
                )[0, 0]

    # Graph & PageRank
    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)

    # Rank and return keywords
    ranked = sorted(((scores[i], w) for i, w in enumerate(unique_words)), reverse=True)
    return [word for score, word in ranked[:top_n]]

# === Main execution ===
if __name__ == "__main__":
    keywords = extract_keywords(user_text)
    print("\nTop Keywords:")
    for word in keywords:
        print("-", word)
