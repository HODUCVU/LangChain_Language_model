from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import GPT4AllEmbeddings

# model
model = "../models/vinallama-7b-chat_q5_0.gguf"
# vector db
vector_db = '../vectorstores/db_faiss'
# Load LLM
def Load_LLMs(model):
    # llm = CTransformers(model = model, model_type = 'llama', max_new_tokens = 1024, temperature = 0.01, context_length=2000)
    llm = CTransformers(model = model, model_type = 'llama', 
                        config={'max_new_tokens': 256,
                        'temperature': 0.01,
                        'context_length' : 2048})
    return llm

def Create_prompt(template):
    prompt = PromptTemplate(template = template, input_variables = ["context","question"])
    return prompt


# Create Chain
def Create_chain(prompt, llm, vector_db):
    llm_chain = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type = "stuff",
        retriever = vector_db.as_retriever(search_kwargs = {"k":3}, max_tokens_limit=1024),
        return_source_documents = False,
        chain_type_kwargs = {'prompt':prompt}
    )
    return llm_chain

def Create_Templates():
    temp = """<|im_start|>system
    Sử dụng thông tin sau đây để trả lời câu hỏi. Nếu bạn không biết câu trả lời, hãy nói không biết, đừng cố tạo ra câu trả lời
    {context}<|im_end|>
    <|im_start|>user
    {question}<|im_end|>
    <|im_start|>assistant"""
    return temp
    """ <|im_start|>system
        Bạn là một trợ lí AI hữu ích. Hãy trả lời người dùng một cách chính xác.
        <|im_end|>
        <|im_start|>user
        {question}<|im_end|>
        <|im_start|>assistant
        """ 
# Read infor from Vector DB
def Read_from_VectorDB():
    # Embedding
    embedding_model = GPT4AllEmbeddings(model_file = model)
    db = FAISS.load_local(vector_db, embedding_model,allow_dangerous_deserialization=True)
    return db

# Test
db = Read_from_VectorDB()
llm = Load_LLMs(model=model)
prompt = Create_prompt(Create_Templates())
llm_chain = Create_chain(prompt=prompt,llm=llm,vector_db=db)
# Q/A
# nextQuestion = True
question = "Làm thế nào để biết một số tự nhiên chia hết cho 2, 3, 4, 5?"
reponse = llm_chain.invoke({"query":question})
print(reponse)
