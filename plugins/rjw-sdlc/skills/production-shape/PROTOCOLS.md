# Protocol and wire format

Choose the format from who reads it, where it runs, how much flows, and how it evolves.

- **Reader**: humans and agents reading text want a readable format; machines exchanging volume want a compact one. Many protocols want both: a binary wire with a readable debug rendering.
- **Locality**: on the same machine, prefer binary framing, shared memory or handle passing over serialising to text and back. Cross-host, weigh bandwidth, latency and schema evolution.
- **Volume and shape**: streams of small deltas, large blobs and tabular results each favour different encodings. Size the ceiling in bytes per second.
- **Evolution**: choose the protocol's evolution level and write its rules before the first release (see [EVOLUTION.md](EVOLUTION.md)).

JSON is one candidate among several, chosen when its readability or reach earns its cost. Binary formats are in bounds. Where the project has standard formats, start from them.
