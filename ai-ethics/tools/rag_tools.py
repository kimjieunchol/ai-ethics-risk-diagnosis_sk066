from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict
import os
from config.settings import (
    GUIDELINES_PATH, 
    CHUNK_SIZE, 
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
    TOP_K_RESULTS,
    OPENAI_API_KEY
)

class RAGTools:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            openai_api_key=OPENAI_API_KEY
        )
        self.vectorstore = None
        self.guideline_docs = {}
    
    def load_guidelines(self, guideline_names: List[str]) -> bool:
        """
        윤리 가이드라인 PDF 문서 로드 및 벡터 스토어 생성
        """
        all_documents = []
        
        # PDF 파일명 매핑
        filename_map = {
            "EU AI Act": "eu_ai_act.pdf",
            "UNESCO": "unesco_ethics.pdf",
            "OECD": "oecd_principles.pdf"
        }
        
        for guideline in guideline_names:
            filename = filename_map.get(guideline)
            if not filename:
                print(f"Unknown guideline: {guideline}")
                continue
            
            filepath = os.path.join(GUIDELINES_PATH, filename)
            
            if not os.path.exists(filepath):
                print(f"⚠️  파일 없음: {filepath} - 웹 검색으로 대체됩니다")
                continue  # 파일이 없어도 계속 진행
            
            try:
                # PDF 로드
                loader = PyPDFLoader(filepath)
                documents = loader.load()
                
                # 메타데이터에 가이드라인 이름 추가
                for doc in documents:
                    doc.metadata['guideline'] = guideline
                
                all_documents.extend(documents)
                self.guideline_docs[guideline] = len(documents)
                print(f"✅ Loaded {len(documents)} pages from {guideline}")
            
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
        
        if not all_documents:
            print("⚠️  PDF 문서 없음 - 웹 검색만 사용합니다")
            return True  # False 대신 True 반환
        
        # 텍스트 분할
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len
        )
        
        splits = text_splitter.split_documents(all_documents)
        print(f"Created {len(splits)} chunks from all guidelines")
        
        # FAISS 벡터 스토어 생성
        self.vectorstore = FAISS.from_documents(splits, self.embeddings)
        print("Vector store created successfully!")
        
        return True
    
    def search_guidelines(self, query: str, guideline_filter: str = None) -> List[Dict]:
        """
        벡터 스토어에서 관련 내용 검색
        
        Args:
            query: 검색 쿼리
            guideline_filter: 특정 가이드라인으로 필터링 (선택사항)
        """
        if not self.vectorstore:
            print("Vector store not initialized!")
            return []
        
        try:
            # 검색 수행
            docs = self.vectorstore.similarity_search(
                query,
                k=TOP_K_RESULTS
            )
            
            results = []
            for doc in docs:
                # 가이드라인 필터 적용
                if guideline_filter and doc.metadata.get('guideline') != guideline_filter:
                    continue
                
                results.append({
                    "content": doc.page_content,
                    "guideline": doc.metadata.get('guideline', 'Unknown'),
                    "page": doc.metadata.get('page', 'N/A'),
                    "source": "rag"
                })
            
            return results
        
        except Exception as e:
            print(f"RAG search error: {e}")
            return []
    
    def get_guideline_context(self, dimension: str, guidelines: List[str]) -> str:
        """
        특정 윤리 차원에 대한 가이드라인 컨텍스트 가져오기
        """
        dimension_queries = {
            "bias": "bias fairness discrimination equality",
            "privacy": "privacy data protection personal information",
            "transparency": "transparency explainability interpretability",
            "accountability": "accountability responsibility governance oversight"
        }
        
        query = dimension_queries.get(dimension, dimension)
        
        # PDF가 없으면 웹 검색 사용
        if not self.vectorstore:
            print(f"  ⚠️  RAG 사용 불가 - 웹 검색으로 대체")
            from tools.search_tools import SearchTools
            search_tools = SearchTools()
            
            all_context = []
            for guideline in guidelines:
                results = search_tools.search_ethics_guidelines(guideline, dimension)
                for result in results[:1]:  # 가이드라인당 상위 1개
                    all_context.append(
                        f"[{guideline}] {result['content'][:500]}"
                    )
            
            return "\n\n".join(all_context) if all_context else f"{dimension}에 대한 일반적인 윤리 기준을 적용합니다."
        
        # 기존 RAG 로직
        all_context = []
        for guideline in guidelines:
            results = self.search_guidelines(query, guideline_filter=guideline)
            for result in results[:2]:
                all_context.append(
                    f"[{result['guideline']}] {result['content']}"
                )
        
        return "\n\n".join(all_context)