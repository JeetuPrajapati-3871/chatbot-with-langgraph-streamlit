from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint,HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv
load_dotenv()

embedd_model=HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
llm=HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    max_new_tokens=120
)
llm=ChatHuggingFace(llm=llm)


loader=PyPDFLoader('C:\\Users\\jeetu\\OneDrive\\Desktop\\Customer Support\\Flipkart_Policies_Detailed_Guide.pdf')

documents=loader.load()
text_splitter=CharacterTextSplitter(chunk_size=50,chunk_overlap=15)
docs=text_splitter.split_documents(documents)

vectorstore=FAISS.from_documents(docs,embedd_model)
retriever=vectorstore.as_retriever(search_type="similarity",search_kwargs={"k":3})

template = """
You are an assistant answering questions using provided context.
If the answer is not in the context, say "Information not available in Flipkart policy."

Context:
{context}

Question: {question}

Answer:
"""
prompt = PromptTemplate(template=template, input_variables=["context", "question"])

# 8️⃣ Build RetrievalQA chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",     # simplest form
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt}
)

# 9️⃣ Ask a question
# query = "What is the return policy for electronic items on Flipkart?"
# answer=qa.invoke({"query":query})
# print(answer['result'])



