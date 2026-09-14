import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_URL = "http://127.0.0.1:8000"


def request(method: str, path: str, payload: dict | None = None):
    url = f"{BASE_URL}{path}"

    headers = {
        "Accept": "application/json",
    }

    data = None

    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")

    request_object = Request(
        url,
        data=data,
        headers=headers,
        method=method,
    )

    with urlopen(request_object, timeout=5) as response:
        body = response.read().decode("utf-8")

        return response.status, json.loads(body)


def check_health() -> None:
    status, body = request("GET", "/healthz")

    if status != 200:
        raise RuntimeError(
            f"/healthz returned HTTP {status}: {body}"
        )

    if body.get("status") != "ok":
        raise RuntimeError(
            f"/healthz returned unexpected body: {body}"
        )

    print("[PASS] /healthz")


def check_readiness() -> None:
    status, body = request("GET", "/readyz")

    if status != 200:
        raise RuntimeError(
            f"/readyz returned HTTP {status}: {body}"
        )

    if body.get("status") != "ready":
        raise RuntimeError(
            f"/readyz returned unexpected body: {body}"
        )

    print("[PASS] /readyz")


def check_loans() -> None:
    status, body = request("GET", "/loans")

    if status != 200:
        raise RuntimeError(
            f"/loans returned HTTP {status}: {body}"
        )

    if not isinstance(body, list):
        raise RuntimeError(
            "/loans did not return a JSON list"
        )

    if len(body) < 5:
        raise RuntimeError(
            f"/loans returned only {len(body)} rows; expected at least 5"
        )

    print(f"[PASS] /loans returned {len(body)} rows")


def check_create_loan() -> None:
    payload = {
        "borrower_name": "Smoke Test Borrower",
        "loan_amount": 1500000,
        "property_city": "Lucknow",
        "status": "PENDING",
    }

    status, body = request(
        "POST",
        "/loans",
        payload,
    )

    if status != 201:
        raise RuntimeError(
            f"POST /loans returned HTTP {status}: {body}"
        )

    if not body.get("id"):
        raise RuntimeError(
            f"POST /loans did not return an ID: {body}"
        )

    if body.get("borrower_name") != payload["borrower_name"]:
        raise RuntimeError(
            f"POST /loans returned unexpected borrower: {body}"
        )

    print(
        f"[PASS] POST /loans created loan "
        f"{body['id']}"
    )


def main() -> int:
    print("LoanTrack API smoke test")
    print("=========================")

    checks = [
        check_health,
        check_readiness,
        check_loans,
        check_create_loan,
    ]

    try:
        for check in checks:
            check()

    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")

        print(
            f"[FAIL] HTTP {exc.code}: {body}",
            file=sys.stderr,
        )

        return 1

    except URLError as exc:
        print(
            f"[FAIL] Could not connect to API: {exc}",
            file=sys.stderr,
        )

        return 1

    except Exception as exc:
        print(
            f"[FAIL] {exc}",
            file=sys.stderr,
        )

        return 1

    print()
    print("All API smoke tests passed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())