"""
RAG 검색 도구
"""
from typing import List, Dict
from langchain.schema import Document
from src.utils.vector_store import VectorStoreManager


class RAGRetriever:
    """RAG 기반 문서 검색 도구"""
    
    def __init__(self, vector_store_manager: VectorStoreManager):
        self.vsm = vector_store_manager
    
    def retrieve_guidelines(self, query: str, k: int = 5) -> List[Dict]:
        """
        윤리 가이드라인 검색
        
        Args:
            query: 검색 쿼리
            k: 반환할 문서 수
        
        Returns:
            검색된 문서 정보 리스트
        """
        try:
            documents = self.vsm.similarity_search(query, k=k)
            
            results = []
            for doc in documents:
                results.append({
                    "content": doc.page_content,
                    "source": doc.metadata.get("source_file", "Unknown"),
                    "page": doc.metadata.get("page", "N/A")
                })
            
            print(f"📚 Retrieved {len(results)} guideline documents")
            return results
            
        except Exception as e:
            print(f"❌ Retrieval error: {e}")
            return []
    
    def retrieve_for_criterion(self, criterion: str, service_context: str = "") -> List[Dict]:
        """
        특정 윤리 기준에 대한 가이드라인 검색
        
        Args:
            criterion: 윤리 기준 (bias, privacy, transparency 등)
            service_context: 서비스 컨텍스트 (선택)
        
        Returns:
            관련 가이드라인 문서
        """
        # 기준별 검색 쿼리 구성
        criterion_queries = {
            "bias": "fairness non-discrimination bias algorithmic fairness",
            "privacy": "data protection personal information privacy GDPR",
            "transparency": "explainability interpretability transparency disclosure",
            "accountability": "responsibility accountability liability governance",
            "safety": "safety security robustness risk assessment harm prevention"
        }
        
        base_query = criterion_queries.get(criterion, criterion)
        query = f"{base_query} {service_context}".strip()
        
        return self.retrieve_guidelines(query, k=4)