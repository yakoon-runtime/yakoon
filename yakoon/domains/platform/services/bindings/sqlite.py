from yakoon.domains.platform.stores._db.sqlite import\
      LocalSqlSession, create_missing_tables 
from yakoon.services.registry import PlatformServiceRegistry
from yakoon.services.core.session import SessionService
from yakoon.domains.platform.services.account import AccountService
from yakoon.domains.platform.stores.sql.account import SQLAccountStore
from yakoon.domains.platform.stores.sql.session import SQLSessionStore
from yakoon.services.renderer.engines.jinja import JinjaEngine
from yakoon.services.renderer.service import RendererService


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
