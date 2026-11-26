import logging
import os
from functools import lru_cache

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

logger = logging.getLogger(__name__)


class SupabaseConfigurationError(RuntimeError):
    """Indica que as variáveis obrigatórias do Supabase não foram configuradas."""


@lru_cache(maxsize=1)
def get_supabase() -> Client:
    """Cria o cliente uma única vez usando as variáveis do ambiente do deploy."""
    url = os.getenv("SUPABASE_URL", "").strip()
    # SUPABASE_KEY é mantida por compatibilidade; ANON_KEY é o nome recomendado.
    chave = (
        os.getenv("SUPABASE_ANON_KEY", "").strip()
        or os.getenv("SUPABASE_KEY", "").strip()
    )

    if not url or not chave:
        raise SupabaseConfigurationError(
            "SUPABASE_URL e SUPABASE_ANON_KEY (ou SUPABASE_KEY) são obrigatórias."
        )

    if not url.startswith(("http://", "https://")):
        raise SupabaseConfigurationError("SUPABASE_URL deve ser uma URL HTTP/HTTPS válida.")

    try:
        return create_client(url, chave)
    except Exception as exc:
        logger.exception("Falha ao inicializar o cliente Supabase")
        raise SupabaseConfigurationError("Não foi possível inicializar o Supabase.") from exc


def supabase_is_configured() -> bool:
    """Verifica a configuração sem registrar ou retornar a chave secreta."""
    return bool(
        os.getenv("SUPABASE_URL", "").strip()
        and (
            os.getenv("SUPABASE_ANON_KEY", "").strip()
            or os.getenv("SUPABASE_KEY", "").strip()
        )
    )
