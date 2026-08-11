import importlib.util
from pathlib import Path
import subprocess
import re
import sys
import types

import pytest
import yaml

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


def test_provider_has_no_dead_trusted_sources_policy():
    source = (ROOT / "__init__.py").read_text(encoding="utf-8")
    assert "trusted_sources" not in source


def test_readme_documents_hmac_environment_boundary():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "ownership_hmac_key_env" in text
    assert "do not put the key in a public configuration file" in text


def test_manifest_version_and_dependency_contract_match_readme():
    manifest = yaml.safe_load((ROOT / "plugin.yaml").read_text(encoding="utf-8"))
    assert re.fullmatch(r"\d+\.\d+\.\d+", str(manifest["version"]))
    dependency = manifest["pip_dependencies"][0]
    assert dependency.startswith("hyperspacedb>=") and ",<" in dependency
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert f"Version {manifest['version']}" in text
    assert dependency in text


def test_e2e_runner_requires_explicit_approval_and_test_hmac_before_client_creation():
    text = (ROOT / "tests" / "run_test_collection_e2e.py").read_text(encoding="utf-8")
    assert "HSDB_E2E_WRITE_APPROVED" in text
    assert "HSDB_TEST_OWNERSHIP_HMAC_KEY" in text
    assert "HSDB_E2E_STATE_PATH" in text
    assert "hsdb_e2e_" in text
    assert text.index('approval != "approved"') < text.index("client = HyperspaceClient")
    assert text.index('state_path = require_external_state_path') < text.index("client = HyperspaceClient")


def _load_e2e_runner(monkeypatch):
    fake_hyperspace = types.ModuleType("hyperspace")
    fake_hyperspace.HyperspaceClient = object
    module_name = "hyperspace_e2e_runner_under_test"
    monkeypatch.setitem(sys.modules, "hyperspace", fake_hyperspace)
    monkeypatch.delitem(sys.modules, module_name, raising=False)
    runner_path = ROOT / "tests" / "run_test_collection_e2e.py"
    spec = importlib.util.spec_from_file_location(module_name, runner_path)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, module_name, module)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("state_path", ["", "relative/ledger.sqlite3"])
def test_e2e_state_path_guard_rejects_empty_or_relative_path(monkeypatch, state_path):
    runner = _load_e2e_runner(monkeypatch)
    with pytest.raises(SystemExit):
        runner.require_external_state_path(state_path)


def test_e2e_state_path_guard_rejects_path_under_plugin_root(monkeypatch):
    runner = _load_e2e_runner(monkeypatch)
    with pytest.raises(SystemExit):
        runner.require_external_state_path(str(ROOT / "state" / "e2e.sqlite3"))


def test_e2e_state_path_guard_accepts_absolute_external_path(monkeypatch):
    runner = _load_e2e_runner(monkeypatch)
    external = ROOT.parent / "e2e-runtime" / "ledger.sqlite3"
    assert Path(runner.require_external_state_path(str(external))) == external.resolve()


def test_tracked_release_manifest_excludes_runtime_artifacts():
    repository = ROOT.parents[2]
    prefix = "plugins/memory/hyperspacedb"
    output = subprocess.check_output(
        ["git", "ls-files", "--", prefix], cwd=repository, text=True
    )
    tracked = [line for line in output.splitlines() if line]
    assert f"{prefix}/__init__.py" in tracked
    assert f"{prefix}/README.md" in tracked
    assert f"{prefix}/plugin.yaml" in tracked
    assert not any("/state/" in path for path in tracked)
    assert not any(path.endswith((".sqlite3", ".pyc")) for path in tracked)


def test_e2e_runner_never_defaults_its_ledger_into_plugin_state():
    text = (ROOT / "tests" / "run_test_collection_e2e.py").read_text(encoding="utf-8")
    assert '"state_path": state_path' in text
    assert 'ROOT / "state"' not in text
