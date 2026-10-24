# Structure And Topology

Read when a design fixes persistence, cross-service parameter names, or repository
topology. These are the decisions that survive a rewrite and cost the most to
change later; they are recorded once, at the architecture authority.

## Storage And Persistence

Decide each of these explicitly rather than by default: whether a database is
needed at all, whether state lives locally or remotely, and which layer owns the
cache. For each, name the source of truth, what is derived from it, and what the
system does when the store is unavailable. "We will add persistence later" is a
decision to re-derive every identifier on restart; write it down as such.

## Runtime Data From The Source

Runtime data is built in memory from the single handwritten source. No second
generated copy is committed, served, or treated as authority. A cache is
acceptable when it is rebuildable, versioned, and cannot be mistaken for the
source; anything else is a second truth that will drift.

## Parameter Naming Across Services

One name per parameter, used identically by every service, script, and deployment
surface. A second name for the same value is a second source of truth: the day one
of them changes, the failure appears as a configuration bug in an unrelated
component.

## Repository Topology

Record which repositories exist, who consumes whom, what each exposes, and how
cross-repository paths are parameterized. A path copied between repositories is a
hardcoded assumption waiting to break on the next machine.

## Optional Practice: Position-Prefixed Names

Example, not a rule. Names that carry their position (`c01-`, `c02-`, `p1-`) keep
order and gaps readable at a glance, and make a deleted item visible as a hole
rather than a silent renumbering. Adopt it where assets or parts are ordered; do
not impose it on code identifiers, where the language's own conventions decide.
