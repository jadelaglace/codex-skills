# Intent Preservation

Use this reference before accepting a new or substantially rewritten current
requirements authority.

## Distinguish The Records

| Record | Purpose | Boundary |
| --- | --- | --- |
| Direct wording | Preserve selected user decisions, values, examples, corrections, and unresolved tension | Do not turn it into a full transcript or Agent summary |
| Current requirements | State the outcome and constraints that govern delivery now | Do not accumulate obsolete debate, implementation plans, or transient status |
| External reference | Supply research, alternatives, risks, or implementation ideas | Do not attribute it to the user or treat it as adopted |
| Adopted decision | Record a conclusion accepted through the repository's decision authority | Trace it to the authority that adopted it |

## Maintain Current Truth

1. Read the latest direct user statement and any selected raw evidence relevant
   to the change.
2. Compare it with the current requirements rather than appending blindly.
3. Resolve conflicts in favor of the latest explicit instruction. Keep choices
   open when the user has not decided them.
4. Preserve concrete priorities and tensions when removing them would narrow or
   sanitize what the user wants.
5. Keep exact quotations attributable. Curate existing unique raw evidence only
   with user authorization.
6. Rewrite the interpreted body as current truth; retain history only where it
   helps recover intent or explain an active constraint.

## Acceptance Check

- Could the user recognize the requirement as their own demand without reading
  the implementation discussion?
- Does it preserve why the outcome matters, not only a clean abstraction?
- Are direct wording, Agent interpretation, external advice, and adopted
  decisions visibly distinct?
- Did architecture, tooling, planning, or framework fashion displace the
  product purpose?
- Are current priorities and genuinely unresolved choices accurate?
- Is low-signal history kept out of the main reading path while unique decision
  evidence remains recoverable?

Reject a requirements rewrite that mainly reads like a technology stack, API or
file inventory, sprint plan, generic product pitch, external AI answer, or
chronological transcript.

Use this authority direction:

```text
direct user wording -> current requirements -> product behavior -> acceptance
-> architecture/design -> plan/progress -> verification -> implementation
```

Downstream records may interpret intent. They may not silently rewrite it.
