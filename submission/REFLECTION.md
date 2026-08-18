# Lab 18 — Reflection: Top 5 Lakehouse Anti-Patterns

## Most Risky Anti-Pattern for Our Team: **Lifecycle Skew Between Lakehouse and External Index**

After completing this lab, the most dangerous pattern we would likely encounter is **syncing embeddings/vectors to an external index without subscribing to deletes**—exactly what NB7 demonstrates.

### Why This Is the Biggest Risk:

1. **Compliance Liability** — Once a data subject exercises their right to erasure (GDPR, CCPA), deleting from the lakehouse is mandatory. An out-of-sync external index that still returns erased content becomes a legal violation instantly.

2. **Silent Data Leakage** — Unlike a crashed pipeline, lifecycle skew is *invisible*. The lakehouse is clean, but the vector index happily returns sensitive data until the next "sync" — which might never happen if sync is one-way upsert.

3. **Harder to Fix Than It Looks** — Rebuilding the entire index from scratch is expensive. Change Data Feeds (CDF) are the answer, but many pipelines skip them because they add complexity.

4. **Affects All Multimodal AI** — As models grow larger and multimodal RAG becomes standard, this pattern scales from "one embarrassing incident" to "enterprise-wide exposure."

### Our Mitigation Strategy:

- Store embeddings *in the table* whenever possible (cost permitting).
- For external indices: subscribe to CDF deletes, not guessing from upsert-only syncs.
- Audit sync pipeline contracts quarterly, especially before feature launches.

**Lesson:** The system-of-record must own the delete contract. Everything else is just a cache.

---

*Lab18 Track 2 | Lakehouse Architecture | VinUniversity AICB*
