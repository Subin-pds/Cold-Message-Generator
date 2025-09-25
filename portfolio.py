import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self, file_path="C:\GenAI Projects\Cold Message Generator\App\Resources\AI_Skills_JobLinks.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.client = chromadb.PersistentClient("vector_store")
        self.collection = self.client.get_or_create_collection(name="portfolio_collection")

    def add_to_vector_store(self):
        if not self.collection.count():
            for _,row in self.data.iterrows():
                self.collection.add(
                    documents= row['Skills'],
                    metadatas={'links':row['Portfolio']},
                    ids=[str(uuid.uuid4())]
        )

    def query_portfolio(self, skills, n_results=2):
        print("Querying portfolio with skills:", skills)
        print(self.collection.query(query_texts= skills, n_results=n_results).get('metadatas', []))
        return self.collection.query(query_texts= skills, n_results=n_results).get('metadatas', [])[0]