"""Keep every test's notes and shop in their own throwaway files."""

import pytest


@pytest.fixture(autouse=True)
def notes_file(tmp_path, monkeypatch):
    path = tmp_path / "notes.json"
    monkeypatch.setenv("NOTES_FILE", str(path))
    return path


@pytest.fixture(autouse=True)
def shop_file(tmp_path, monkeypatch):
    path = tmp_path / "shop.json"
    monkeypatch.setenv("SHOP_FILE", str(path))
    return path
