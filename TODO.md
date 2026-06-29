# TODO - DB SESSION INJECTION FIXED

- [x] Inspect get_db implementation and verify whether it returns a SQLAlchemy Session vs a context manager.
- [ ] Identify root cause of `AttributeError: '_GeneratorContextManager' object has no attribute 'query'`.
- [ ] Fix Factor Engine injection so `db` passed to services is a real SQLAlchemy Session.
- [ ] Update Factor Engine routes/services accordingly.
- [ ] Add/adjust DB helper in core/database.py if needed.
- [ ] Test Factor Engine routes (run backend + smoke test calls).
- [ ] Audit other modules listed for the same get_db misuse and fix everywhere.
- [x] Showcase documentation package created (docs/*).
- [ ] List all modified files at completion.


