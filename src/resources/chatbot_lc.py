import os

from dotenv import load_dotenv
from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationEntityMemory
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE

load_dotenv()


def llm_ai_chatbot(human_input, input_memory):
    llm = OpenAI(
        model="text-davinci-003",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        max_tokens=256,
    )

    template = """Você é um chatbot conversando com um humano sobre seguros e créditos. Por favor, responda em Português BR e use no máximo 2 linhas.

    context: {entities}

    current conversation: {chat_history}

    Humano: {human_input}
    Chatbot:"""

    prompt = PromptTemplate(
        input_variables=["entities", "chat_history", "human_input"], template=template
    )

    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input"], template=template
    )

    memory = ConversationEntityMemory(llm=llm)
    _input = {"input": f"{input_memory}"}
    memory.load_memory_variables(_input)

    conversation = ConversationChain(
        llm=llm,
        verbose=True,
        prompt=prompt,
        memory=ConversationEntityMemory(llm=llm),
    )

    return conversation.predict(input=human_input)
