-- Yakoon Session Schema: Initial Structure

CREATE TABLE IF NOT EXISTS accounts (
    _domain TEXT NOT NULL,
    _bucket TEXT NOT NULL,
    _scope TEXT NOT NULL,
    _id TEXT NOT NULL,
    name TEXT,
    cmd_groups TEXT,
    PRIMARY KEY (_domain, _bucket, _scope, _id)
);
