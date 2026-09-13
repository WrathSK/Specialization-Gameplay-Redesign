"""Machine paths are explicit, never inferred from a parent game workspace."""
from pathlib import Path
import json, os

def external_database(root):
    value=os.environ.get('SPC_DEBUG_GAMEPLAY_DB')
    config=root/'local/config.json'
    if not value and config.is_file():
        value=json.loads(config.read_text()).get('debug_gameplay_db')
    if not value:
        raise RuntimeError('Set SPC_DEBUG_GAMEPLAY_DB or local/config.json debug_gameplay_db; game database remains external and read-only.')
    path=Path(value).expanduser()
    if not path.is_absolute() or not path.is_file():
        raise RuntimeError('External DebugGameplay.sqlite must be an existing absolute file path')
    return path
