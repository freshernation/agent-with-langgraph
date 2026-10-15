# Day 3 - a checkpointer chosen by a setting, not by the code.
#
# Copy your week 3 milestone's durable.py (for serializer()).
#
#   DEFAULT_URL = "sqlite:///helpdesk.db"
#
#   database_url(env=None) -> str
#       env defaults to os.environ. DATABASE_URL, stripped - or DEFAULT_URL if it
#       is missing or blank.
#
#   kind_of(url) -> "sqlite" | "postgres"
#       sqlite:/// for SQLite; postgresql:// or postgres:// for Postgres. Anything
#       else: ValueError saying what it must start with.
#
#   checkpointer_for(url)       an async context manager (@asynccontextmanager)
#       sqlite:   aiosqlite.connect(<the path after sqlite:///>), and yield an
#                 AsyncSqliteSaver(connection, serde=serializer())
#       postgres: from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
#                 (import it here, so SQLite users never need the driver);
#                 AsyncPostgresSaver.from_conn_string(url, serde=serializer()),
#                 await saver.setup() - it creates its tables - and yield it.
#
# Then write the Dockerfile, compose.yaml and .dockerignore beside this file.
