# Your Dockerfile, built from the TOP of the repository (compose says so).
#   - FROM python:3.12-slim, WORKDIR /app
#   - copy requirements.txt, pyproject.toml and the four packages (llm, desk,
#     models, shop) FIRST, then pip install - so changing your code does not
#     reinstall everything
#   - then copy week-05/milestone/ into /app - that is where app.py will live
#   - a user that is not root, owning /data, and USER it
#   - DATABASE_URL defaults to sqlite:////data/helpdesk.db (four slashes: an
#     absolute path)
#   - EXPOSE 8000, and run: uvicorn app:from_environment --factory
#     --host 0.0.0.0 --port 8000
