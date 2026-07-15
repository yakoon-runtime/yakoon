# Architecture

> **Yakoon is a runtime with a language-neutral Runtime Bus.**
> **Applications do not communicate with each other — they communicate exclusively with the Runtime through a stable ABI.**

## Evolution

Yakoon started as a Python framework and evolved into a
language-neutral runtime platform.

```
SDK (Python, Go, Ruby, …)
   │
   ▼
Runtime Bus (Call/Response)
   │
   ├── CallHandler
   ├── RegisterProviderHandler
   ├── EventHandler
   │
   ├── Resolver (port → provider_id)
   │
   ├── Transport (direct / pipe / socket)
   │
   └── Provider (asyncpg, MQTT, SAP, …)
```

### Executor Levels

| Level   | Executor | ABI | Language | Use case |
|---------|----------|-----|----------|----------|
| Kernel  | `runtime` | `async def run(space)` | Python | Setup, provider registration, async init |
| Command | `python` | `print()` → stdout | Python | Business commands, port consumers |
| Script  | `script` | `print()` → stdout | Python | Isolated scripts (custom venv) |
| Native  | `process` | `_yak/run/app` (shebang) | Any | Non-Python commands (Go, Ruby, …) |

## Runtime Architecture

```
┌──────────────────────────────────────────┐
│         Runtime Kernel                   │
│                                          │
│  ┌──────────┐  ┌────────────────────┐    │
│  │ Resolver │  │    Runtime Bus     │    │
│  │ port→id  │  │ dispatch(message)  │    │
│  └──────────┘  └────────┬───────────┘    │
│                         │                │
│  ┌──────────────────────▼────────────┐   │
│  │         Handlers                 │   │
│  │  CallHandler / RegisterHandler /…│   │
│  └──────────────┬───────────────────┘   │
│                 │                        │
│  ┌──────────────▼───────────────────┐   │
│  │  Transport (DirectTransport)     │   │
│  │  send(provider_id, call)         │   │
│  └──────────────┬───────────────────┘   │
│                 │                        │
│  ┌──────────────▼───────────────────┐   │
│  │  Provider (contacts, worlds, …)  │   │
│  │  asyncpg connections / memory    │   │
│  └──────────────┬───────────────────┘   │
│                 │                        │
│         Runtime Event Loop               │
└──────────────────────────────────────────┘
                    ▲
                    │
          run_coroutine_threadsafe()
                    │
┌──────────────────────────────────────────┐
│         Executor (ThreadPool)            │
│                                          │
│  ┌──────────────────────────────────┐    │
│  │       Command Script             │    │
│  │  ports.get("crm.contact.service")│    │
│  │  .list_contacts(ns)              │    │
│  └──────────────────────────────────┘    │
│                                          │
│  ┌──────────────────────────────────┐    │
│  │  SDK (_PortProxy → invoke(Call)) │    │
│  └──────────────────────────────────┘    │
└──────────────────────────────────────────┘
```

## Runtime Rule #1 — Event Loop Ownership

> **All long-lived runtime resources belong to the Runtime Event Loop.**
>
> Executors must never access these resources directly. They communicate exclusively through the Runtime Bus. The Transport is responsible for safely handing calls (and coroutines) into the Runtime Event Loop.

Resources that live on the Runtime Loop:

- Scheduler
- Provider instances (services, stores)
- Database connection pools (asyncpg, etc.)
- Runtime Bus and its handlers
- Resolver (port → provider_id mapping)

This rule applies to any resource bound to an event loop:
PostgreSQL pools, MQTT clients, Redis connections, WebSockets — all live on the Loop.

### How it works

1. Setup phase (`runtime` executor) creates providers on the Runtime Loop
2. Command phase (`python` executor) runs in a ThreadPool thread
3. When a command calls a port method, the SDK sends a `Call` via the Bus
4. `CallHandler` resolves the provider and calls `Transport.send()`
5. `Transport.send()` detects the async function and uses `run_coroutine_threadsafe()` to execute it on the Runtime Loop
6. The result flows back through the Future to the calling thread

```python
# Command — runs in ThreadPool, knows nothing about the Loop
svc = ports.get("crm.contact.service")
contacts = svc.list_contacts(ns)  # → invoke(Call) → bus → transport → loop → provider → PostgreSQL
```

## What is a Command?

A command is executable code that receives input and produces output.
Everything else is optional.

|                | `runtime` | `python` | `script` | `process` |
|----------------|-----------|----------|----------|-----------|
| **Input**      | `space.request` | `sys.argv` | `sys.argv` | argv |
| **Output**     | `yield out_*`  | `print()`  | `print()`  | stdout |
| **Async**      | ✅ native      | ✅ via transport bridge | ✅ | ❌ |
| **Port access**| ✅ direct      | ✅ via SDK proxy | ❌ | ❌ |

### When to use what

- **runtime** — setup, provider registration, anything that creates long-lived async resources
- **python** — business commands (CRUD, queries, actions); runs in ThreadPool, speaks to providers via Bus
- **script** — Python in subprocess (isolation, custom venv)
- **process** — any program in any language (bash, go, rust, …)

## The Runtime Bus Protocol

```
SDK:                           Runtime:
────────────────────────────────────────────────
ports.get("hello").greet()
  → invoke(Call("hello","greet",{...}))
                               → bus.dispatch(Call)
                                 → CallHandler
                                   → resolver.resolve("hello","greet")
                                   → transport.send(provider_id, Call)
                                     → fn(**args)
                                     → Response(result="Hello!")
  ← Response
  ← "Hello!"

ports.register("hello", svc)
  → bus.dispatch(RegisterProvider(...))
                               → RegisterProviderHandler
                                 → resolver.register(provider_id, exports)
                                 → transport.register_provider(provider_id, svc)
                               ← Ok
  ← Ok
```

## Configuration

```
# _yak/run/yak.yml
runtime:
  executor:
    kind: python          # or: runtime, script, process
  transport:
    kind: direct          # or: pipe, socket, websocket
```

Executor and Transport are orthogonal. Any executor can use any transport.
The combination is set per command in its `_yak/run/yak.yml`.
