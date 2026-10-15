# Day 2 - Helpdesk behind HTTP, streaming.
#
# Copy your week 3 milestone files and day 1's streaming.py.
#
#   class MessageIn(BaseModel):   customer: str (not empty)   text: str (1 to 4000 characters)
#   class DecisionIn(BaseModel):  customer: str (not empty)
#                                 action: "approve" | "reject" | "edit"
#                                 amount: float | None = None   note: str = ""
#
#   sse(event, data) -> str
#       one server-sent event: "event: <event>\ndata: <json.dumps(data)>\n\n"
#       (JSON, so a token with a newline in it cannot break the stream)
#
#   thread(customer, ticket_id) -> {"configurable": {"thread_id": "<customer>/<ticket_id>"}}
#
#   create_app(model, db_path) -> FastAPI
#       A lifespan that opens aiosqlite.connect(db_path), makes an
#       AsyncSqliteSaver(connection, serde=durable.serializer()), builds Helpdesk
#       with it into app.state.graph, and yields. (A server is async, so its
#       checkpointer is too.)
#
#       GET  /health                        {"status": "ok"}
#       POST /tickets/{ticket_id}/messages  MessageIn -> a StreamingResponse,
#                                           media_type "text/event-stream", of
#                                           sse() for every event from
#                                           streaming.events
#       GET  /tickets/{ticket_id}?customer= {"next": [...], "reply": ..., "waiting": [values]}
#                                           404 if the thread has no state
#       POST /tickets/{ticket_id}/decision  DecisionIn -> 409 if nothing is waiting;
#                                           422 for an edit with no amount; otherwise
#                                           resume with Command(resume={action, note,
#                                           and amount if given}) and stream it like
#                                           a message.
