# from time import sleep

from fastapi import FastAPI, HTTPException
from modules.database_functions import *
from modules.calc_functions import *

app = FastAPI()

# Rotas GET

# Função de pesquisar por serviços
@app.get("/search_clients/{tech_id}")
def search_clients(tech_id: int):
    
    tech = getTechFromId(tech_id)
    
    if not tech:
      raise HTTPException(status_code=404, detail="Técnico não encontrado.")
    
  
    available_clients = getAvailableClients()
    if not available_clients:
      raise HTTPException(status_code=404, detail="Nenhum cliente encontrado.")
    
    scored_clients = []

    for client in available_clients:
      distance = calcDistance(tech, client)
      
      # Pontuação 0 se o técnico tiver a especialidade, se não 1
      qualification_score = 0 if tech["specialty"].lower() in client["problem"].lower() else 1
      
      # Quanto menor a pontuação, melhor
      score = distance + (qualification_score * 10)
      
      # Adiciona à lista
      scored_clients.append({ 
          "client": client,
          "score": score,
          "distance": distance,
          "specialty_match": qualification_score == 0 # Se tem a especialização ou não
      })
    
    # Ordena os clientes, da menor pontuação até a maior
    scored_clients.sort(key=lambda x: x["score"])
    
    return { "available_clients": scored_clients }



# Rotas POST

# Criar serviço
@app.post("/service/{client_id}/{tech_id}/create")
async def create_service(client_id: int, tech_id: int):

  client = getClientFromId(client_id)
  tech = getTechFromId(tech_id)

  if client and tech:
    new_service = createNewService(client, tech)

    if new_service:
      results = {"service": new_service}
      return results
    
    else:
      raise HTTPException(status_code=404, detail="Erro ao criar serviço.")
  else:
    raise HTTPException(status_code=404, detail="Erro: cliente ou técico não encontrado.")



# Rotas PUT

# Aceitar serviço como técnico
@app.put("/service/{service_id}/{tech_id}/accept")
async def accept_service(service_id: int, tech_id: int):

  service = getServiceFromId(service_id)

  if service["fk_id_maintenance"] == tech_id:
    accepted_service = acceptService(service)

    if accepted_service:
      results = {"service": accepted_service}
      return results
    
    else:
      raise HTTPException(status_code=404, detail="Erro ao aceitar serviço.")
  else:
    raise HTTPException(status_code=404, detail="Erro: serviço não contém um técnico com esse ID.")
  

# Concluir serviço
@app.put("/service/{service_id}/{tech_id}/complete")
async def complete_service(service_id: int, tech_id: int):

  service = getServiceFromId(service_id)

  if service["fk_id_maintenance"] == tech_id:

    completed_service = completeService(service)

    if completed_service:
      return {"service": completed_service}
    else:
      raise HTTPException(status_code=404, detail="Erro ao completar serviço.")

    
  else:
    raise HTTPException(status_code=404, detail="Erro: serviço não contém um técnico com esse ID.")



# Rotas DELETE

# Cancelar serviço enviado
@app.delete("/service/{service_id}/{tech_id}/cancel")
async def cancel_service(service_id: int, tech_id: int):

  service = getServiceFromId(service_id)

  if service["fk_id_maintenance"] == tech_id:

    canceled_service = cancelService(service)

    if canceled_service:
      return {"service": canceled_service}
    else:
      raise HTTPException(status_code=404, detail="Erro ao completar serviço.")

    
  else:
    raise HTTPException(status_code=404, detail="Erro: serviço não contém um técnico com esse ID.")