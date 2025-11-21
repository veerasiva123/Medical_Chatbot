from typing import List, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

_vectorizer: Optional[TfidfVectorizer] = None


def embed_texts(texts: List[str], fit: bool = False) -> np.ndarray:
    """Embed texts into TF-IDF vectors (local, no external API)."""
    global _vectorizer

    if fit or _vectorizer is None:
        _vectorizer = TfidfVectorizer(max_features=8192)
        mat = _vectorizer.fit_transform(texts)
    else:
        mat = _vectorizer.transform(texts)

    return mat.astype("float32").toarray()