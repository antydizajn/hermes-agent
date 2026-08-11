import inspect

from agent.memory_provider import MemoryProvider


def test_subclasses_current_hermes_memory_provider(plugin):
    assert issubclass(plugin.HyperspaceDBMemoryProvider, MemoryProvider)


def test_current_on_memory_write_signature(plugin):
    sig = inspect.signature(plugin.HyperspaceDBMemoryProvider.on_memory_write)
    assert list(sig.parameters)[:5] == ["self", "action", "target", "content", "metadata"]


def test_all_eight_tool_names_are_unique(provider):
    names = [s["name"] for s in provider.get_tool_schemas()]
    assert names == [
        "hyperspace_search", "hyperspace_store", "hyperspace_status",
        "hyperspace_graph", "hyperspace_hierarchy", "hyperspace_clusters",
        "hyperspace_search_advanced", "hyperspace_admin",
    ]
    assert len(names) == len(set(names))


def test_sync_turn_is_explicit_noop(provider, fake_client):
    provider.sync_turn("hello", "world", session_id="s")
    assert fake_client.points == {}
