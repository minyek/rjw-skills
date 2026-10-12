# Protocol and wire format

Choose the format from who reads it, where it runs, how much flows, and how it evolves.

- **Reader**: humans and agents reading text want a readable format; machines exchanging volume want a compact one. Many protocols want both: a binary wire with a readable debug rendering.
- **Locality**: on the same machine, prefer binary framing, shared memory or handle passing over serialising to text and back. Cross-host, weigh bandwidth, latency and schema evolution.
- **Volume and shape**: streams of small deltas, large blobs and tabular results each favour different encodings. Size the ceiling in bytes per second.
- **Evolution**: write the rules before the first release: how a field is added, deprecated and removed; tags or names are never reused; readers skip what they do not know; peers handshake on version.

JSON is one candidate among several, chosen when its readability or reach earns its cost. Binary formats are in bounds. Where the project has standard formats, start from them.
