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