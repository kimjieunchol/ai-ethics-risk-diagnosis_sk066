from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List, Dict
import json
from pathlib import Path
import os
import tempfile
import shutil


class GuidelineRetriever:
    """AI 윤리 가이드라인 검색 시스템"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir).resolve()
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.vectorstore = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
    
    def load_guidelines(self) -> List[Document]:
        """JSON 파일에서 가이드라인 로드"""
        documents = []
        
        json_files = [
            "eu_ai_act.json",
            "unesco_ethics.json",
            "oecd_principles.json"
        ]
        
        for filename in json_files:
            filepath = self.data_dir / filename
            if not filepath.exists():
                print(f"경고: {filename} 파일을 찾을 수 없습니다")
                continue
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            source = data.get('source', filename)
            url = data.get('url', '')
            
            # 각 섹션을 Document로 변환
            for section in data.get('sections', []):
                content = f"출처: {source}\n"
                content += f"섹션: {section['title']}\n\n"
                content += section['content']
                
                doc = Document(
                    page_content=content,
                    metadata={
                        'source': source,
                        'url': url,
                        'section': section['title']
                    }
                )
                documents.append(doc)
            
            # 추가 정보가 있으면 포함
            if 'additional_info' in data:
                for i, info in enumerate(data['additional_info']):
                    doc = Document(
                        page_content=f"출처: {source}\n추가 정보 {i+1}:\n{info}",
                        metadata={
                            'source': source,
                            'url': url,
                            'section': f'추가 정보 {i+1}'
                        }
                    )
                    documents.append(doc)
        
        print(f"가이드라인에서 {len(documents)}개 문서 로드 완료")
        return documents
    
    def build_vectorstore(self):
        """벡터 스토어 구축"""
        documents = self.load_guidelines()
        
        if not documents:
            raise ValueError("문서를 로드할 수 없습니다. 먼저 크롤러를 실행하세요.")
        
        # 문서 분할
        split_docs = self.text_splitter.split_documents(documents)
        print(f"{len(split_docs)}개 청크로 분할 완료")
        
        # FAISS 벡터 스토어 생성
        self.vectorstore = FAISS.from_documents(
            split_docs,
            self.embeddings
        )
        
        print("✓ 벡터 스토어 구축 완료")
    
    def save_vectorstore(self, path: str = "data/vectorstore"):
        """벡터 스토어 저장 (한글 경로 문제 해결)"""
        if self.vectorstore is None:
            raise ValueError("벡터 스토어가 아직 구축되지 않았습니다")
        
        # 최종 저장 경로
        final_path = Path(path).resolve()
        final_path.mkdir(parents=True, exist_ok=True)
        
        # 임시 디렉토리 생성 (영문 경로)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir) / "vectorstore"
            temp_path.mkdir(parents=True, exist_ok=True)
            
            print(f"임시 경로에 저장 중: {temp_path}")
            
            try:
                # 임시 디렉토리에 저장
                self.vectorstore.save_local(str(temp_path))
                
                # 최종 경로로 복사
                print(f"최종 경로로 복사 중: {final_path}")
                
                # 기존 파일이 있으면 삭제
                for file in final_path.glob("*"):
                    if file.is_file():
                        file.unlink()
                
                # 임시 디렉토리의 파일들을 최종 경로로 복사
                for file in temp_path.glob("*"):
                    if file.is_file():
                        shutil.copy2(file, final_path / file.name)
                
                print(f"✓ 벡터 스토어 저장 완료: {final_path}")
                
            except Exception as e:
                print(f"저장 중 오류 발생: {e}")
                raise
    
    def load_vectorstore(self, path: str = "data/vectorstore"):
        """벡터 스토어 로드"""
        vectorstore_path = Path(path).resolve()
        
        # index.faiss 파일이 있는지 확인
        index_file = vectorstore_path / "index.faiss"
        
        if index_file.exists():
            try:
                print(f"벡터 스토어 로드 시도: {vectorstore_path}")
                
                # 한글 경로 문제 해결: 임시 디렉토리에 복사 후 로드
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir) / "vectorstore"
                    temp_path.mkdir(parents=True, exist_ok=True)
                    
                    # 파일 복사
                    for file in vectorstore_path.glob("*"):
                        if file.is_file():
                            shutil.copy2(file, temp_path / file.name)
                    
                    # 임시 경로에서 로드
                    self.vectorstore = FAISS.load_local(
                        str(temp_path),
                        self.embeddings,
                        allow_dangerous_deserialization=True
                    )
                
                print(f"✓ 벡터 스토어 로드 완료: {vectorstore_path}")
                
            except Exception as e:
                print(f"벡터 스토어 로드 실패: {e}")
                print("새로 구축합니다...")
                self.build_vectorstore()
                self.save_vectorstore(str(vectorstore_path))
        else:
            print(f"벡터 스토어를 {vectorstore_path}에서 찾을 수 없습니다.")
            print("새로 구축합니다...")
            self.build_vectorstore()
            self.save_vectorstore(str(vectorstore_path))
    
    def retrieve(self, query: str, k: int = 5) -> List[Dict]:
        """관련 가이드라인 검색"""
        if self.vectorstore is None:
            raise ValueError("벡터 스토어가 초기화되지 않았습니다")
        
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        
        retrieved = []
        for doc, score in results:
            retrieved.append({
                'content': doc.page_content,
                'source': doc.metadata.get('source', '출처 불명'),
                'section': doc.metadata.get('section', '섹션 불명'),
                'url': doc.metadata.get('url', ''),
                'score': float(score)
            })
        
        return retrieved
    
    def retrieve_by_category(self, category: str, k: int = 3) -> List[Dict]:
        """카테고리별 가이드라인 검색"""
        queries = {
            'bias': '편향 차별 공정성 평등 AI 시스템',
            'privacy': '개인정보 데이터 보호 프라이버시 GDPR',
            'transparency': '투명성 설명가능성 해석가능성 공개',
            'fairness': '공정성 정의 형평성 차별금지 평등',
            'safety': '안전성 보안 견고성 신뢰성 리스크 관리',
            'accountability': '책임성 거버넌스 감독'
        }
        
        query = queries.get(category.lower(), category)
        return self.retrieve(query, k=k)


if __name__ == "__main__":
    retriever = GuidelineRetriever()
    retriever.build_vectorstore()
    retriever.save_vectorstore()
    
    # 테스트 검색
    results = retriever.retrieve("AI의 편향성과 차별")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['source']} - {result['section']}")
        print(f"점수: {result['score']:.3f}")
        print(result['content'][:200] + "...")