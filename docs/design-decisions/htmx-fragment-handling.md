# Design Decision: Handling HTMX Fragments vs. Full Page Loads

## Context

When using HTMX for partial page updates, route handlers often need to return different responses based on whether the request is a standard full-page navigation (or refresh) versus an HTMX-triggered request targeting a specific DOM element (like the main content area).

## Problem

Implementing the logic to check request headers (`HX-Request`, `HX-Target`) and conditionally wrap the response content (either in a full page layout like `BaseLayout` or just the target container like `MainContentContainer`) within every relevant route handler leads to repetitive code (violating DRY) and increases the chance of inconsistencies.

## Decision: Use a Decorator for Conditional Rendering

We will use a Python decorator (`@render_htmx_fragment_or_full_page`) to encapsulate the logic for handling HTMX fragment requests versus full page loads.

## Implementation Details

1.  **Decorator Location:** `app/utils/decorators.py`
2.  **Functionality:**
    *   The decorator (`render_htmx_fragment_or_full_page`) accepts the `title` for the full page as an argument.
    *   It wraps the route handler function.
    *   Inside the wrapper, it calls the original route handler to get the main content elements.
    *   It inspects the incoming `request` headers (`HX-Request` and `HX-Target`).
    *   **If** it's an HTMX request targeting the main content area (`#main-content`), it wraps the content elements returned by the route handler in the `MainContentContainer` component and returns that fragment.
    *   **Else** (for full page loads), it wraps the content elements returned by the route handler in the full `BaseLayout` component, passing the `title` argument, and returns the complete page structure.
    *   It also includes basic handling to pass through non-standard responses (like redirects) returned by the route handler.

## Required Convention for Route Handlers

Route handlers intended to be used with this decorator **MUST** adhere to the following convention:

*   They should accept `request: Request` as their first argument.
*   They should **return only the FastHTML component(s)** intended to be placed *inside* the main content area (typically `<main id="main-content">`). This is often a tuple or list of components like `H1`, `P`, `Div`, `Form`, etc.
*   They **SHOULD NOT** return the `BaseLayout` or `MainContentContainer` themselves.

## Example Usage

```python
# app/main.py (or other route file)
from app.utils.decorators import render_htmx_fragment_or_full_page
from starlette.requests import Request

@rt("/some-page")
@render_htmx_fragment_or_full_page(title="Some Page Title")
async def handle_some_page(request: Request):
    # This function only generates the content for the main area
    page_content = (
        H1("Some Page Title"),
        P("Content specific to this page.")
    )
    return page_content
```

## Benefits

*   **DRY:** Avoids repeating header checks and layout logic in every route.
*   **Clean Routes:** Route handlers remain focused on generating page-specific content.
*   **Consistency:** Ensures a standard way of handling fragment vs. full page responses.
*   **Maintainability:** Changes to the layout logic only need to be made in the decorator and layout components.
