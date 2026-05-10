# Author: Kelvin Kabute
# Last-updated: 2026-05-10

# Author: Kelvin Kabute
# Last-updated: 2026-05-10

"""Regression tests for scripts/append_provenance.py."""

import importlib
import tempfile
from pathlib import Path


def _load_appender():
    return importlib.import_module("scripts.append_provenance")


def test_placeholder():
    # Placeholder: append tests when running in CI/local environment
    assert True


def test_skip_extensions_does_not_include_commentable_exts():
    """SKIP_EXTENSIONS and SAFE_CODE_EXTS must not overlap."""
    mod = _load_appender()
    overlap = mod.SKIP_EXTENSIONS & mod.SAFE_CODE_EXTS
    assert overlap == set(), (
        f"Extensions appear in both SKIP_EXTENSIONS and SAFE_CODE_EXTS: {overlap}. "
        "This means parsed formats could still receive provenance headers."
    )


def test_json_not_in_safe_code_exts():
    """.json is a parsed format — the appender must never touch it."""
    mod = _load_appender()
    assert ".json" not in mod.SAFE_CODE_EXTS, (
        ".json must not be in SAFE_CODE_EXTS; provenance headers break JSON parsers."
    )
    assert ".json" in mod.SKIP_EXTENSIONS, (
        ".json must be in SKIP_EXTENSIONS so the intent is explicit and auditable."
    )


def test_yaml_not_in_safe_code_exts():
    """YAML is a parsed format used for CI/CD configs — must not be touched."""
    mod = _load_appender()
    for ext in (".yaml", ".yml"):
        assert ext not in mod.SAFE_CODE_EXTS, (
            f"{ext} must not be in SAFE_CODE_EXTS."
        )
        assert ext in mod.SKIP_EXTENSIONS, (
            f"{ext} must be in SKIP_EXTENSIONS."
        )


def test_append_header_does_not_modify_json_file():
    """append_header must leave the content of a .json file completely unchanged."""
    mod = _load_appender()
    original = '{"MD013": false, "MD036": false}\n'
    with tempfile.NamedTemporaryFile(
        suffix=".json", mode="w", encoding="utf-8", delete=False
    ) as f:
        f.write(original)
        tmp_path = Path(f.name)
    try:
        changed = mod.append_header(tmp_path, "Test Author", "2026-05-10")
        assert not changed, "append_header returned True for a .json file — it must return False."
        result = tmp_path.read_text(encoding="utf-8")
        assert result == original, (
            f"append_header modified a .json file. Got:\n{result!r}\nExpected:\n{original!r}"
        )
    finally:
        tmp_path.unlink(missing_ok=True)
