# tools.py - tool 들을 제공하는 module

# TavilySearch로 검색한 결과를 Document에 담아서 반환하는 tool을 생성.
from langchain_community.tools import TavilySearchResults
from langchain_core.documents import Document
from langchain_core.tools import tool

@tool
def search_web(query:str, max_results:int=2) -> list[Document]|str:
    """
    가지고 있지 않은 정보나 최신 정보를 찾기 위해 인터넷 검색을 하는 툴입니다.
    검색할 내용은 query 로 입력 받습니다.
    검색 개수는 max_results로 받습니다. 입력되지 않은 경우에는 2개를 검색합니다.
    검색 결과는 Document 객체에 담아 list로 묶어서 반환합니다.
    """
    tavily_search = TavilySearchResults(max_results=max_results)
    docs = tavily_search.invoke(query) # list[dict]
    # print(docs)
    # list[dict] => list[Document(page_content:검색결과, metadata={url:검색 url})]
    document_list = []
    for doc in docs:
        _doc = Document(
            page_content=doc['content'],
            metadata={"url":doc['url'], "question":query}
        )
        document_list.append(_doc)
    if document_list: # True: 원소 한개 이상 있는 경우.
        return document_list
    else: #False: 검색결과가 없는 경우.
        return "관련된 정보를 검색할 수 없습니다."

