# 05_streamlit_chat_exam_memory.py
# control + shift + p : 명령 팔레트 -> Python: select interpreter -> 가상환경 선택
import streamlit as st
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser

from uuid import uuid4 # 중복되지 않은 값을 생성해주는 모듈. session_id 만들때 사용.
# print(str(uuid4()))
from dotenv import load_dotenv
load_dotenv() # 환경변수 저장한 파일의 경로를 지정해서 호출해도 됨.

st.set_page_config(page_title="Chatbot memory 예제", page_icon=":robot_face:")#, layout="wide")
st.title("Chatbot 메모리 예제")

#####################################
# InMemoryChatMessageHistory 생성
#####################################
store = {}

def get_session_history(session_id:str) -> InMemoryChatMessageHistory:
    if session_id not in store: #store dict에 key로 session_id가 없으면 생성해서 넣는다.
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

############################################################
# Runnable Chain -> PromptTemplate -> Model -> OutputParser
############################################################
@st.cache_resource
def get_resource():
    prompt_template = ChatPromptTemplate(
        [
            ("system", "답변은 100단어 이하로 작성해주세요. 정확하지 않은 경우 모른다고 대답해주세요."),
            MessagesPlaceholder("history"),
            ("human", "{query}")
        ]
    )
    model = ChatOpenAI(model="gpt-4o-mini", streaming=True)
    return prompt_template | model | StrOutputParser()

runnable = get_resource()

###############################
# RunnableWithMessageHistory
###############################
@st.cache_resource
def get_chain():
    return RunnableWithMessageHistory(
        runnable=runnable,
        get_session_history=get_session_history,
        input_messages_key="query",
        history_messages_key="history"
    )
chain = get_chain()

######################################################
# st.session_state에 대화 내용들을 저장할 state를 생성
######################################################
if "message_list" not in  st.session_state:
    st.session_state["message_list"] = [] # list[dict[str:role, str:msg]]
if "session_id" not in st.session_state:
    st.session_state['session_id'] = None

###################################
# 기존 대화내용 chat_message에 출력
###################################
for message in st.session_state['message_list']:
    with st.chat_message(message['role']):
        st.write(message['message'])

####################################
# sidebar 에 session_id 입력 폼
####################################
session_id = st.sidebar.text_input("Session ID", placeholder="대화 ID를 입력하세요.")

prompt = st.chat_input("사용자:")
if prompt: 
    # 사용자 입력 prompt를 message_list에 추가.
    st.session_state["message_list"].append({"role":"user", "message":prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # session_id가 입력되지 않았을 때 처리(생성).
    if session_id is None:
        session_id = str(uuid4())
    # session_state에 session id를 저장.
    if st.session_state['session_id'] is None:
        st.session_state["session_id"] = session_id
    
    ## chain을 이용해서 LLM 에게 요청
    with st.chat_message("ai"):
        full_message = "" # model이 token단위로 응답(streaming=True)하면 그것을 누적할 변수
        message_placeholder = st.empty() # chat message 컨테이너에 empty() 컨테이너 추가.
        print("session id:", st.session_state["session_id"])

        config = {"configurable": {"session_id":st.session_state["session_id"]}}
        for token in chain.stream({"query":prompt}, config=config):
            full_message += token 
            message_placeholder.write(full_message)

        # 응답이 완료되면 응답을  session state의 message list에 추가.
        st.session_state['message_list'].append({"role":"ai", "message":full_message})