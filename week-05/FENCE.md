# Week 5 — Concept fence

## Allowed

**Everything from weeks 1 to 4**, plus:

- `async def`, `await`, `async for`, async generators, `asyncio.run`,
  `@asynccontextmanager`
- `astream` with `updates`, `messages` and both; `aget_state`
- FastAPI: routes, Pydantic bodies, `HTTPException`, a lifespan, `StreamingResponse`
- Server-sent events
- `AsyncSqliteSaver`, and `AsyncPostgresSaver` in the deep track
- A Dockerfile and a compose file

## Not yet — and in another course

Authentication, rate limits, a public deployment, CI and alerts are Agent In
Production's subject. Here the server runs on your machine. WebSockets ·
background runs · horizontal scaling

---

## Why the customer id is in the body

A real server takes the customer from an authenticated session, never from what the
client sends. This one trusts the body because authentication is not this course's
subject — say so in your defence, and say what you would change.
