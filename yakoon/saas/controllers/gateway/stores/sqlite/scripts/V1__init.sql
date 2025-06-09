CREATE TABLE IF NOT EXISTS accounts (
    __key__ TEXT PRIMARY KEY,
    __scope__ TEXT NOT NULL,
    __created_at__ TEXT NOT NULL,

    name TEXT,
    permissions TEXT,
    cmd_groups TEXT
);

CREATE INDEX IF NOT EXISTS idx_account_scope ON accounts (__scope__);
CREATE INDEX IF NOT EXISTS idx_account_created ON accounts (__created_at__);
