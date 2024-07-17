import os
import streamlit as st
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.readers.github import GithubRepositoryReader, GithubClient

from traceloop.sdk import Traceloop

Traceloop.init(disable_batch=True)

Settings.llm = OpenAI(model="gpt-4o")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

github_client = GithubClient(github_token=os.environ["GITHUB_TOKEN"])

st.set_page_config(
    page_title="Traceloop Demo",
    page_icon="🔭",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
st.title("Traceloop Demo")
st.info(
    "Do not share any private information here. "
    + "All traces can be viewed by anyone who signs up at https://app.traceloop.com"
)

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question about Traceloop or OpenLLMetry!",
        }
    ]


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing Traceloop and OpenLLMetry docs."):
        reader = GithubRepositoryReader(
            github_client=github_client,
            owner="traceloop",
            repo="docs",
            filter_file_extensions=(
                [".mdx"],
                GithubRepositoryReader.FilterType.INCLUDE,
            ),
            verbose=True,
        )
        docs = reader.load_data(branch="main")
        index = VectorStoreIndex.from_documents(docs)
        return index


index = load_data()

if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="best", verbose=True)

if prompt := st.chat_input(
    "Your question"
):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            Traceloop.set_association_properties(
                {"session_id": id(st.session_state.chat_engine)}
            )
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)  # Add response to message history
