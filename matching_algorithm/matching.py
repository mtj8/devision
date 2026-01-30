from dataclasses import dataclass
from typing import List, Set
from sentence_transformers import SentenceTransformer
import numpy as np

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded.")

#Data classes
@dataclass
class Skill:
    id: int
    name: str

@dataclass
class Interest:
    id: int
    name: str

@dataclass
class GradYear:
    gradYear: int

@dataclass
class User:
    id: int
    gradYear: int
    bio: str
    level: int            
    xp: int               
    skills: List[Skill]
    interests: List[Interest]
    interest_vecs: list = None
    skill_vecs: list = None
    bio_vec: list = None


# Matching functions 
def jaccard(set_a, set_b):
    if not set_a and not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)

def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def avg_pairwise(vecs1, vecs2):
    if vecs1 is None or vecs2 is None:
        return 0
    if len(vecs1) == 0 or len(vecs2) == 0:
        return 0
    sims = [
        cosine(v1, v2)
        for v1 in vecs1
        for v2 in vecs2
    ]
    return sum(sims) / len(sims)

def embed_user(user: User):
    interest_texts = [i.name for i in user.interests]
    skill_texts = [s.name for s in user.skills]
    bio_text = user.bio or ""

    texts = interest_texts + skill_texts + [bio_text]
    embeddings = model.encode(texts)

    n_int = len(interest_texts)
    n_skill = len(skill_texts)

    user.interest_vecs = embeddings[:n_int]
    user.skill_vecs = embeddings[n_int:n_int+n_skill]
    user.bio_vec = embeddings[-1]

    return user

def compute_match_score(u1: User, u2: User) -> float:
    """
    A simple scoring function using:
    - Skill overlap
    - Interest overlap
    - Level proximity
    """

    # Semantic Similarity
    S_skills = avg_pairwise(u1.skill_vecs, u2.skill_vecs)
    S_interests = avg_pairwise(u1.interest_vecs, u2.interest_vecs)
    S_bio = cosine(u1.bio_vec, u2.bio_vec)

    # Closer scores higher
    S_level = max(0, 1 - abs(u1.level - u2.level) / 5)
    S_gradYear = max(0, 1 - abs(u1.gradYear - u2.gradYear)/2)

    # Final weighted score
    score = (
        0.40 * S_skills +
        0.25 * S_interests +
        0.15 * S_bio +
        0.10 * S_level +
        0.10 * S_gradYear
    )

    return score
