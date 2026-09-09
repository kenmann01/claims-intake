# Claims Intake Service

A service that accepts a first notice of loss, validates it against the policy
master and the rule table in `docs/api-contract.md`, and either records a
notification and issues a claim reference or refuses the submission with a
specific reason.

## Working in this repository

You are inside a Linux container. Confirm it before you start:

```
uname -sm     # Linux aarch64
pwd           # /workspaces/claims-intake
```

Dependencies are installed when the container is created. There is no install
step in any assignment this week. If a tool you need is missing, that is a defect
in the image specification and should be reported rather than worked around.

## Running the service

```
uv run uvicorn claims.api.routes:app --reload
```

```
curl -s -X POST http://127.0.0.1:8000/notifications \
  -H "Content-Type: application/json" \
  -d '{"policy_number":"MOT-4471","loss_date":"2026-04-02","claim_type":"collision","estimated_amount":"4200.00"}'
# {"claim_reference":"CLM-2026-000001","status":"recorded"}
```

## Running the tests

```
uv run pytest
uv run ruff check .
uv run mypy
```

Unit tests mirror `src/claims/`. Integration tests in `tests/integration/`
exercise the HTTP surface end to end, against the fixtures in `data/`.

## Running in Docker

```
docker buildx build --platform linux/amd64 -t claims-intake .
docker run --rm -p 8000:8000 claims-intake
```

### Why `--platform linux/amd64`

A container image isn't machine code that runs anywhere — it's compiled for one
specific CPU family, the same way a program built for an ARM chip won't run on
an Intel one without a translator. Earlier in this README you confirmed your
dev container with `uname -sm` and probably saw `Linux aarch64` — that's ARM.
Plenty of us build on ARM machines: this dev container is one, and so is any
Apple Silicon Mac. But the servers this service actually gets deployed to,
along with most CI runners, are `amd64` (a.k.a. x86-64) machines.

`docker buildx build` defaults to building an image for whatever architecture
you're building _on_, not whatever you're building _for_. Build without the
flag on this ARM dev container and you get an ARM image. Ship that to an
amd64 server and it either refuses to start, or Docker quietly falls back to
emulating ARM instructions on the amd64 chip — which works, but runs far
slower and isn't actually exercising the same code path production will use.

Passing `--platform linux/amd64` tells buildx to cross-compile for amd64
regardless of the machine running the build command. That guarantees the
image you build on your laptop, in this dev container, or in CI is byte-for-byte
the same architecture as the one that will actually run in production.

## Where things are

| Path                         | What it holds                                                     |
| ---------------------------- | ----------------------------------------------------------------- |
| `docs/api-contract.md`       | What the service accepts, returns, and refuses. The authority.    |
| `docs/requirements-brief.md` | The open work items and their acceptance criteria.                |
| `docs/payload-triage.md`     | Your Day 1 classification of the edge payloads.                   |
| `data/`                      | Synthetic policies and notification payloads.                     |
| `src/claims/`                | The service.                                                      |
| `tests/`                     | Unit tests mirror `src/claims/`. Integration tests exercise HTTP. |
| `Dockerfile`                 | Builds the service image.                                         |

## Data

Everything in `data/` is synthetic and was authored for this program. It contains
no real client data and no named clients.
