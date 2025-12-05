from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from dotenv import load_dotenv
import os
import torch
import numpy as np
import re
from typing import List

story_text: str = """John walked into the forest. He heard rustling behind him. The trees loomed tall as he pressed forward, his heart pounding. Later that night, he found a small cabin. It looked abandoned, but the door creaked open when he pushed it. The wind howled outside as he stepped in. Inside the cabin, an old man sat by the fire. He wore a long cloak and stared at John as if expecting him. In the morning, John woke up to find the man missing. The fire had gone cold. He stepped outside and saw footprints leading into the misty woods. With no other choice, he followed the footprints. The deeper he went, the more uneasy he felt, as if someone—or something—was watching him."""

def split_into_sentences(text: str) -> List[str]:
    """
    Splits a given text into a list of sentences based on punctuation.

    Args:
        text (str): The input text to split.

    Returns:
        List[str]: A list of sentences found in the text.
    """
    return re.findall(r"[^.!?]+", text)

def main(story_text: str, threshold: float = 0.5) -> List[str]:
    """
    Splits the story text into meaningful scenes using semantic similarity.

    Args:
        story_text (str): The full text of the story.
        threshold (float): The similarity threshold for merging sentences. Defaults to 0.5.

    Returns:
        List[str]: A list of merged sentences representing scenes.
    """
    index_name = "text-search"
    sentences = split_into_sentences(story_text)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using", device)

    load_dotenv()
    api_key = os.getenv("PINECONE_ANIMEGEN_API_KEY")
    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)

    # Load the SentenceTransformer model for generating text embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")
    # Generate embeddings for all sentences at once
    embeddings = model.encode(sentences)

    merged_sentences = []
    similarity_array = []
    i = 0
    # Iterate through sentences to determine if they should be merged
    while i < len(sentences) - 1:
        # Get embeddings for current and next sentence
        vector_1, vector_2 = embeddings[i], embeddings[i + 1]
        
        # Example of querying Pinecone index (if used in future)
        response = index.query(vector=vector_1.tolist(), top_k=1, include_values=True)
        
        # Calculate Cosine Similarity between the two sentence vectors
        # Formula: (A . B) / (||A|| * ||B||)
        similarity = np.dot(vector_1, vector_2) / (np.linalg.norm(vector_1) * np.linalg.norm(vector_2))
        
        similarity_array.append([similarity,sentences[i],sentences[i+1]])
        
        # If sentences are similar enough, merge them into one scene
        if similarity >= threshold:
            sentences[i + 1] = sentences[i] + ". " + sentences[i + 1]
        else:
            # Otherwise, the current sentence is a complete scene
            merged_sentences.append(sentences[i])
        
        i += 1
    
    # Append the last sentence/scene
    merged_sentences.append(sentences[-1])
    return merged_sentences

if __name__ == "__main__":
    print(main(story_text))