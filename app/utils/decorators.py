import functools
from starlette.requests import Request
from fasthtml.common import *

# Assuming BaseLayout and MainContentContainer are accessible
# We might need to adjust imports based on final structure
from app.components.layout import BaseLayout, MainContentContainer

def render_htmx_fragment_or_full_page(title: str):
    """Decorator to return full BaseLayout or just MainContentContainer based on HTMX headers."""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # Call the original route handler to get the main content elements
            main_content_elements = await func(request, *args, **kwargs)

            # --- Handle Non-Standard Returns (e.g., Redirects) ---
            # Check if the route returned something other than FT elements (tuple, list, or single FT object)
            # This allows routes to return things like RedirectResponse directly.
            is_ft_content = False
            if isinstance(main_content_elements, (tuple, list)):
                # Assume it's content if it's a list/tuple (might need refinement if routes return other tuples/lists)
                is_ft_content = True
            elif hasattr(main_content_elements, '_name'): # Crude check for single FT element
                 is_ft_content = True
                 main_content_elements = (main_content_elements,) # Normalize single element to tuple

            if not is_ft_content:
                 # If the route returned something else (like a RedirectResponse), pass it through
                 return main_content_elements
            # --- End Non-Standard Return Handling ---

            # --- Check if it's an HTMX request targeting the main content ---
            is_htmx_target_request = (
                request.headers.get("HX-Request") == "true" and
                request.headers.get("HX-Target") == "main-content"
            )

            if is_htmx_target_request:
                # HTMX Fragment Request: Wrap the returned content elements in MainContentContainer
                return MainContentContainer(*main_content_elements)
            else:
                # Full Page Request: Wrap the returned content elements in the full BaseLayout
                return BaseLayout(title, *main_content_elements)
        return wrapper
    return decorator