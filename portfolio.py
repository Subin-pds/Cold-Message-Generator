import os
import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path: str | None = None):
        if file_path is None:
            file_path = os.path.join(os.path.dirname(__file__), "Resources", "AI_Skills_JobLinks.csv")
        self.file_path = file_path
        self.data = pd.read_csv(self.file_path)
        self.client = chromadb.PersistentClient("vector_store")
        self.collection = self.client.get_or_create_collection(name="portfolio_collection")

    def add_to_vector_store(self):
        # Add rows to the vector store; ensure inputs are lists as required by chroma
        try:
            if not self.collection.count():
                for _, row in self.data.iterrows():
                    doc = str(row.get('Skills', '')).strip()
                    link = row.get('Portfolio', '')
                    if not doc:
                        continue
                    self.collection.add(
                        documents=[doc],
                        metadatas=[{'links': link}],
                        ids=[str(uuid.uuid4())]
                    )
        except Exception:
            # If collection.count() or add() isn't supported in this runtime, skip silently
            pass

    def query_portfolio(self, skills, n_results=2):
        # Normalize skills into a non-empty list of strings for query_texts
        print("Querying portfolio with skills:", skills)
        if not skills:
            return []

        if isinstance(skills, str):
            query_texts = [skills]
        elif isinstance(skills, list):
            # flatten nested lists/dicts into strings
            query_texts = [str(s) for s in skills if s]
        else:
            query_texts = [str(skills)]

        if not query_texts:
            return []

        result = self.collection.query(query_texts=query_texts, n_results=n_results)
        metadatas = result.get('metadatas', [])

        # Extract links from metadatas result if present
        links = []
        for entry in metadatas:
            if isinstance(entry, list):
                for md in entry:
                    if isinstance(md, dict) and 'links' in md:
                        links.append(md['links'])
            elif isinstance(entry, dict) and 'links' in entry:
                links.append(entry['links'])

        return links