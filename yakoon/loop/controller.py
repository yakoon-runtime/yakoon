from yakoon.loop.registry import CommandRegistry

def enter_room(args):
    return {"msg": f"You enter {args.get('room', 'an empty space')}"}

def register_controller():
    CommandRegistry.register("enter_room", enter_room)

    commands = [
        {"id": "cmd-001", "name": "look", "description": "...", "syntax": "..."},
        {"id": "cmd-002", "name": "pickup", "description": "...", "syntax": "..."},
        {"id": "cmd-003", "name": "enter_room", "description": "...", "syntax": "..."},
    ]

    return {
        "controller_id": "realm",
        "commands": commands
    }
