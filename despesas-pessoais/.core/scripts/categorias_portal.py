"""Resolve a portal purpose category; participation/rateio remains a separate step."""
import json
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / 'modelos/categorias_portal.json'

def linha_por_categoria(category: str) -> str | None:
    """None means unresolved, never silently 'Outros'. Does not apply card splits."""
    rows = json.loads(CATALOG.read_text(encoding='utf-8'))
    match = next((r for r in rows if r['id'] == category), None)
    if match is None:
        raise ValueError(f'Categoria desconhecida no portal: {category}')
    return match['sheetLine']
