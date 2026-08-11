from pathlib import Path
import subprocess
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


def test_readme_discloses_no_automatic_mutation_replay():
    text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    assert "does not replay failed `add` or `replace`" in text
    assert "does not claim automatic eventual consistency" in text


def test_runtime_artifacts_are_ignored_without_deleting_them():
    ignored = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "/state/" in ignored
    assert "*.sqlite3" in ignored
    probe = subprocess.run(
        ["git", "check-ignore", "-q", "state/example/ledger.sqlite3"],
        cwd=ROOT,
        check=False,
    )
    assert probe.returncode == 0


def test_readme_discloses_plaintext_ledger_and_permission_boundary():
    text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    assert "plaintext memory content" in text
    assert "mode `0700`" in text
    assert "mode `0600`" in text
    assert "not encryption at rest" in text


def test_readme_matches_collection_contract_configuration():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "`expected_dimension`" in text
    assert "`trusted_sources`" not in text


def test_readme_documents_hmac_environment_boundary():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "ownership_hmac_key_env" in text
    assert "do not put the key in a public configuration file" in text
