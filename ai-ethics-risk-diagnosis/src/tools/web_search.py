"""
웹 검색 도구
"""
from typing import List, Dict
from tavily import TavilyClient
from src.config import TAVILY_API_KEY


class WebSearchTool:
    """웹 검색 도구 클래스"""
    
    def __init__(self):
        self.client = TavilyClient(api_key=TAVILY_API_KEY)
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        웹 검색 수행
        
        Args:
            query: 검색 쿼리
            max_results: 최대 결과 수
        
        Returns:
            검색 결과 리스트
        """
        try:
            response = self.client.search(
                query=query,
                max_results=max_results,
                search_depth="advanced"
            )
            
            results = []
            for result in response.get('results', []):
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "score": result.get("score", 0)
                })
            
            print(f"🔍 Search completed: {len(results)} results for '{query}'")
            return results
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
    
    def search_service_info(self, service_name: str) -> List[Dict]:
        """AI 서비스 정보 검색"""
        query = f"{service_name} AI service features data usage privacy policy"
        return self.search(query, max_results=5)
    
    def search_ethics_info(self, service_name: str, criterion: str) -> List[Dict]:
        """특정 윤리 기준에 대한 정보 검색"""
        query = f"{service_name} AI ethics {criterion} bias privacy concerns"
        return self.search(query, max_results=3)