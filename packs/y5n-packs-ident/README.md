# y5n-packs-ident

*Identity and permission management for Yakoon.*

This package provides account administration, group management,
permission grants, and authentication services.

## Commands

| Command | Module | Description |
|---------|--------|-------------|
| `su` | `y5n.packs.ident.su` | Authenticate (switch account) |
| `accounts add` | `y5n.packs.ident.apps.accounts.add` | Create an account (with optional profile) |
| `accounts list` | `y5n.packs.ident.apps.accounts.list` | List accounts |
| `accounts edit` | `y5n.packs.ident.apps.accounts.edit` | Modify an account |
| `accounts delete` | `y5n.packs.ident.apps.accounts.delete` | Remove an account |
| `groups add` | `y5n.packs.ident.apps.groups.add` | Create a group |
| `groups list` | `y5n.packs.ident.apps.groups.list` | List groups |
| `groups edit` | `y5n.packs.ident.apps.groups.edit` | Modify a group |
| `groups delete` | `y5n.packs.ident.apps.groups.delete` | Remove a group |
| `joins add` | `y5n.packs.ident.apps.joins.add` | Add account to group |
| `joins remove` | `y5n.packs.ident.apps.joins.remove` | Remove account from group |
| `joins groups` | `y5n.packs.ident.apps.joins.groups` | List groups for an account |
| `joins accounts` | `y5n.packs.ident.apps.joins.accounts` | List accounts in a group |
| `grants account add` | `y5n.packs.ident.apps.grants.account_add` | Grant permission to account |
| `grants account remove` | `y5n.packs.ident.apps.grants.account_remove` | Revoke permission from account |
| `grants account show` | `y5n.packs.ident.apps.grants.account_show` | Show account permissions |
| `grants group add` | `y5n.packs.ident.apps.grants.group_add` | Grant permission to group |
| `grants group remove` | `y5n.packs.ident.apps.grants.group_remove` | Revoke permission from group |
| `grants group show` | `y5n.packs.ident.apps.grants.group_show` | Show group permissions |
| `grants path show` | `y5n.packs.ident.apps.grants.perm_show` | Show who has access to a path |

## Model

- **Account** — the only security identity: login, credentials, groups,
  grants. An account may optionally carry profile information (`name`,
  `mail`, `language`). A human is an account with a profile; a bot is an
  account without one. There is no separate user concept.
- **Group** — a bundle of accounts that may itself carry grants.
- **Join** — account-to-group membership.
- **PermissionGrant** — grants access to a runtime path, set on an account
  or a group. A grant is `path + bits (+ deny)`.

## Services

The package also provides backend services used by the runtime:

- **AccountService** — account creation, lookup, password verification
- **AuthenticationService** — credential validation, session auth
- **GroupService** — group CRUD
- **JoinService** — account-group membership
- **PermissionGrantService** — permission grants
- **PermissionResolver** — resolves an account's effective permissions into
  spec strings the engine parses into a session PermissionSet
- **Verifier** — password policy enforcement

## Setup

On first start, `bootstrap.py` creates the default root account
and initial permission set.
