import pinecone
import streamlit as st

def get_pinecone_index():
    index_name = 'openai-price-embedding'

# initialize connection to pinecone (get API key at app.pinecone.io)
    pinecone.init(
        api_key=st.secrets.PINECONE_API,
        environment="gcp-starter"  # find next to api key in console
    )
    # # check if 'openai' index already exists (only create index if not)
    # if index_name not in pinecone.list_indexes():
    #     pinecone.create_index(index_name, dimension=len(embedding_data.embedding[0]))
    # connect to index
    index = pinecone.Index(index_name)
    return index

def get_pinecone_index2():
    index_name = 'statements'

# initialize connection to pinecone (get API key at app.pinecone.io)
    pinecone.init(
        api_key=st.secrets.PINECONE_API2,
        environment="gcp-starter"  # find next to api key in console
    )
    # # check if 'openai' index already exists (only create index if not)
    # if index_name not in pinecone.list_indexes():
    #     pinecone.create_index(index_name, dimension=len(embedding_data.embedding[0]))
    # connect to index
    index = pinecone.Index(index_name)
    return index