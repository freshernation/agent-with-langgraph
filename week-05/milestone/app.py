# Project 2 - start from your week-05/day-2/server.py. Four changes:
#
#   1. create_app(model, url, callbacks=None)
#      the lifespan opens checkpoints.checkpointer_for(url) - SQLite or Postgres,
#      decided by the setting.
#
#   2. config_for(customer, ticket_id, callbacks) -> dict
#      the thread, the callbacks, and the Langfuse user and session, as on
#      week 3 day 4. Every message and decision is run with it, so every trace
#      lands in the right session.
#
#   3. POST /tickets/{id}/messages refuses with 409 while the ticket is waiting
#      for a decision - the fix from the reference incident. (If your own
#      incident led to a different fix, add that too.)
#
#   4. from_environment() -> FastAPI
#      models.connect(), checkpoints.database_url(), and a Langfuse
#      CallbackHandler only if LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY are set.
#      This is what the Dockerfile's uvicorn --factory calls.
