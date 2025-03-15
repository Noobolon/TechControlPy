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
        clientes_disponiveis = (
            supabase.table("client")
            .select("*")
            .eq('status', '0')
            .execute()
        )
        return clientes_disponiveis.data
    
    except Exception as error:
        print(error)
        return None

# Pega os técnicos com status 0 (disponível)
def getAvailableTechs():
    try:
        tecnicos_disponiveis = (
            supabase.table("maintenance")
            .select("*")
            .eq('status', '0')
            .execute()
        )
        return tecnicos_disponiveis.data
    
    except Exception as error:
        print(error)
        return None

def createNewService(client, tech):
    new_service = {
        "fk_id_client": client["id_client"],
        "fk_id_maintenance": tech["id_maintenance"],
        "status": 0
    }
    supabase.table("service").insert(new_service).execute()
    print("Novo ticket criado.")

