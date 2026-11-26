from dotenv import load_dotenv
from supabase import create_client
import os

load_dotenv()

_cliente = None


# o cliente só é criado na primeira vez que alguém precisa dele,
# assim o site abre normalmente mesmo se o .env estiver sem as chaves
def get_supabase():
    global _cliente

    if _cliente is None:
        url = os.getenv("SUPABASE_URL")
        chave = os.getenv("SUPABASE_KEY")

        if not url or not chave:
            raise RuntimeError("Configure SUPABASE_URL e SUPABASE_KEY no arquivo .env")

        _cliente = create_client(url, chave)

    return _cliente
