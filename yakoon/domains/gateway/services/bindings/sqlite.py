from yakoon.domains.gateway.stores._db.sqlite import\
      LocalSqlSession, create_missing_tables 
from yakoon.engines.render.jinja.engine import JinjaEngine
from yakoon.runtime.system.registry import PlatformServiceRegistry
from yakoon.services.session import SessionService
from yakoon.domains.gateway.services.account import AccountService
from yakoon.domains.gateway.stores.sql.account import SQLAccountStore
from yakoon.domains.gateway.stores.sql.session import SQLSessionStore
from yakoon.services.render import RendererService


def bind_sql_services() -> PlatformServiceRegistry:
    """
    Returns a ServiceRegistry with SQLite-backed service bindings.
    Used for persistent local development.
    """
    db = LocalSqlSession()
    create_missing_tables()

    return PlatformServiceRegistry(
        renderer=RendererService(JinjaEngine()),
        sessions=SessionService(SQLSessionStore(db)),
        accounts=AccountService(SQLAccountStore(db))
    )
