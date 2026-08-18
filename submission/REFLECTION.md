# Lab 18 — Reflection: Top 5 Lakehouse Anti-Patterns

**Riskiest anti-pattern for our team: lifecycle skew between the lakehouse and an external index** — exactly what NB7 reproduces.

We sync embeddings out to a vector index for latency, but most sync jobs are upsert-only. When a row is deleted from the lakehouse, nothing tells the index to forget it. The lakehouse looks clean; the index keeps serving the deleted content indefinitely. That is invisible until an audit or a GDPR/CCPA erasure request surfaces it — at which point it is a compliance violation, not a bug ticket.

It is also the hardest of the five anti-patterns to catch in review, because both systems report healthy independently. Small-file sprawl or missing Z-ORDER show up as slow queries; skew shows up as nothing, until someone asks "is this data really gone?"

**Mitigation:** treat the lakehouse as the sole system of record for deletes. Subscribe external indices to Change Data Feed deletes rather than re-running upsert-only syncs, and add a periodic reconciliation job that diffs index membership against current table state.

---

*Lab18 Track 2 | Lakehouse Architecture | VinUniversity AICB*
