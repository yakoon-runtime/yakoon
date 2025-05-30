from yakoon.platform.stores._db.sqlite import LocalSqlSession, create_missing_tables 
from yakoon.platform.services.account import AccountService
from yakoon.platform.services.session import SessionService
from yakoon.platform.stores.sql.account import SQLAccountStore
from yakoon.platform.stores.sql.session import SQLSessionStore


def bind_sql_storages():
    """
    Binds all services to SQLite-backed SQLAlchemy stores.
    Used for development or lightweight persistence scenarios.
    """
    db = LocalSqlSession()
    create_missing_tables()
    
    SessionService.bind_storage(SQLSessionStore(db))
    AccountService.bind_storage(SQLAccountStore(db))
