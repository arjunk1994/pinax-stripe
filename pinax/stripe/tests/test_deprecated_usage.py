from pathlib import Path


def _iter_runtime_python_sources():
    root = Path(__file__).resolve().parents[1]
    for path in root.rglob("*.py"):
        # skip tests and historical migrations
        if "tests" in path.parts or "migrations" in path.parts:
            continue
        yield path


def test_no_django_timezone_utc_usage_in_runtime_code():
    for path in _iter_runtime_python_sources():
        source = path.read_text(encoding="utf-8")
        assert "django.utils.timezone.utc" not in source


def test_no_decrypt_references_in_runtime_code():
    for path in _iter_runtime_python_sources():
        source = path.read_text(encoding="utf-8").lower()
        assert "decrypt" not in source
