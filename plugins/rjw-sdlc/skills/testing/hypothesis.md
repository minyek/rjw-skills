# Hypothesis recipes

Hypothesis is Python's property-based and stateful testing library. It runs under pytest or unittest.

```python
from hypothesis import given, settings, strategies as st
from hypothesis.stateful import RuleBasedStateMachine, invariant, rule
```

## Function or type property

Decorate the test with `@given(<strategy>)`; Hypothesis draws arguments from the strategies and shrinks a failure to a minimal case.

```python
# Behaviour: decoding an encoded ref name gives back the name, for every valid
# name. The oracle is the round-trip law, not a fixed string.
# Generator: lengths 0..255 straddle both bounds; the alphabet includes "/" and "."
# because they are the separators most likely to collide.
@given(st.text(alphabet="abc/.-_", min_size=0, max_size=255))
def test_ref_name_round_trips(name: str) -> None:
    assert decode_ref(encode_ref(name)) == name
```

Strategies to reach for: `st.integers(min_value=, max_value=)` with bounds that include the boundaries you care about, `st.sampled_from(...)` for every variant of a closed set, `st.lists(..., unique=True)` or duplicates on purpose, and `st.builds(Type, ...)` or `@st.composite` for structured values.

## Scenario or stateful property

A `RuleBasedStateMachine` draws a sequence of rules and checks every `@invariant` after **each** step, which localises the failing prefix.

```python
# Behaviour: across every put/delete/restart interleaving, no key is both
# tombstoned and present.
class DeletesStayDeleted(RuleBasedStateMachine):
    def __init__(self) -> None:
        super().__init__()
        self.store = Store()          # the real in-memory implementation, not a mock

    keys = st.sampled_from(["a", "b", "c"])   # few keys, so operations collide

    @rule(key=keys, value=st.integers())
    def put(self, key: str, value: int) -> None:
        self.store.put(key, value)

    @rule(key=keys)
    def delete(self, key: str) -> None:
        self.store.delete(key)

    @rule()
    def restart(self) -> None:
        self.store.restart()

    @invariant()
    def deleted_keys_are_absent(self) -> None:
        assert not (self.store.deleted & self.store.items.keys())


TestDeletesStayDeleted = DeletesStayDeleted.TestCase
TestDeletesStayDeleted.settings = settings(max_examples=50, stateful_step_count=10)
```

A failure prints the shrunk step sequence (`state.delete(key='b')`, `state.put(key='b', value=0)`, …), which is the reproducer. Keep key sets and step counts small so shrinking is fast.

## Settings, profiles and seeds

Set per-test limits with `@settings(max_examples=..., deadline=None)`. `deadline=None` keeps a slow, loaded machine from failing a functional test on elapsed time.

Project-wide profiles go in `conftest.py`:

```python
import os
from hypothesis import settings

settings.register_profile("dev", max_examples=50)
settings.register_profile("ci", max_examples=200, derandomize=True)
settings.register_profile("nightly", max_examples=2000)
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "dev"))
```

`derandomize=True` makes CI replayable. Hypothesis also saves failing examples in its example database (`.hypothesis/`) and replays them first on the next run. To pin one counterexample while you fix it, add the `@reproduce_failure(...)` decorator a failure prints when `print_blob=True` is set, or `@seed(<n>)`.
