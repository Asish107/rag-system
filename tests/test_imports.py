import importlib

import pytest


@pytest.mark.parametrize(
    "module_name",
    [
        "rag.chunking",
        "rag.embeddings",
        "rag.loader",
        "rag.db",
        "rag.retrieval",
        "rag.rag",
        "rag.generate",
        "rag.remote_search",
        "rag.handlers.api",
        "rag.handlers.search",
        "rag.ingest",
    ],
)
def test_rag_module_imports(module_name):
    importlib.import_module(module_name)