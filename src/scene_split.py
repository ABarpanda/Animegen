from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from dotenv import load_dotenv
import os
import torch
import numpy as np
import re

# Example story text for testing
story_text = """John walked into the forest. He heard rustling behind him. The trees loomed tall as he pressed forward, his heart pounding. Later that night, he found a small cabin. It looked abandoned, but the door creaked open when he pushed it. The wind howled outside as he stepped in. Inside the cabin, an old man sat by the fire. He wore a long cloak and stared at John as if expecting him. In the morning, John woke up to find the man missing. The fire had gone cold. He stepped outside and saw footprints leading into the misty woods. With no other choice, he followed the footprints. The deeper he went, the more uneasy he felt, as if someone—or something—was watching him."""

def split_into_sentences(text):
    """
    Splits a given text into individual sentences based on punctuation marks.

    Args:
        text (str): The input story or text to split.

    Returns:
        list: A list of sentences extracted from the input text.
    """
    return re.findall(r"[^.!?]+", text)

def main(story_text, threshold=0.5):
    """
    Splits a story text into sentences and merges them based on semantic similarity.

    The function uses SentenceTransformer to generate sentence embeddings and
    calculates cosine similarity between adjacent sentences. If the similarity
    between two consecutive sentences is greater than or equal to the threshold,
    they are merged into one sentence.

    Args:
        story_text (str): The story or text to process.
        threshold (float, optional): The cosine similarity threshold to decide
                                      whether two sentences should be merged. Defaults to 0.5.

    Returns:
        list: A list of merged sentences after comparing their similarity.
    """
    index_name = "animegen"
    sentences = split_into_sentences(story_text)

    # Use GPU if available, otherwise fallback to CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using", device)

    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv("PINECONE_ANIMEGEN_API_KEY")
    pc = Pinecone(api_key=api_key)  # Initialize Pinecone with API key
    index = pc.Index(index_name)  # Access the Pinecone index for querying

    # Load the pre-trained sentence transformer model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(sentences)  # Encode sentences into embeddings

    merged_sentences = []  # List to store final merged sentences
    similarity_array = []  # List to store the similarity results for each pair
    i = 0

    # Iterate through sentences and merge based on similarity threshold
    while i < len(sentences) - 1:
        vector_1, vector_2 = embeddings[i], embeddings[i + 1]
        
        # Query Pinecone index to find top-k most similar vectors
        response = index.query(vector=vector_1.tolist(), top_k=1, include_values=True)
        
        # Calculate cosine similarity between two consecutive sentence vectors
        similarity = np.dot(vector_1, vector_2) / (np.linalg.norm(vector_1) * np.linalg.norm(vector_2))
        similarity_array.append([similarity, sentences[i], sentences[i + 1]])
        
        # If similarity is above the threshold, merge sentences
        if similarity >= threshold:
            sentences[i + 1] = sentences[i] + ". " + sentences[i + 1]
        else:
            merged_sentences.append(sentences[i])
        
        i += 1
    
    # Add the last sentence to the merged list
    merged_sentences.append(sentences[-1])

    return merged_sentences

if __name__ == "__main__":
    # Print the merged sentences after processing the story text
    print(main(story_text))
