# TODO: actually complete 
from dotenv import load_dotenv
import os

import itertools

from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader, UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate, LLMChain, OpenAI
from langchain.vectorstores import Chroma
from chromadb.config import Settings

# API key stuff
load_dotenv()
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# create LLM and embeddings
openAI_llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)
openAI_embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

subdir_name = "OpenAI" # TODO: don't hardcode to openai embeddings
embeddings = openAI_embeddings
embeddings_fp = os.path.join(".chromadb", subdir_name)
client_settings = Settings(chroma_db_impl="duckdb+parquet",
                        persist_directory=embeddings_fp)

import praw

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent="extractor by u/silversur4_",
)


def get_top_n_reddit(n=10, subreddit="wheelchairs"):
    submissions = reddit.subreddit(subreddit).hot(limit=n)
    return [{"submission":subm.title, "url":subm.url} for subm in submissions]



# sub = Reddit Submission
def get_doc_content(sub):
    header = f"THREAD: {sub.title}\ndescription: {sub.selftext}\nurl: {sub.url}"
    comments = "\n".join([f"{c.author} says: {c.body}" for c in sub.comments])
    return f"{header}\n\nCommunity responses (most to least upvoted):\n{comments}"

# list of relevant subreddits
def get_documents(subreddits):
    doc_list_list = []
    for (subred, n) in subreddits:
        submissions = reddit.subreddit(subred).hot(limit=n)
        docs = [get_doc_content(sub) for sub in submissions]
        doc_list_list.append(docs)

    return list(itertools.chain.from_iterable(doc_list_list))

# extra training for model
if not os.path.exists(embeddings_fp):
    # TODO: stop this from happening every time
    print("recreating vectorstore")
    subreddits = [("wheelchair", 100), ("wheelchairs", 50), ("wheelchai", 30)]
    all_docs = get_documents(subreddits)

    # load docs from reddit top comments
    page_contents = all_docs

    splitter = RecursiveCharacterTextSplitter()
    split_docs = splitter.create_documents(texts=page_contents)

    docsearch = Chroma.from_documents(split_docs, embeddings, client_settings=client_settings)

# same as docsearch just showing that we can have persistent docs
vectordb = Chroma(client_settings=client_settings, embedding_function=embeddings)

# prompt
prompt_footer = """
    Context: {context}
    User Request: {question}
    Response:"""

general_prompt_template = f"""
You have access to information about Reddit threads about wheelchairs.
Use the context below to answer the user request. Do not respond with any NSFW or inappropriate content.

{prompt_footer}"""

# create model instance
GENERAL_PROMPT = PromptTemplate(template=general_prompt_template, input_variables=["context", "question"])
general_chain_type_kwargs = {"prompt": GENERAL_PROMPT}
general_qa = RetrievalQA.from_chain_type(llm=openAI_llm, chain_type="stuff", retriever=vectordb.as_retriever(), chain_type_kwargs=general_chain_type_kwargs, return_source_documents=True)

# function easily called
def run_generic_query(user_question):
    return general_qa({"query":f"{user_question}"})



