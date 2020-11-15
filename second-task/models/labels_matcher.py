from typing import Tuple, List

import spacy

nlp = spacy.load('en_core_web_sm')
EXPECTED_LABELS = [
    'Animals', 'Bench', 'Building', 'Castle', 'Cave', 'Church',
    'City', 'Cross', 'Cultural institution', 'Food', 'Footpath',
    'Forest', 'Furniture', 'Grass', 'Graveyard', 'Lake', 'Landscape',
    'Mine', 'Monument', 'Motor vehicle', 'Mountains', 'Museum',
    'Open-air museum', 'Park', 'Person', 'Plants', 'Reservoir', 'River',
    'Road', 'Rocks', 'Snow', 'Sport', 'Sports facility', 'Stairs', 'Trees',
    'Watercraft', 'Windows'
]
EXPECTED_TOKENS = [nlp(token) for token in EXPECTED_LABELS]

def get_similar_label(label: str,  similarity_threshold: float = 0.55) -> List[str]:
    token = nlp(label)
    return [
        expected_token.text for expected_token in EXPECTED_TOKENS
        if token.similarity(expected_token) > similarity_threshold
    ]
