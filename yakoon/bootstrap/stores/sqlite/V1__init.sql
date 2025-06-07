-- Yakoon Session Schema: Initial Structure

CREATE TABLE IF NOT EXISTS sessions (
    _domain TEXT NOT NULL,
    _bucket TEXT NOT NULL,
    _scope TEXT NOT NULL,
    _id TEXT NOT NULL,
    lang TEXT,
    data_storage TEXT,
    last_active TEXT,
    PRIMARY KEY (_domain, _bucket, _scope, _id)
);

CREATE TABLE IF NOT EXISTS shards (
    prefix TEXT NOT NULL,
    shard_id INTEGER NOT NULL,
    range_start INTEGER NOT NULL,
    range_end INTEGER NOT NULL,
    value INTEGER NOT NULL DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (prefix, shard_id),
    CHECK (range_start < range_end),
    CHECK (value >= 0)
);
