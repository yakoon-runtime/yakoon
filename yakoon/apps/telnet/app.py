# yakoon/apps/telnet/app.py

import asyncio
from yakoon.apps.telnet.session_bridge import handle_telnet_session


async def main():
    server = await asyncio.start_server(
        handle_telnet_session,
        host="0.0.0.0",
        port=4000
    )
    print("✅ Yakoon Telnet listening on port 4000")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
