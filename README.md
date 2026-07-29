# password-validator-ai-testing

Password validator built with Claude Code, with an AI-generated pytest suite audited and extended for boundary conditions and edge cases the AI missed on first pass.

## Audit process

The initial AI-generated test suite passed on a green run, but a passing suite only proves the tests that exist agree with the code — it says nothing about the tests that don't exist. I interrogated the generated suite against a 10-question checklist covering boundary conditions, input-type edge cases, rule isolation, and test-suite quality, then closed the real gaps it surfaced.

## Gaps found and fixed

| Gap Found | Why It Matters | Fix Added |
|---|---|---|
| No test for `None` / non-string input | Type mismatches crash instead of returning a clean `False`; without a test you don't know whether the function fails gracefully or throws unhandled in production | `test_none_input_raises_type_error` — documents that `validate_password(None)` raises `TypeError`, since the function has no type guard |
| Missing `test_only_uppercase_letters` (asymmetric with lowercase/digit/special-only tests) | Completes the single-character-class isolation matrix | `test_only_uppercase_letters` — asserts an all-uppercase password returns `False` |
| No test for whitespace-only input or leading/trailing whitespace on an otherwise-valid password | Whitespace-only strings pass a naive length check; whitespace handling was undocumented | `test_all_whitespace_password` (`False`) and three isolated leading/trailing/both-sides tests (`True`), confirming the function never strips input |
| No test for a special character outside the allowed set beyond a plain symbol (`?`) — specifically emoji | Confirms the special-character check is precise, not accidentally permissive; emoji raise real Unicode code-point edge cases | Single-codepoint and multi-codepoint (ZWJ family emoji) tests, both `False` |
| No test for a very long password or for performance at scale | Unbounded input is a classic source of performance bugs and an easy case for an AI to overlook | A 5,000-character valid-password test and a 50,000-character performance guard (must validate in under 1 second), protecting against a future refactor introducing quadratic behavior |
| Two tests testing the identical 7-character length boundary in different words, plus a combined-failure test isolating nothing | Near-duplicate tests inflate the count without adding coverage; a test failing multiple rules at once doesn't prove any single rule works | Removed both redundant/low-value tests, keeping the one deliberate boundary test |
| A whitespace test bundled 3 asserts into one function, so an early failure would mask the other cases | A failing assert stops a test immediately — bundled assertions hide whether later cases also break | Split into three separate, independently-reportable test functions |
| A test named for testing non-ASCII digits actually used a plain ASCII `0`, making it a duplicate of another test under a misleading name | A misleadingly named test gives false confidence a real edge case is covered when it isn't | Changed the password to use the Arabic-Indic digit U+0660, which `str.isdigit()` accepts despite not being ASCII 0-9 |

## Verifying the suite actually tests the logic (mutation testing)

Passing tests aren't proof the tests do anything. Commenting out the digit-check branch in `validate_password` and re-running pytest failed exactly the 12 tests that assert a valid password — confirming the suite genuinely exercises that rule rather than just agreeing with whatever the function outputs.
