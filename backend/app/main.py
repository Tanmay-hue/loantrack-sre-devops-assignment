import os
import socket
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status

from .database import (
    check_database_connection,
    close_pool,
    open_pool,
    pool,
)
from .schemas import LoanCreate, LoanResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    open_pool()

    yield

    close_pool()


app = FastAPI(
    title="LoanTrack API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    """
    Process health endpoint.

    This endpoint intentionally does not check PostgreSQL.
    """
    return {
        "status": "ok",
        "service": "loantrack-api",
    }


@app.get("/readyz")
def readyz() -> dict[str, str]:
    """
    Readiness endpoint.

    The service is ready only when PostgreSQL is reachable.
    """
    if not check_database_connection():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="database is not ready",
        )

    return {
        "status": "ready",
        "database": "reachable",
    }


@app.get("/loans", response_model=list[LoanResponse])
def list_loans() -> list[LoanResponse]:
    query = """
        SELECT
            id,
            borrower_name,
            loan_amount,
            property_city,
            status,
            created_at
        FROM loans
        ORDER BY id;
    """

    try:
        with pool.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to retrieve loans",
        ) from exc

    hostname = socket.gethostname()

    return [
        LoanResponse(
            id=row[0],
            borrower_name=row[1],
            loan_amount=row[2],
            property_city=row[3],
            status=row[4],
            created_at=row[5],
            served_by=hostname,
        )
        for row in rows
    ]


@app.post(
    "/loans",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_loan(loan: LoanCreate) -> LoanResponse:
    query = """
        INSERT INTO loans (
            borrower_name,
            loan_amount,
            property_city,
            status
        )
        VALUES (%s, %s, %s, %s)
        RETURNING
            id,
            borrower_name,
            loan_amount,
            property_city,
            status,
            created_at;
    """

    try:
        with pool.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        loan.borrower_name,
                        loan.loan_amount,
                        loan.property_city,
                        loan.status,
                    ),
                )

                row = cursor.fetchone()

            connection.commit()

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to create loan",
        ) from exc

    return LoanResponse(
        id=row[0],
        borrower_name=row[1],
        loan_amount=row[2],
        property_city=row[3],
        status=row[4],
        created_at=row[5],
        served_by=socket.gethostname(),
    )