from time import sleep

# from fastapi import FastAPI, HTTPException
from modules.database_functions import *
from modules.calc_functions import *


#app = FastAPI()
# @app.get("/allocate_service/")

def allocate_service():
    
  avaiable_techs = getAvailableTechs()
  open_clients = getAvailableClients()

  if not avaiable_techs or not open_clients:
        # raise HTTPException(status_code=404, detail="Nenhum técnico disponível ou nenhum cliente com ticket aberto.")
        print("Nenhum cliente ou técnico encontrado.")

  for client in open_clients:
    best_tech = None 
    best_score = float("inf") # Pontuação infinita para a comparação entre os técnicos

    # Para cada técnico na lista
    for i, tech in enumerate(avaiable_techs):
       
       print(tech)
       sleep(2)

       distance = calcDistance(tech, client)

       # Critério de qualificação: técnicos com a especialidade correspondente ao problema do cliente têm prioridade
       qualification_score = 0 if tech["specialty"].lower() in client["problem"].lower() else 1
       
       # Pontuação = distância + (qualificação), se não houver (for 0) reduz a pontuação do técnico
       score = distance + (qualification_score * 10)

       if score < best_score:
        best_score = score
        best_tech = tech
        
    # Depois de encontrar o melhor técnico entre os disponíveis
    if best_tech:
       createNewService(client, best_tech)

  #return {"message": "Serviços alocados com sucesso"}


allocate_service()
       

            

       

      
      

