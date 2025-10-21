"""
Vector Store 관리 유틸리티
"""
from typing import List
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from src.config import EMBEDDING_MODEL, VECTOR_STORE_PATH
import os


class VectorStoreManager:
    """Vector Store 관리 클래스"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        self.vector_store = None
    
    def create_vector_store(self, documents: List[Document]) -> FAISS:
        """
        문서로부터 Vector Store 생성
        
        Args:
            documents: Document 객체 리스트
        
        Returns:
            FAISS vector store
        """
        print("🔄 Creating vector store...")
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        print("✅ Vector store created successfully")
        return self.vector_store
    
    def save_vector_store(self, path: str = VECTOR_STORE_PATH):
        """Vector Store 저장"""
        if self.vector_store:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            self.vector_store.save_local(path)
            print(f"💾 Vector store saved to: {path}")
    
    def load_vector_store(self, path: str = VECTOR_STORE_PATH) -> FAISS:
        """저장된 Vector Store 로드"""
        if os.path.exists(path):
            self.vector_store = FAISS.load_local(
                path, 
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"📂 Vector store loaded from: {path}")
            return self.vector_store
        else:
            raise FileNotFoundError(f"Vector store not found at: {path}")
    
    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """유사도 검색"""
        if self.vector_store:
            return self.vector_store.similarity_search(query, k=k)
        else:
            raise ValueError("Vector store not initialized")