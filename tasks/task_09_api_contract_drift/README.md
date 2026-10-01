# API contract drift

An existing client was built against a baseline API contract. A newer server contract is considered compatible only when it preserves the guarantees that client relies on.

Implement:

`assert_compatible(expected, actual)`

Each contract contains:

- `method`
- `path`
- `request_required`
- `response_required`

Compatibility is directional:

- method and path must remain exactly the same;
- the server must not add a **new required request field** that the existing client does not send;
- the server must not remove a **required response field** the existing client expects;
- removing a request requirement is allowed;
- adding response fields is allowed.

Incompatible drift raises `ContractDriftError`.

The task intentionally models only required-field compatibility, not a complete OpenAPI diff engine.
