from yakoon.platform.services.account import AccountService
from yakoon.platform.stores._db.sqlite import SessionLocal
from yakoon.platform.stores.sql.account import SQLAccountStore

def bind_sql_storages():
    """
    Binds all services to SQLite-backed SQLAlchemy stores.
    Used for development or lightweight persistence scenarios.
    """
    db = SessionLocal()

    # TODO: SessionService.
    AccountService.bind_storage(SQLAccountStore(db))
