"""
Maps extracted JSON data to Excel tracker column positions.
Produces exactly ONE row per PDF — array values are joined with commas.
"""

from config import COLUMN_MAPPINGS


def map_to_tracker(extracted: dict, case_number: int) -> list[dict]:
    """
    Map extracted JSON fields to a single tracker row.

    Each uploaded PDF = 1 row. If the LLM returns arrays
    (e.g. multiple vehicle numbers), they are comma-joined into one cell.

    Args:
        extracted: Dict of field_name -> value from LLM extraction.
        case_number: 1, 2, or 3.

    Returns:
        List containing exactly one row dict mapping column_number -> value.
    """
    col_map = COLUMN_MAPPINGS[case_number]
    row = {}

    for field_name, col_num in col_map.items():
        if field_name == "s_no":
            row[col_num] = 1
            continue

        val = extracted.get(field_name)

        if val is None:
            continue

        # If LLM returned a list, join into a single comma-separated string
        if isinstance(val, list):
            val = ", ".join(str(v) for v in val if v is not None)

        row[col_num] = val

    return [row]
