from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from openai import OpenAI

import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()
openai_api = os.getenv('OPENAI_API_KEY')
openai_org = os.getenv('OPENAI_API_ORG')
pinecone_api = os.getenv('PINECONE_API_KEY')

# Initialize OpenAI
client = OpenAI(api_key=openai_api, organization=openai_org)

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api)

namespace = "all_course_texts"
embeddings = OpenAIEmbeddings()

index_name = "langchain-index"
index = pc.Index(index_name)
existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

def documents_already_indexed(index, namespace):
    stats = index.describe_index_stats()
    return stats['namespaces'].get(namespace, {}).get('vector_count', 0) > 0

# Setup Pinecone Vector Store
if documents_already_indexed(index, namespace):
    docsearch = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings,
        namespace=namespace
    )
    print("Documents are already indexed.")
else:
    print("Invalid index")

# Setup LangChain
llm = ChatOpenAI(
    openai_api_key=openai_api,
    model_name="gpt-4o",
    temperature=0.0
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever()
)

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    query_text = data.get('query')
    
    if not query_text:
        return jsonify({"error": "Query text is required"}), 400

    result_with_knowledge = qa.invoke(query_text)
    
    response = {
        "result_with_knowledge": result_with_knowledge['result'],
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
