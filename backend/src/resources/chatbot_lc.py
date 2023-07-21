import os

from dotenv import load_dotenv
from langchain import OpenAI, PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationEntityMemory

load_dotenv()


def extract_context(memory, context):
    """Extracts conversation context from the provided list and updates the memory.

    This function extracts the conversation context from the given list and
    updates the provided memory object with the user messages as input and bot
    responses as output. The context should be in the form of a list of
    dictionaries, where each dictionary contains 'user_message' and
    'bot_response' keys.

    Args:
        memory (ConversationEntityMemory): The memory object to be updated.
        context (list): A list of dictionaries containing conversation context
            with 'user_message' and 'bot_response' keys.

    Returns:
        ConversationEntityMemory: The updated memory object with the conversation context.
    """

    for item in context:
        # Load memory variables and save context for the standardized message
        _input = {"input": item["user_message"]}
        memory.load_memory_variables(_input)
        memory.save_context(_input, {"output": item["bot_response"]})

    return memory


def llm_ai_chatbot(human_input, input_memory):
    """Converse with the chatbot using the OpenAI language model.

    This function allows you to interact with a chatbot using the OpenAI language
    model for conversations related to insurance and credits.

    Args:
        human_input (str): The user input (message) for the chatbot.

    Returns:
        str: The chatbot's response to the user input.
    """

    # Instanciação do modelo da OpenAI
    llm = OpenAI(
        model="text-davinci-003",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        max_tokens=256,
    )

    # Template para a conversa com variáveis a serem substituídas
    template = """Você é um chatbot conversando com um humano sobre seguros e créditos. Por favor, responda em Português BR e use no máximo 2 linhas.
    Context: {entities}
    Current conversation: {history}
    Humano: {input}
    Chatbot:"""

    # Prompt com variáveis para substituir no template
    prompt = PromptTemplate(
        input_variables=["entities", "history", "input"], template=template
    )

    # Criação da memória da conversa
    memory = ConversationEntityMemory(llm=llm)

    # Extrai o contexto da memória
    memory = extract_context(memory, input_memory)

    # Criação da cadeia de conversa
    conversation = ConversationChain(
        llm=llm,
        verbose=True,
        prompt=prompt,
        memory=memory,
    )

    # Retorno da resposta do chatbot ao input do usuário
    return conversation.predict(input=human_input)
