
# import os
# from dotenv import load_dotenv
# from langchain_openai import OpenAIEmbeddings


# # Load the .env file
# load_dotenv()
# embedding_model = OpenAIEmbeddings(model="text-embedding-3-small",api_key=os.getenv("OPENAI_API_KEY"))

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

# Load the .env file
load_dotenv()

embedding_model = OpenAIEmbeddings(
    model=os.getenv("EMBED_MODEL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)
