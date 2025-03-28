# from time import sleep

from fastapi import FastAPI, HTTPException
from modules.database_functions import *
from modules.calc_functions import *


app = FastAPI()

@app.get("/available_techs/")
async def available_techs():
  available_techs = getAvailableTechs()
  if available_techs:
    return {"available_maintenance": available_techs}
  else:
    raise HTTPException(status_code=404, detail="Nenhum técnico disponível.")


@app.put("/service/{service_id}/{tech_id}/accept")
async def accept_service(service_id: int, tech_id: int):

  
  service = getServiceFromId(service_id)

  # return {"response":  table_tech_id}

  if service["fk_id_maintenance"] == tech_id:
    accepted_service = acceptService(service)

    if accepted_service:
      results = {"service": accepted_service}
      return results
    
    else:
      raise HTTPException(status_code=404, detail="Erro ao aceitar serviço.")
  else:
    raise HTTPException(status_code=404, detail="Erro: serviço não contém um técnico com esse ID.")



# INCOMPLETO

# Função de criar serviços 
# @app.get("/allocate_service/")
# def allocate_service():
    
#   available_techs = getAvailableTechs()
#   open_clients = getAvailableClients()

#   # Se não encontrar:
#   if not available_techs or not open_clients:
#    raise HTTPException(status_code=404, detail="Nenhum técnico disponível / Nenhum cliente com ticket aberto.")
        
#   for client in open_clients:
#     best_tech = None 
#     best_score = float("inf") # Pontuação infinita para a comparação entre os técnicos

#     # Para cada técnico na lista
#     for i, tech in enumerate(available_techs):

#       distance = calcDistance(tech, client)

#       # Critério de qualificação: técnicos com a especialidade correspondente ao problema do cliente têm prioridade
#       qualification_score = 0 if tech["specialty"].lower() in client["problem"].lower() else 1
       
#       # Pontuação = distância + (qualificação), se não houver (for 0) reduz a pontuação do técnico
#       score = distance + (qualification_score * 10)

#       if score < best_score:
#         best_score = score
#         best_tech = tech
        
#     # Depois de encontrar o melhor técnico entre os disponíveis
#     if best_tech:
#       service = createNewService(client, best_tech)
#       if service:
#         return {"service:": service.data}

