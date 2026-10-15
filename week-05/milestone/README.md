# Week 5 Milestone — Project 2: Helpdesk as a service

> Streaming over HTTP, durable through a restart, traced per ticket, in a container.

---

## The files

| File | Where it comes from |
|---|---|
| your week 3 milestone files | **copy** |
| `streaming.py`, `checkpoints.py`, `costs.py` | **copy from this week's days** |
| `Dockerfile`, `.dockerignore`, `compose.yaml` | **copy from day 3** (compose points at this folder's Dockerfile) |
| `app.py` | day 2's server, grown up |
| `INCIDENT.md` | **copy from day 4** |

## Run it

```bash
docker compose -f week-05/milestone/compose.yaml up --build
curl -N -X POST localhost:8000/tickets/T02/messages \
     -H 'content-type: application/json' -d '{"customer": "c1", "text": "My kettle broke, refund A1001"}'
curl -N -X POST localhost:8000/tickets/T02/decision \
     -H 'content-type: application/json' -d '{"customer": "c1", "action": "approve"}'
```

---

## Check it

```bash
pytest week-05/milestone -v
```

## Friday

The defence restarts your container while a refund is waiting.
