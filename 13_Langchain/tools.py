# tools.py - tool 들을 제공하는 module

# TavilySearch로 검색한 결과를 Document에 담아서 반환하는 tool을 생성.
from langchain_community.tools import TavilySearchResults
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_community.document_loaders import WikipediaLoader
from langchain_core.runnables import RunnableLambda 
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


from pydantic import BaseModel, Field
from textwrap import dedent


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



# Runnable로 만들 함수
def wikipedia_search(input_data:dict) -> list[Document]:
    """
    사용자 query(검색 키워드)를 위키백과사전(wikipedia)에서 검색한 결과 k개를 Document로 반환
    parameter:
        input_data: dict dict[str:query, int:검색개수-max_results]
    return:
        list[Document] - 개별 검색결과: Document
    """
    query = input_data['query']
    k = input_data.get('max_results', 2)
    # Document Loader 생성
    wiki_loader = WikipediaLoader(query=query, load_max_docs=k, lang='ko')
    # 문서 로드.
    wiki_docs = wiki_loader.load() # list[Document]
    return wiki_docs

wiki_runnable = RunnableLambda(wikipedia_search)
#### runnable을 tool로 정의
# tool 관련 schema를 정의 한 뒤에서 runnable.as_tool() 메소드를 이용해 생성.
## parameter schema는 pydantic으로 정의
## description 등은 as_tool() 에 직접 정의
class WikiSearchSchema(BaseModel):
    # ... 시작: required(필수), description: parameter 설명명
    query:str = Field(..., description="Wikipedia에서 검색할 keyword") 
    # ... 으로 시작하지 않으면 optional, default: 값이 없을 경우 사용할 기본값.
    max_results:int = Field(default=2, description="검색할 문서 개수")

# Runnable -> tool 
search_wiki = wiki_runnable.as_tool(
    args_schema=WikiSearchSchema, # 필수
    name="search_wiki", #생략-함수명이 이름이 됨.
    description=dedent("""
        이 도구는 위키피디아(wikipedia)에서 정보를 검색해야 할 때 사용합니다.
        사용자의 질문과 관련된 위키피디아 문서를 지정된 개수 만큼 검색해서 반환합니다.
        일반적인 지식이나 배경 정보가 필요한 경우 사용할 수있는 도구 입니다.
        """) # 생략: 함수의 docstring이 description이됨.
)

#################################
# 식당 메뉴 조회 tool
#################################
COLLECTION_NAME = "restaurant_menu_2"
PERSIST_DIRECTORY = "vector_store/restaurant_menu_db"
# 연결
embedding_model = OpenAIEmbeddings(model='text-embedding-3-small')
v_store = Chroma(
    embedding_function=embedding_model,
    collection_name=COLLECTION_NAME,
    persist_directory=PERSIST_DIRECTORY
)
retriver = v_store.as_retriever()

@tool
def search_menu(query:str) -> list[Document]:
    """
    Vector Store에 저장된 restaurant의 메뉴를 검색한다. 
    이 도구는 restaurant의 메뉴 관련 질문에 대해 실행한다.
    """
    result = retriver.invoke(query)
    if len(result): #검색결과가 있다면
        return result
    else:
        return [Document(page_content="검색 결과가 없습니다.")]