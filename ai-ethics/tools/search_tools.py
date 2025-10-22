from tavily import TavilyClient
from typing import List, Dict
from config.settings import TAVILY_API_KEY

class SearchTools:
    def __init__(self):
        self.client = TavilyClient(api_key=TAVILY_API_KEY)
    
    def search_service_info(self, service_name: str, query_type: str = "overview") -> List[Dict]:
        """
        AI 서비스 정보 검색
        
        Args:
            service_name: AI 서비스 이름
            query_type: 검색 유형 (overview, features, ethics, privacy 등)
        """
        query_templates = {
            "overview": f"{service_name} AI service overview features capabilities",
            "ethics": f"{service_name} AI ethics concerns risks bias privacy",
            "privacy": f"{service_name} data privacy policy personal information",
            "transparency": f"{service_name} AI transparency explainability how it works"
        }
        
        query = query_templates.get(query_type, f"{service_name} {query_type}")
        
        try:
            results = self.client.search(
                query=query,
                max_results=5,
                search_depth="advanced"
            )
            
            formatted_results = []
            for result in results.get('results', []):
                formatted_results.append({
                    "title": result.get('title', ''),
                    "url": result.get('url', ''),
                    "content": result.get('content', ''),
                    "source": "web"
                })
            
            return formatted_results
        
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def search_ethics_guidelines(self, guideline_name: str, topic: str) -> List[Dict]:
        """
        윤리 가이드라인 관련 정보 검색
        
        Args:
            guideline_name: 가이드라인 이름 (EU AI Act, UNESCO, OECD)
            topic: 검색 주제 (bias, privacy, transparency 등)
        """
        query = f"{guideline_name} AI {topic} requirements guidelines"
        
        try:
            results = self.client.search(
                query=query,
                max_results=3,
                search_depth="advanced"
            )
            
            formatted_results = []
            for result in results.get('results', []):
                formatted_results.append({
                    "title": result.get('title', ''),
                    "url": result.get('url', ''),
                    "content": result.get('content', ''),
                    "guideline": guideline_name,
                    "source": "web"
                })
            
            return formatted_results
        
        except Exception as e:
            print(f"Guideline search error: {e}")
            return []