from langchain_community.llms import CTransformers
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# model
model = "../models/vinallama-7b-chat_q5_0.gguf"

# Load LLM
def Load_LLMs(model):
    llm = CTransformers(model = model, model_type = 'llama', max_new_tokens = 1024, temperature = 0.01)
    return llm

def Create_prompt(template):
    prompt = PromptTemplate(template = template, input_variables = ["question"])
    return prompt

# Create Chain
def Create_chain(prompt, llm):
    llm_chain = LLMChain(prompt = prompt, llm = llm)
    return llm_chain

def Create_Templates():
    temp = """ <|im_start|>system
        Bạn là một trợ lí AI hữu ích. Hãy trả lời người dùng một cách chính xác.
        <|im_end|>
        <|im_start|>user
        {question}<|im_end|>
        <|im_start|>assistant
        """ 
    return temp

prompt = Create_prompt(Create_Templates())
llm = Load_LLMs(model=model)
llm_chain = Create_chain(prompt=prompt,llm=llm)

# test
question = "Vì sao có thể tính nhanh bình phương của một số hai chữ số có chữ số cuối là 5?"
response = llm_chain.invoke({"question":question})
print('Response: ', response)