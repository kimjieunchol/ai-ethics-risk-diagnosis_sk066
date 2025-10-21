"""
PDF 문서 로딩 유틸리티
"""
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


def load_pdf_documents(pdf_paths: List[str], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    PDF 문서들을 로드하고 청크로 분할
    
    Args:
        pdf_paths: PDF 파일 경로 리스트
        chunk_size: 청크 크기
        chunk_overlap: 청크 오버랩
    
    Returns:
        Document 객체 리스트
    """
    all_documents = []
    
    for pdf_path in pdf_paths:
        try:
            # PDF 로드
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            
            # 메타데이터 추가
            for doc in documents:
                doc.metadata["source_file"] = pdf_path.split("/")[-1]
            
            all_documents.extend(documents)
            print(f"✅ Loaded: {pdf_path} ({len(documents)} pages)")
            
        except Exception as e:
            print(f"❌ Error loading {pdf_path}: {e}")
    
    # 텍스트 분할
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = text_splitter.split_documents(all_documents)
    print(f"📄 Total chunks created: {len(chunks)}")
    
    return chunks