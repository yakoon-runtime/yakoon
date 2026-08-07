# y5n-packs-ident

*Identity, authorization and session security for Yakoon.*

`ident` answers three independent questions:

| Question | Concept |
| -------- | ------- |
| Who are you? | **Account** |
| What may you do? | **Grants** |
| How are you currently working? | **Session** |

The three are kept strictly separate. A permission system that mixes
them (a "user" that is also a role, a login that is also a rights set)
makes every change unpredictable. `ident` keeps each concept to a single
question — and Yakoon's security is built on that separation.

Everything fits together in one picture:

```
            Account
               │
        ┌──────┴──────┐
        │             │
     Groups        Grants
        │             │
        └──────┬──────┘
               │
      Effective Permissions
               │
            Session
               │
           privileged?
               │
           Execution
```

---

## Core Concepts

### Account

An identity. A human or a bot — Yakoon does not distinguish. An account
authenticates (login, credentials), belongs to groups, receives grants
and may optionally carry profile information (`name`, `mail`, `language`).

> **An account is the single identity in Yakoon.**
>
> Accounts authenticate, belong to groups, receive grants and may
> optionally carry profile information. Human users are simply accounts
> with a profile.

There is exactly one identity concept. Nothing else logs in, nothing
else is granted rights.

### Group

A collection of accounts. A group exists for one purpose only: to manage
permissions for several accounts at once. A group may itself carry grants.

### Join

The link between an account and a group: *stefan is a member of admins*.

### Grant

A grant connects a subject to a runtime path:

```
Account / Group
        │
        ▼
  Runtime Path
        │
        ▼
 Permission Bits
```

Not commands. Not controllers. Not applications. **Runtime paths.** A
grant is `path + bits (+ deny)`. Granting access to `/usr/bin` means
granting access to everything the runtime serves at that path — the
mount structure of the runtime tree *is* the security model.

---

## Permissions

> **The runtime tree is the authorization tree.**

The rules that follow from grants on runtime paths:

- **Permissions are granted on runtime paths.** A grant on `/usr/bin`
  applies to `/usr/bin` and everything below it.
- **Permissions are inherited down the tree.** The mount structure
  becomes the security model — a pack chooses where it lives, and that
  is where its rights begin.
- **Traversal is automatic.** You can always reach your own grants. An
  explicitly allowed area is never unreachable — even a deny on an
  ancestor cannot remove the path to your own rights.
- **Deny subtracts only its own bits.** A `deny /usr/bin/shutdown|x`
  removes only `x` from an inherited `allow /usr/bin|rwx` — `r` and `w`
  remain.
- **`/` is just the highest grant.** Root is what an account looks like
  from the outside when its grant begins at the root. There is no
  superuser flag and no special-cased identity.

---

## Sessions

The session answers *how you are working right now* — independent of who
you are and what you may do:

```
Normal Session         → privileged operations ask for confirmation
Temporary Elevation    → the next privileged operation is confirmed once
Administrative Session → no additional confirmation for privileged operations
```

> **A session never grants additional permissions. It only changes how
> privileged operations are confirmed.**

A command that is declared `privileged` requires an elevated session on
top of the grant. Without elevation it is refused; with elevation it
runs — but always within the rights your grants already give you. An
administrative session does not make you root; it only stops asking.

Elevation is established at login:

```
su USER --password SECRET                  → normal session
su USER --password SECRET --temporary      → next privileged op runs
su USER --password SECRET --administrative → privileged ops run directly
```

The login is the conscious act; the password is the confirmation.

---

## Commands

| Command | Purpose |
| ------- | ------- |
| `su` | Authenticate (switch account) |
| `logout` | End the session |
| `accounts add` | Create an account (with optional profile) |
| `accounts list` | List accounts |
| `accounts edit` | Modify an account |
| `accounts delete` | Remove an account |
| `groups add` | Create a group |
| `groups list` | List groups |
| `groups edit` | Modify a group |
| `groups delete` | Remove a group |
| `joins add` | Add an account to a group |
| `joins remove` | Remove an account from a group |
| `joins groups` | List groups for an account |
| `joins accounts` | List accounts in a group |
| `grants account add` | Grant permission to an account |
| `grants account remove` | Revoke permission from an account |
| `grants account show` | Show an account's permissions |
| `grants group add` | Grant permission to a group |
| `grants group remove` | Revoke permission from a group |
| `grants group show` | Show a group's permissions |
| `grants path show` | Show who has access to a path |

---

## Example

A small scenario, end to end:

```
Create an account.                accounts add stefan
Create a group.                   groups add admins
Add the account to the group.     joins add stefan admins
Grant the group access to paths.  grants group add admins /usr/bin --bits rwx
                                  grants group add admins /usr/sbin/ident --bits rwx
Login.                            su stefan --password 123
```

`stefan` can now use everything under `/usr/bin` and administer the
ident area — because the `admins` group holds those grants and stefan is
a member.

---

## Bootstrap

`bootstrap.py` seeds the default setup on first start:

| Account | Password | Rights |
| ------- | -------- | ------ |
| `root` | `master` | the top grant `/` via the `admins` group |
| `stefan` | `123` | no grants (demo profile) |
| `lara` | `456` | no grants |

---

## Services

Backend services used by the runtime:

- **AccountService** — account creation, lookup, password verification
- **AuthenticationService** — credential validation, session auth
- **GroupService** — group CRUD
- **JoinService** — account-group membership
- **PermissionGrantService** — permission grants
- **PermissionResolver** — resolves an account's effective permissions
  into spec strings the engine parses into a session `PermissionSet`
- **Verifier** — password policy enforcement
