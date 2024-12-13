from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
from dotenv import load_dotenv
from textwrap import dedent

import config

load_dotenv()
###############################################################################
# Vector Store 생성
###############################################################################
COLLECTION_NAME = config.collection_name 
PERSIST_DIRECTORY = config.persist_directory

EMBEDDING_NAME = config.embedding_name
MODEL_NAME = config.model_name


@st.cache_resource
def get_retriever():

    embedding_model = OpenAIEmbeddings(
        model=EMBEDDING_NAME
    )

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_model
    )
    return vector_store.as_retriever(
        search_type="mmr", 
        search_kwargs={"k": 5, "fetch_k": 10}
    )

retriever = get_retriever()

############################################################
# Chain 생성
############################################################
def remove_same_novel_retriever(input):
    """
    Retriever를 이용해 질문과 관련 문서들을 조회한 뒤 중복되는 소설은 제거한다. 
    metadata의 full_text에 소설 전체 내용이 있기 때문에 같은 소설의 문서 조각(chunk)는 하나만 있으면 된다.
    parameter:
        input: str - 질문
    return: 
        str - Document.metadata의 full_text를 모아서 반환한다.
        ```반환 문자열 형식
            제목
            내용

            -------------
        ```
    """
    docs = retriever.invoke(input) # list[Document-k:5]
    doc_list = []

    for retrieve_doc in docs:
        # 중복 여부를 확인하는 플래그
        is_duplicate = False
        ## 제목 중복 여부 확인
        for save_doc in doc_list:
            if save_doc.metadata['title'] == retrieve_doc.metadata['title']:
                is_duplicate = True
                break
        
        # 중복이 아닌 경우에만 리스트에 추가
        if not is_duplicate:
            doc_list.append(retrieve_doc)
            
    context = ""
    for doc in doc_list:
        context += doc.metadata['full_text']+('\n\n'+"-"*30+"\n")
    
    return context



@st.cache_resource
def get_resource():
    # Chain생성
    human_message = dedent("""
        You are an assistant for question-answering tasks.
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. Use five sentences maximum and keep the answer concise.

        Question: {question} 
        Context: {context} 
        Answer:
        """)
    prompt_template = ChatPromptTemplate(
        [
            ("human", human_message)
        ]
    )
    
    model = ChatOpenAI(model=MODEL_NAME, streaming=True)

    chain = ({"context":RunnableLambda(remove_same_novel_retriever), "question":RunnablePassthrough()} 
             | prompt_template 
             | model 
             | StrOutputParser())
    
    return chain

chain = get_resource()



######################################################
# title, sidebar
# sidebar에 소설 제목 출력
######################################################
st.title("한국 근대소설")

with st.sidebar:
    st.write("""
    ## 소설 제목
  다음 소설들에 대해 궁금한 것을 질문하세요.
   - **금따는 콩밭** - 김유정
   - **동백꽃** - 김유정
   - **봄봄** - 김유정
   - **메밀꽃 필 무렵** - 이효석
   - **배따라기** - 김동인
   - **백치아다다** - 계용묵
   - **벙어리 삼룡이** - 나도향
   - **소나기** - 황순원
   - **술 권하는 사회** - 현진건
   - **운수 좋은 날** - 현진건
""")


######################################################
# 대화 내용들을 저장할 session state를 생성
######################################################
if "message_list" not in  st.session_state:
    st.session_state["message_list"] = [] # list[dict[str:role, str:msg]]
    
###################################
# 기존 대화내용 chat_message에 출력
###################################
for message in st.session_state['message_list']:
    with st.chat_message(message['role']):
        st.write(message['message'])

######################################
# 질의 처리
######################################
prompt = st.chat_input("사용자:")
if prompt: 
    # 사용자 입력 prompt를 session_state에 추가하고 chat_message에 출력
    st.session_state["message_list"].append({"role":"user", "message":prompt})
    with st.chat_message("user"):
        st.write(prompt)

    ## chain 호출
    with st.chat_message("ai"):
        full_message = ""
        message_placeholder = st.empty()

        for token in chain.stream(prompt):
            full_message += token 
            message_placeholder.write(full_message)

        st.session_state['message_list'].append({"role":"ai", "message":full_message})
    