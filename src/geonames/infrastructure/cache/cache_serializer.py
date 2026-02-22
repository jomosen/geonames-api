import json
from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from typing import Any, List


class _GeonamesEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, date):
            return {"__date__": obj.isoformat()}
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def _decode_hook(d: dict) -> Any:
    if "__date__" in d:
        return date.fromisoformat(d["__date__"])
    return d


def rows_to_json(rows: list) -> str:
    """Serialize SQLAlchemy Row objects (from query(*columns)) to JSON string."""
    return json.dumps(
        [dict(row._mapping) for row in rows],
        cls=_GeonamesEncoder,
    )


def models_to_json(models: list) -> str:
    """Serialize full SQLAlchemy ORM model instances to JSON string."""
    return json.dumps(
        [
            {c.key: getattr(m, c.key) for c in m.__class__.__table__.columns}
            for m in models
        ],
        cls=_GeonamesEncoder,
    )


def json_to_namespaces(cached: str) -> List[SimpleNamespace]:
    """Deserialize a JSON string back to a list of SimpleNamespace objects."""
    rows = json.loads(cached, object_hook=_decode_hook)
    return [SimpleNamespace(**r) for r in rows]
