# LoanTrack

LoanTrack is a small three-tier loan management application built as part of
an SRE / DevOps technical assignment.

## Architecture

```text
+----------------------+
|      Browser         |
|   LoanTrack UI       |
+----------+-----------+
           |
           | HTTP
           v
+----------------------+
|   FastAPI Backend    |
|      :8000           |
+----------+-----------+
           |
           | PostgreSQL
           v
+----------------------+
|      PostgreSQL      |
|       :5432          |
+----------------------+

## Current development setup

## Database reliability

The backend uses a PostgreSQL connection pool instead of creating a new
database connection for every request.

During startup, the backend attempts to establish the database connection
multiple times with an increasing delay between attempts. This allows the
backend to recover when PostgreSQL takes longer to become available.

The API exposes two separate endpoints:

- `/healthz` checks whether the backend process is alive.
- `/readyz` checks whether the backend can reach PostgreSQL.

This separation is important for the later Kubernetes deployment because
liveness and readiness probes have different purposes.

## Startup behavior

If PostgreSQL is temporarily unavailable during backend startup, the backend
does not immediately terminate. It retries the connection using the configured
startup retry count and delay.

The retry settings are controlled through:

```text
DB_STARTUP_RETRIES
DB_STARTUP_RETRY_DELAY