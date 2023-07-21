from pymongo import MongoClient

from .config import get_db_url

DB_URL = get_db_url()

client = MongoClient("localhost", 27017)
database = client["teste_data"]
script_collection = database["script"]
users_collection = database["users"]

conversations_collection = database["bot"]

script_collection.insert_one(
    {
        "steps": 3,
        "script_id": 4,
        "script": [
            {
                "step": 1,
                "message": "Olá! Bem-vindo ao nosso suporte. Como posso ajudar você hoje?",
            },
            {
                "step": 2,
                "message": "Entendo que você está buscando ajuda para automatizar um processo de atendimento ao cliente no front office. Podemos orientar você nessa questão.",
            },
            {
                "step": 3,
                "message": "Você poderia fornecer mais detalhes sobre o processo que deseja automatizar? Quais são as etapas envolvidas e quais são os principais desafios que você está enfrentando em relação à eficiência?",
            },
            # {
            #     "step": 4,
            #     "message": "Quais são os objetivos que você deseja alcançar por meio da automação desse processo? Por exemplo, você está buscando reduzir o tempo de resposta, melhorar a qualidade do atendimento ou aumentar a satisfação dos clientes?",
            # },
            # {
            #     "step": 5,
            #     "message": "Com base nas informações fornecidas, vamos fornecer orientações sobre como melhorar a automação desse processo. Após coletarmos todas as informações necessárias, poderemos oferecer soluções mais específicas.",
            # },
            # {"step": 6, "message": "Coleta das informações"},
            # {
            #     "step": 7,
            #     "message": "Obrigado por fornecer os detalhes sobre o processo de atendimento ao cliente que você deseja automatizar. Vou encaminhar sua demanda para nossa equipe especializada, que analisará as informações e fornecerá as melhores práticas e soluções adequadas para otimizar a eficiência do seu processo.",
            # },
            # {
            #     "step": 8,
            #     "message": "Se você tiver mais alguma dúvida ou precisar de suporte adicional, não hesite em nos contatar novamente. Estamos aqui para ajudar. Obrigado pelo contato!",
            # },
        ],
    }
)


# def insert(**args):
#     try:
#         collection.insert_one(args)
#     except Exception:
#         return False


# def read(**args):
#     try:
#         return collection.find(args)
#     except Exception:
#         return False


# def update(args):
#     try:
#         collection.update_one(args[0], args[1])
#     except Exception:
#         return False


# def delete(args):
#     try:
#         collection.delete_one(args)
#     except Exception:
#         return False


# def delete_(args):
#     try:
#         collection.delete_many(args)
#     except Exception:
#         return False
