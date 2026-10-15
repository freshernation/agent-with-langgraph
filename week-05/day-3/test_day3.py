"""Week 5, Day 3 - a durable checkpointer, chosen by a setting, in a container.

Run me:  pytest week-05/day-3 -v

The container files are checked by reading them. Build them for real with
`docker compose -f week-05/day-3/compose.yaml up --build` once the milestone exists.
"""

import asyncio

import pytest


@pytest.fixture
def cp(load):
    return load("checkpoints.py")


def lines(source, name):
    kept = []
    for line in source(name).splitlines():
        if line.strip() and not line.strip().startswith("#"):
            kept.append(line)
    assert kept, f"{name} contains only comments so far - write it."
    return "\n".join(kept)


class TestTheSetting:
    def test_default(self, cp):
        assert cp.database_url({}) == "sqlite:///helpdesk.db"
        assert cp.database_url({"DATABASE_URL": "  "}) == "sqlite:///helpdesk.db"

    def test_from_the_environment(self, cp):
        assert cp.database_url({"DATABASE_URL": "postgresql://u:p@db/h"}) == "postgresql://u:p@db/h"

    @pytest.mark.parametrize("url,kind", [("sqlite:///x.db", "sqlite"), ("sqlite:////data/x.db", "sqlite"),
                                          ("postgresql://h/d", "postgres"), ("postgres://h/d", "postgres")])
    def test_kinds(self, cp, url, kind):
        assert cp.kind_of(url) == kind

    def test_anything_else(self, cp):
        with pytest.raises(ValueError):
            cp.kind_of("mysql://h/d")


class TestSqlite:
    def test_survives_closing(self, cp, tmp_path):
        url = f"sqlite:///{tmp_path / 'h.db'}"
        config = {"configurable": {"thread_id": "c1/T1", "checkpoint_ns": ""}}

        async def write():
            from langgraph.checkpoint.base import empty_checkpoint
            async with cp.checkpointer_for(url) as saver:
                checkpoint = empty_checkpoint()
                await saver.aput(config, checkpoint, {"step": 0}, {})
                return checkpoint["id"]

        async def read():
            async with cp.checkpointer_for(url) as saver:
                found = await saver.aget_tuple(config)
                return found.checkpoint["id"] if found else None

        written = asyncio.run(write())
        assert asyncio.run(read()) == written

    def test_uses_the_safe_serializer(self, cp, tmp_path):
        async def serde():
            async with cp.checkpointer_for(f"sqlite:///{tmp_path / 'h.db'}") as saver:
                return saver.serde
        assert ("classify", "Triage") in asyncio.run(serde())._allowed_msgpack_modules


class TestPostgres:
    def test_the_postgres_branch_is_taken(self, cp):
        async def connect():
            async with cp.checkpointer_for("postgresql://nobody:nothing@127.0.0.1:1/none"):
                pass
        with pytest.raises(Exception) as caught:
            asyncio.run(connect())
        assert "psycopg" in type(caught.value).__module__ or "connect" in str(caught.value).lower(), (
            "A Postgres URL should try to reach Postgres. This one failed some other way."
        )


class TestTheContainer:
    def test_dockerfile(self, source):
        text = lines(source, "Dockerfile")
        assert text.startswith("FROM python:3.12")
        assert text.index("pip install") < text.index("week-05/milestone"), (
            "Install the requirements before copying your code, or every change reinstalls everything."
        )
        assert "USER " in text and "0.0.0.0" in text and "--factory" in text

    def test_compose_keeps_secrets_out(self, source):
        text = lines(source, "compose.yaml")
        assert "/data" in text and "DATABASE_URL" in text
        assert "${ANTHROPIC_API_KEY}" in text and "sk-" not in text
        assert 'LANGSMITH_TRACING: "false"' in text

    def test_dockerignore(self, source):
        text = lines(source, ".dockerignore")
        for entry in (".env", ".venv", "instructor", ".db"):
            assert entry in text, f".dockerignore lets {entry} into the image."
