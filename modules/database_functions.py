import os

from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Definições do Supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Funções do banco de dados

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



