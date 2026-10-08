import json
from datetime import datetime, timezone

from config.settings import ANALYSIS_RESULTS_DIR


def save_analysis_result(result: dict, analysis_id: str) -> str:
    ANALYSIS_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    result_with_metadata = {
        "analysis_id": analysis_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "result": result,
    }

    result_path = ANALYSIS_RESULTS_DIR / f"{analysis_id}.json"

    result_path.write_text(
        json.dumps(result_with_metadata, indent=2),
        encoding="utf-8",
    )

    return str(result_path)


def load_analysis_result(analysis_id: str) -> dict | None:
    result_path = ANALYSIS_RESULTS_DIR / f"{analysis_id}.json"

    if not result_path.exists():
        return None

    return json.loads(
        result_path.read_text(encoding="utf-8")
    )