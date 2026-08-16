# Greenfield Initialization

## Contents

- [Quick Route](#quick-route)
- [Decide The Minimum Chain](#decide-the-minimum-chain)
- [Recovery And Sources](#recovery-and-sources)
- [Init Terminals](#init-terminals)
- [Verification And Rollback](#verification-and-rollback)

Use this route only when a repository is empty, newly initialized, or missing
an authority chain and the task includes repository setup. Do not replace a
working chain merely to match this reference.

## Quick Route

```text
scope and boundaries -> smallest authority chain -> recovery entry (when applicable)
-> acceptance and evidence -> optional architecture/design -> implementation
```

Read the full sections below only for the roles and risks that apply. Keep the
initial route summary in the active plan or status; do not create a second
requirements authority.

## Decide The Minimum Chain

1. Capture the latest direct user goal and unresolved questions before reading
   older history. Preserve product-specific wording in recovery evidence when
   that role exists; place general execution obligations in the active plan.
2. Identify whether the repository is public, private, or not yet decided.
   Separate source locators, source bodies, case mappings, provenance,
   derivatives, credentials, and authorized publication templates.
3. Map existing files before creating roles. Add only the smallest chain that
   can govern the requested outcome:

| Role | Add when | Keep out of it |
| --- | --- | --- |
| Authority index | More than one durable authority exists | New product decisions |
| Direct wording / recovery | User wording or corrections must remain recoverable | Full transcript or Agent summary |
| Requirements / intent | Current product outcome and constraints need interpretation | Task order or run status |
| Product behavior / PRD | Actors and observable behavior need a reusable contract | Storage or code layout |
| Acceptance | Success and failure must be observable | Test implementation details |
| Architecture / ownership | Durable data, security, recovery, or access boundaries matter | Product priority or phase estimates |
| Active plan / live status | Work has a route, terminal, next action, or evidence-backed progress | Product acceptance or full logs |
| Verification | Claims need repeatable checks or evidence pointers | New requirements |

Design or external-source registers are conditional roles. Combine roles when
authority, reader, and update cadence are genuinely shared; split only for a
durable independent boundary. Do not create empty placeholder files merely to
complete a template.

## Recovery And Sources

Add a bounded root recovery hook only when recovery safety is in scope and a
deep active-plan authority exists. The hook should name the goal/task-state API
first, link to the active plan second, and state that the linked authority owns
the lifecycle. It is navigation, not a second plan.

For public repositories, keep private source bodies, private locators, private
case mappings, and private provenance outside the repository unless a user
explicitly authorizes a reviewed safe template. Public, publishable locators
may remain when their publication is authorized and safe. A locator is not body
evidence. Use the source-evidence states defined in `governance-rules.md`; keep
them separate from runtime capability and usage outcome.

Do not promote any of these states to a product decision or a successful route
without the applicable evidence and authority. Keep a human review gate for
combinations of details that may make an otherwise de-identified case linkable.

## Init Terminals

Keep initialization dimensions separate and report the evidence for each:

| Dimension | Example terminal | Does not prove |
| --- | --- | --- |
| Documentation scaffold | Index, roles, links, and checks pass | Product acceptance |
| Local Git | Repository and intended branch exist | Remote publication |
| Remote | Remote exists and is authorized | Successful push |
| Publication | Push/readback succeeds | Real workflow proof |
| Real workflow | Authorized path works with a valid corpus | Human acceptance |
| Human acceptance | User accepts the result | Operational closure of future work |

Use explicit `success`, `partial`, `blocked`, `unavailable`, or `not-yet-probed`
states where applicable. Do not collapse initialization into one `complete`
flag.

## Verification And Rollback

Before claiming the scaffold is verified:

1. Resolve internal links and validate the authority index.
2. Check the recovery hook only inside its marker boundaries, accepting both LF
   and CRLF input.
3. Apply a temporary mutation that reverses the required API/Active Plan order
   and confirm the checker rejects it; discard the mutation after the check.
4. Scan public repository candidates for private locators, credentials, raw
   case material, and forbidden paths.
5. Record real command/API readback separately from file existence.

Run these checks in an isolated copy when possible. Keep the changes additive,
reviewable, and reversible; never delete historical wording or private source
evidence merely to make the initializer pass.
