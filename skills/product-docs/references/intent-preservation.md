# Intent Preservation Check

Use this check before accepting a new or substantially rewritten requirements
authority. Read any selected raw user wording first, and keep external reference
material visibly separate.

## Keep The Records Distinct

| Record | Purpose | Boundary |
| --- | --- | --- |
| Direct wording | Preserve selected user decisions, values, examples, corrections, and unresolved tension | Not a full transcript or Agent summary |
| Current requirements | State the outcome and constraints that govern delivery now | Not architecture, task order, or transient status |
| External reference | Supply research, alternatives, risks, or implementation ideas | Not user intent or an adopted decision |
| Implementation candidate | Describe a possible route or experiment | Not a commitment or product fact |
| Adopted decision | Record a conclusion accepted through the repository's authority | Trace to the authority that adopted it |

## Questions

1. Could the user recognize the current requirement as their own demand without
   seeing the implementation discussion?
2. Does it preserve concrete priorities, examples, corrections, and tensions
   where they carry meaning?
3. Did architecture, framework, process fashion, or task planning displace the
   actual purpose?
4. Is direct user intent distinguishable from external research, advisor/AI
   suggestions, Agent interpretation, and adopted decisions?
5. Were conflicts resolved by the latest explicit user instruction?
6. Are genuinely open choices still open?
7. Does the interpreted body describe current truth instead of accumulating
   every historical debate?
8. If raw excerpts are kept, are selected quotations exact and attributable?
9. Was any deletion or curation of existing evidence authorized by the user,
   and does unique decision evidence remain recoverable?
10. Does the document fit the product's current lifecycle mode without turning
    a delivery or closure problem into a new product definition?

## Failure Signals

Rewrite the document if it mainly reads like any of the following:

- a technology stack choice or framework comparison;
- an external AI answer presented as user intent;
- a generic market or product pitch;
- a list of APIs, schemas, repositories, or interfaces;
- a sprint plan or transient status report;
- a chronological transcript whose obsolete debate obscures current intent;
- a clean abstraction that omits why the user cares;
- a completion claim based only on fixtures, file counts, or scaffolding.

## Translation Rule

Translate intent only after it is stable:

```text
direct user wording -> interpreted requirements -> product behavior ->
acceptance -> design/architecture -> delivery -> verification -> implementation
```

Downstream documents may refine how the system works. External references may
inform alternatives. Neither may silently rewrite what the user asked for.
