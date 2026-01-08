---
description: "Ensuring feature parity and consistent design across JS, Python, and Rust SDKs."
name: "006-sdk-development"
applyTo: "**"
---

# SDK Development

Firecrawl maintains official SDKs for JavaScript, Python, and Rust.

## Goal: Feature Parity

Whenever a new feature is added to the API (e.g., a new scrape format or a new extract option), it MUST be added to all SDKs to maintain a consistent developer experience.

## SDK Directories

- `apps/js-sdk`: TypeScript/Node.js SDK.
- `apps/python-sdk`: Python SDK.
- `apps/rust-sdk`: Rust SDK.

## Design Principles

- **Idiomaticity**: While features should be consistent, the implementation should feel idiomatic to the language (e.g., use Pydantic in Python, Zod in JS, Serde in Rust).
- **Naming**: Use consistent parameter names across SDKs where possible (e.g., `scrapeOptions`, `pollInterval`).
- **Error Handling**: Provide clear, language-specific error messages that map to the API's error responses.
- **Authentication**: All SDKs must support the `fc-` prefixed API keys used by the authenticated API.

## Licensing

All SDKs are licensed under the **MIT License**. Ensure that any code or dependencies added to the SDK directories comply with this license.

## Testing SDKs

Each SDK has its own test suite.
- Ensure that integration tests against a real or mocked API are included for new features.
- Check the `README.md` in each SDK directory for language-specific testing instructions.

## Example: Adding a param to `scrape`

1. Update the API controller to accept and process the new parameter.
2. Update the `js-sdk` types and `scrape` method.
3. Update the `python-sdk` Pydantic models and `scrape` method.
4. Update the `rust-sdk` structs and `scrape` function.