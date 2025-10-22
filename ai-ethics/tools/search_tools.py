from tavily import TavilyClient
from typing import List, Dict
from config.settings import TAVILY_API_KEY

class SearchTools:
    """웹 검색 도구"""
    
    def __init__(self):
        self.client = TavilyClient(api_key=TAVILY_API_KEY)
    
    def search_service_info(
        self, 
        service_name: str, 
        query_type: str = "overview"
    ) -> List[Dict]:
        """AI 서비스 정보 검색"""
        
        query_templates = {
            "overview": f"{service_name} AI service overview features capabilities",
            "fairness": f"{service_name} AI bias fairness testing discrimination issues",
            "privacy": f"{service_name} data privacy policy personal information GDPR compliance",
            "transparency": f"{service_name} AI transparency explainability how it works documentation",
            "accountability": f"{service_name} AI accountability governance responsibility oversight",
            "safety": f"{service_name} AI safety security risks vulnerabilities incidents"
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
                    "score": result.get('score', 0),
                    "source": "web"
                })
            
            return formatted_results
        
        except Exception as e:
            print(f"  ⚠️  검색 오류: {e}")
            return []
    
    def search_ethics_guidelines(
        self, 
        guideline_name: str, 
        topic: str
    ) -> List[Dict]:
        """윤리 가이드라인 관련 정보 검색"""
        
        query = f"{guideline_name} AI {topic} requirements guidelines standards"
        
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
            print(f"  ⚠️  가이드라인 검색 오류: {e}")
            return []

