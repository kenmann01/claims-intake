# Tool comparison

**Cursor** wrote the HTTP integration tests.

**Claude Code** wrote `POST /notifications`. This is a comparison of those two tasks, not a ranking of the tools in general.

## The split

- Claude Code implemented `src/claims/api/routes.py`: parse a first notice of loss, call `submit_notification`, and map every outcome to the section 5 envelope and the section 6 status. The file went from a bare `FastAPI()` stub to that mapping in one pass.

- Cursor implemented `tests/integration/test_notifications.py` and `tests/integration/conftest.py`. Those tests POST every payload in `data/fnol_valid.json`, `data/fnol_invalid.json`, and `data/fnol_edge.json`, plus a parse failure, an unknown field, a duplicate, and all three policy-master 5xx reasons. A later pass asserted the section 5 `detail` values, not only status and `code`.

## Claude Code on the endpoint

**What it made easy.** The handler is a translation. The contract had already decided 400 versus 422 versus 5xx, that FastAPI's own validation shape must not leak, that a `Decimal` in `detail` is a string, and that this layer holds no rule logic. Claude Code produced that mapping without a planning round-trip: hand-parsing `request.body()`, a `_STATUS_BY_CODE` table, `_jsonable` so money is not coerced to float, and `PolicyLookupFailed` left uncaught so this layer can tell timeout from unreachable from unparsable. That is the right shape of work for a spec that is already closed.

**What it made awkward.** The mapping was unproven until HTTP tests existed. Claude shipped the surface first. A `jsonable_encoder` float on `estimated_amount` would have looked fine in the file and been wrong for money; nothing in `routes.py` itself would have caught it. Claude Code also finished the layer — display `message` table, module-level singletons, helpers — rather than the smallest change that would turn a failing HTTP test green. Useful when the spec is complete. The wrong shape if the next step was supposed to be test-first.

## Cursor on the integration tests

**What it made easy.** The work is keeping three sources aligned: the `detail` keys in `docs/api-contract.md` section 5, the classification table in `docs/payload-triage.md`, and the payloads in `data/`. Cursor kept those open and drove tests off the fixture files instead of hand-copying bodies, so a fixture change is a test change. It also refused the assignment filename `test_routes.py` once `test_notifications.py` already covered the surface. Duplicating the suite would have been the obedient, worse outcome. The pass that asserted `detail` values (`rule`, dates, `limit`, `field`) is the kind of "the assignment named a gap, tighten this file" job Cursor is comfortable with. `conftest.py` wiring a fresh repository and policy client through `app.dependency_overrides` is the same kind of work: the failure mode is a test that leaks claim-reference state into the next one, and Cursor caught that.

**What it made awkward.** Cursor wanted a plan, a wait for `routes.py`, and a separate worktree before tightening assertions. That is ceremony on a test file. Integration tests cannot pass against a stub, so using Cursor for tests while Claude Code owned the handler meant the test tool was blocked on the other tool. Cursor is slower to just type the parametrize table. It spent attention on whether to create a second suite, and on process, that Claude Code would have spent writing the handler.

## When I would reach for which

I would reach for Claude Code when the decisions are already in the contract and the job is to implement a bounded mapping. `routes.py` is exactly that: parse, delegate, map. I would not open Cursor to write that handler. In this lab it answered a request to write tests by planning and waiting; asked to implement the endpoint it would have done the same.

I would reach for Cursor when the job is to pin that mapping against fixtures and a triage table. The failure mode is asserting the wrong thing, not failing to produce code. Claude Code as the test writer is how you get a second file named `test_routes.py` that restates payloads `data/` already holds, and how you get tests that check status and `code` and skip the `detail` keys a caller is actually allowed to rely on.

I would not swap them. Claude Code is the implementer of a closed spec. Cursor is the checker of that implementation against the documents that specified it.
