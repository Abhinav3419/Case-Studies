"""
RAG Pipeline — Medical Knowledge Retrieval
=============================================
Embeds curated medical knowledge into ChromaDB vector store
and retrieves relevant clinical interpretations for biomarker queries.
"""

import os
import json
import hashlib
from typing import Optional

import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer

from .medical_knowledge import get_all_chunks

# Paths
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "vectordb")
COLLECTION_NAME = "medscan_medical_kb"


class MedicalRAG:
    """Retrieval-Augmented Generation pipeline for clinical knowledge."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", persist_dir: str = DB_DIR):
        self.persist_dir = persist_dir
        os.makedirs(persist_dir, exist_ok=True)

        # Load embedding model
        print(f"[RAG] Loading embedding model: {model_name}")
        self.embedder = SentenceTransformer(model_name)

        # Init ChromaDB
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"[RAG] ChromaDB collection '{COLLECTION_NAME}' — {self.collection.count()} docs")

    def _chunk_hash(self, chunk: dict) -> str:
        """Deterministic hash for deduplication."""
        return hashlib.md5(chunk["content"].encode()).hexdigest()[:12]

    def build_index(self, force_rebuild: bool = False):
        """Embed and index all medical knowledge chunks."""
        chunks = get_all_chunks()

        if self.collection.count() >= len(chunks) and not force_rebuild:
            print(f"[RAG] Index already built ({self.collection.count()} docs). Skipping.")
            return

        if force_rebuild:
            self.client.delete_collection(COLLECTION_NAME)
            self.collection = self.client.get_or_create_collection(
                name=COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )

        print(f"[RAG] Indexing {len(chunks)} medical knowledge chunks...")

        ids = []
        documents = []
        metadatas = []
        embeddings = []

        for chunk in chunks:
            # Compose searchable text: title + content + tags
            search_text = f"{chunk['title']}. {chunk['content']} Tags: {', '.join(chunk['tags'])}"

            ids.append(chunk["id"])
            documents.append(search_text)
            metadatas.append({
                "category": chunk["category"],
                "title": chunk["title"],
                "source": chunk["source"],
                "tags": json.dumps(chunk["tags"]),
            })

        # Batch embed
        print("[RAG] Generating embeddings...")
        all_embeddings = self.embedder.encode(documents, show_progress_bar=True, batch_size=8)

        # Upsert into ChromaDB
        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=all_embeddings.tolist(),
        )

        print(f"[RAG] Indexed {len(ids)} chunks. Collection size: {self.collection.count()}")

    def query(self, query_text: str, n_results: int = 5, category_filter: Optional[str] = None) -> list[dict]:
        """
        Retrieve relevant medical knowledge for a query.

        Args:
            query_text: Natural language query (e.g., "elevated TSH with low T4")
            n_results: Number of results to return
            category_filter: Optional category filter (e.g., "Thyroid")

        Returns:
            List of {id, title, content, source, tags, score} dicts, ranked by relevance.
        """
        # Embed query
        query_embedding = self.embedder.encode([query_text]).tolist()

        # Build where filter
        where_filter = None
        if category_filter:
            where_filter = {"category": category_filter}

        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        # Format results
        formatted = []
        for i in range(len(results["ids"][0])):
            meta = results["metadatas"][0][i]
            distance = results["distances"][0][i]
            # Cosine distance → similarity: similarity = 1 - distance
            similarity = round(1 - distance, 4)

            formatted.append({
                "id": results["ids"][0][i],
                "title": meta["title"],
                "content": results["documents"][0][i],
                "source": meta["source"],
                "tags": json.loads(meta["tags"]),
                "category": meta["category"],
                "similarity": similarity,
            })

        return formatted

    def query_for_biomarker(self, biomarker_name: str, flag: str, value: float = None,
                            interpretation_band: str = "", n_results: int = 3) -> list[dict]:
        """
        Specialized query for a specific biomarker result.

        Constructs an optimal query from the biomarker context.
        """
        # Build context-rich query
        parts = [biomarker_name]
        if flag in ("HIGH", "CRITICAL_HIGH"):
            parts.append("elevated high above normal")
        elif flag in ("LOW", "CRITICAL_LOW"):
            parts.append("low below normal deficiency")

        if interpretation_band:
            parts.append(interpretation_band)

        if value is not None:
            parts.append(f"value {value}")

        query = " ".join(parts)
        return self.query(query, n_results=n_results)

    def query_for_patterns(self, abnormal_biomarkers: list[dict], n_results: int = 3) -> list[dict]:
        """
        Query for combined pattern analysis based on multiple abnormal biomarkers.

        Args:
            abnormal_biomarkers: List of {canonical_name, flag, category} dicts
        """
        # Build a combined query from all abnormal biomarkers
        keywords = []
        for b in abnormal_biomarkers:
            keywords.append(b.get("canonical_name", ""))
            if b.get("flag", "").startswith("HIGH"):
                keywords.append("elevated")
            elif b.get("flag", "").startswith("LOW"):
                keywords.append("low deficiency")
            keywords.append(b.get("category", ""))

        query = " ".join(keywords) + " combined pattern analysis"
        return self.query(query, n_results=n_results, category_filter="Combined Analysis")


def build_and_test():
    """Build the index and run test queries."""
    rag = MedicalRAG()
    rag.build_index(force_rebuild=True)

    print("\n" + "=" * 60)
    print("TEST QUERIES")
    print("=" * 60)

    # Test 1: Elevated TSH
    print("\n--- Query: 'elevated TSH hypothyroidism' ---")
    results = rag.query("elevated TSH hypothyroidism", n_results=3)
    for r in results:
        print(f"  [{r['similarity']:.3f}] {r['title']} ({r['category']})")

    # Test 2: Low Vitamin D
    print("\n--- Query: 'vitamin D deficiency low' ---")
    results = rag.query("vitamin D deficiency low", n_results=3)
    for r in results:
        print(f"  [{r['similarity']:.3f}] {r['title']} ({r['category']})")

    # Test 3: Biomarker-specific query
    print("\n--- Biomarker Query: HbA1c HIGH, band=prediabetes ---")
    results = rag.query_for_biomarker("HbA1c", "HIGH", value=6.1, interpretation_band="prediabetes")
    for r in results:
        print(f"  [{r['similarity']:.3f}] {r['title']} ({r['category']})")

    # Test 4: Combined pattern
    print("\n--- Pattern Query: TSH high + LDL high + Vitamin D low ---")
    abnormals = [
        {"canonical_name": "tsh", "flag": "HIGH", "category": "Thyroid"},
        {"canonical_name": "ldl_cholesterol", "flag": "HIGH", "category": "Lipid Profile"},
        {"canonical_name": "vitamin_d", "flag": "LOW", "category": "Vitamins"},
    ]
    results = rag.query_for_patterns(abnormals, n_results=3)
    for r in results:
        print(f"  [{r['similarity']:.3f}] {r['title']} ({r['category']})")

    # Test 5: Iron panel
    print("\n--- Query: 'low ferritin high TIBC low transferrin saturation iron deficiency' ---")
    results = rag.query("low ferritin high TIBC low transferrin saturation iron deficiency", n_results=3)
    for r in results:
        print(f"  [{r['similarity']:.3f}] {r['title']} ({r['category']})")

    return rag


if __name__ == "__main__":
    build_and_test()
