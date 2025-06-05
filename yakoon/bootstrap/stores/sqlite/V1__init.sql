-- Yakoon Session Schema: Initial Structure

CREATE TABLE IF NOT EXISTS sessions (
    _domain TEXT NOT NULL,
    _bucket TEXT NOT NULL,
    _scope TEXT NOT NULL,
    _id TEXT NOT NULL,
    lang TEXT,
    data_storage TEXT,
    PRIMARY KEY (_domain, _bucket, _scope, _id)
);
