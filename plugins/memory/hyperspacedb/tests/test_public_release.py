from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TEXT_EXTENSIONS = {".py", ".md", ".yaml", ".yml", ".toml", ".txt"}


def shipped_text():
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_EXTENSIONS:
            continue
        if "state" in path.parts:
            continue
        yield path, path.read_text(encoding="utf-8")


def test_no_private_identifiers_or_absolute_user_paths():
    forbidden = [
        "paulina" + "janowska", "anty" + "dizajn", "gniewka" + "_omniscient",
        "Gniew" + "islawa", "ANTI" + "GRAVITY", "/" + "Users/", "~/" + "AI/",
    ]
    failures = []
    for path, text in shipped_text():
        for token in forbidden:
            if token.lower() in text.lower():
                failures.append(f"{path.relative_to(ROOT)}: {token}")
    assert failures == []


def test_no_secret_assignments():
    pattern = re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"][^'\"]{8,}")
    failures = []
    for path, text in shipped_text():
        if pattern.search(text):
            failures.append(str(path.relative_to(ROOT)))
    assert failures == []


def test_manifest_declares_sdk_dependency():
    text = (ROOT / "plugin.yaml").read_text(encoding="utf-8")
    assert "hyperspacedb" in text
    assert "pip_dependencies" in text
