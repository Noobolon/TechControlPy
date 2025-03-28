import os

from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Definições do Supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Funções do banco de dados


# Clientes / Técnicos

# Pega os clientes com status 0 (ticket aberto)
def getAvailableClients():
    try:
        available_clients = (
            supabase.table("client")
            .select("*")
            .eq('status', '0')
            .execute()
        )
        return available_clients.data
    
    except Exception as error:
        print(error)
        return None

# Pega os técnicos com status 0 (disponíveis)
def getAvailableTechs():
    try:
        available_technicians = (
            supabase.table("maintenance")
            .select("*")
            .eq('status', '0')
            .execute()
        )
        return available_technicians.data
    
    except Exception as error:
        print(error)
        return None
    
# Pega um técnico pelo ID com status 0
def getTechFromId(tech_id):
    try:
        tech = (
            supabase.table("maintenance")
            .select("*")
            .eq('id_maintenance', tech_id)
            .eq('status', '0')
            .execute()
        )
        return tech.data[0]

    except Exception as error:
        print(error)
        return None


# Serviços

# Pegar serviços abertos
def getOpenServices(tech_id):

    if tech_id: # Se um ID de técnico for informado na função, retornar os serviços relacionados à ele
        try:
            open_services = (
                supabase.table("service")
                .select("*")
                .eq('status', '0')
                .eq('fk_id_maintenance', tech_id)
                .execute()
            )
            return open_services.data
        
        except Exception as error:
            print(error)
            return None
    else:
        try:
            open_services = (
                supabase.table("service")
                .select("*")
                .eq('status', '0')
                .execute()
            )
            return open_services.data
        
        except Exception as error:
            print(error)
            return None

# Pegar serviço com o ID informado
def getServiceFromId(service_id):

    try:
        service_id = int(service_id)
        service = (
            supabase.table("service")
            .select("*")
            .eq('id_service', service_id)
            .execute()
        )
        return service.data[0]
    
    except Exception as error:
        print(error)
        return None

# Criar serviço com os dados informados
def createNewService(client, tech):
    try:
        new_service = {
            "fk_id_client": client["id_client"],
            "fk_id_maintenance": tech["id_maintenance"],
            "status": 0
        }
        service = supabase.table("service").insert(new_service).execute()

        if service: 
            return service
        else:
            return None

    except Exception as error:
        print(error)
        return None


# Aceitar um serviço
def acceptService(service):

    try:
        service_id = int(service['id_service'])

        accepted_service = (
            supabase.table("service")
            .update({"status": 1}) 
            .eq('id_service', service_id)
            .execute() 
        )

        # Atualiza o status e a chave estrangeira do técnico 
        change_status_tech = (
            supabase.table("maintenance")
            .update({"status": 1})
            .eq('id_maintenance', service['fk_id_maintenance'])
            .execute()
        )

        # Atualiza o status do cliente
        change_status_client = (
            supabase.table("client")
            .update({"status": 1})
            .eq('id_client', service['fk_id_client'])
            .execute()
        )

        return accepted_service

    except Exception as error:
        print(error)
        return None
    

# Completar um serviço e mudar o status do cliente e técnico
def completeService(service):
    try:
        service_id = int(service['id_service'])

        accepted_service = (
            supabase.table("service")
            .update({"status": 1}) 
            .eq('id_service', service_id)
            .execute() 
        )

        # Atualiza o status e a chave estrangeira do técnico 
        change_status_tech = (
            supabase.table("maintenance")
            .update({"status": 0})
            .eq('id_maintenance', service['fk_id_maintenance'])
            .execute()
        )

        # Atualiza o status do cliente
        change_status_client = (
            supabase.table("client")
            .update({"status": 1})
            .eq('id_client', service['fk_id_client'])
            .execute()
        )

        return accepted_service

    except Exception as error:
        print(error)
        return None