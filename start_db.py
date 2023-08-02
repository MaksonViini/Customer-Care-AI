from pymongo import MongoClient

client = MongoClient("localhost", 27017)
database = client["customer-care-db"]


script_collection = database["script"]


script_collection.insert_many(
    
  [
  {
    "steps": 7,
    "problem": {
      "id": 101,
      "description": "Sinistro Automotivo: O cliente sofreu um acidente com seu veículo e precisa de assistência para registrar e acompanhar o processo de sinistro. Ele deseja saber como proceder e obter informações sobre a cobertura e prazos de resolução."
    },
    "script": [
      {
        "step": 1,
        "message": "Sinto muito pelo ocorrido. Conte-me mais sobre o acidente e o estado atual do veículo."
      },
      {
        "step": 2,
        "message": "Entendo a situação e estou aqui para ajudá-lo com o sinistro automotivo. Vamos seguir com o processo."
      },
      {
        "step": 3,
        "message": "Você já registrou um Boletim de Ocorrência? Se sim, por favor, informe o número."
      },
      {
        "step": 4,
        "message": "Para agilizar o processo, preciso que você nos forneça os documentos necessários, como cópia da CNH, documentos do veículo, Boletim de Ocorrência, etc."
      },
      {
        "step": 5,
        "message": "Após recebermos a documentação necessária, iniciaremos a análise do sinistro e informaremos a cobertura e os prazos de resolução."
      },
      {
        "step": 6,
        "message": "Caso haja necessidade de vistoria ou outros procedimentos, agendaremos as etapas adicionais."
      },
      {
        "step": 7,
        "message": "Estamos empenhados em resolver o seu sinistro da melhor forma possível. Acompanharemos todo o processo e você poderá contar conosco para qualquer dúvida ou suporte adicional."
      }
    ]
  },
  {
    "steps": 6,
    "problem": {
      "id": 102,
      "description": "Contratação de Seguro Residencial: O cliente está interessado em adquirir um seguro residencial para sua casa e precisa de orientações sobre as opções de cobertura, valores de prêmios e procedimentos para contratação."
    },
    "script": [
      {
        "step": 1,
        "message": "Ótimo, estamos aqui para ajudá-lo a proteger sua residência. Conte-me mais sobre a localização e características da sua casa."
      },
      {
        "step": 2,
        "message": "Entendido. Vamos analisar suas necessidades e apresentar as opções de cobertura disponíveis para o seguro residencial."
      },
      {
        "step": 3,
        "message": "Com base nas informações fornecidas, recomendaremos as coberturas adequadas para atender às suas necessidades específicas."
      },
      {
        "step": 4,
        "message": "Após a seleção das coberturas, informaremos os valores dos prêmios e os detalhes do contrato."
      },
      {
        "step": 5,
        "message": "Você poderá revisar o contrato e, se concordar com os termos, prosseguiremos com a contratação."
      },
      {
        "step": 6,
        "message": "Parabéns! Seu seguro residencial foi contratado com sucesso. Você receberá todas as informações por e-mail e poderá contar conosco para qualquer assistência relacionada ao seguro."
      }
    ]
  },
  {
    "steps": 5,
    "problem": {
      "id": 103,
      "description": "Atualização de Dados Cadastrais: O cliente precisa atualizar informações em seu cadastro, como mudança de endereço, telefone ou e-mail. Ele deseja saber como proceder e garantir que os dados estejam corretos em seus seguros."
    },
    "script": [
      {
        "step": 1,
        "message": "Entendido. Vamos ajudá-lo a atualizar seus dados cadastrais."
      },
      {
        "step": 2,
        "message": "Por favor, forneça os detalhes das informações que você deseja atualizar, como endereço, telefone ou e-mail."
      },
      {
        "step": 3,
        "message": "Verificaremos as informações e faremos as atualizações em seu cadastro."
      },
      {
        "step": 4,
        "message": "Após a atualização, enviaremos um e-mail de confirmação com os novos dados cadastrais."
      },
      {
        "step": 5,
        "message": "Pronto! Seus dados foram atualizados com sucesso em nossos registros. Caso tenha mais alguma alteração, fique à vontade para nos contatar."
      }
    ]
  },
  {
    "steps": 4,
    "problem": {
      "id": 104,
      "description": "Esclarecimento de Cobertura: O cliente possui um seguro contratado, mas está com dúvidas sobre quais eventos estão cobertos pelo seguro. Ele precisa de assistência para entender a abrangência e limitações de sua apólice."
    },
    "script": [
      {
        "step": 1,
        "message": "Compreendido. Vamos esclarecer suas dúvidas sobre a cobertura de seu seguro."
      },
      {
        "step": 2,
        "message": "Por favor, informe-nos o número de sua apólice para que possamos verificar os detalhes da cobertura."
      },
      {
        "step": 3,
        "message": "Analisaremos sua apólice e forneceremos informações detalhadas sobre os eventos cobertos e as limitações de sua apólice."
      },
      {
        "step": 4,
        "message": "Esperamos que as informações tenham sido úteis. Caso precise de mais esclarecimentos, estamos à disposição para ajudá-lo."
      }
    ]
  },
  {
    "steps": 5,
    "problem": {
      "id": 105,
      "description": "Cancelamento de Seguro: O cliente deseja cancelar um seguro contratado anteriormente. Ele precisa de orientações sobre o processo de cancelamento e possíveis reembolsos."
    },
    "script": [
      {
        "step": 1,
        "message": "Entendido. Vamos ajudá-lo com o processo de cancelamento de seu seguro."
      },
      {
        "step": 2,
        "message": "Por favor, informe-nos o número de sua apólice e o motivo do cancelamento."
      },
      {
        "step": 3,
        "message": "Analisaremos sua solicitação e informaremos sobre quaisquer reembolsos aplicáveis, de acordo com os termos de seu contrato."
      },
      {
        "step": 4,
        "message": "Após a confirmação do cancelamento, enviaremos um e-mail de confirmação com os detalhes do processo."
      },
      {
        "step": 5,
        "message": "O cancelamento foi processado com sucesso. Caso tenha mais alguma questão ou precise de outro seguro no futuro, não hesite em nos contatar."
      }
    ]
  }
]

)
