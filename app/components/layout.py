from fasthtml.common import * # Bring in common components like Div, Nav, A, H1, Span

# Placeholder components for structure
def HeaderBar():
    """Placeholder for the top header bar (could contain Navbar later)."""
    # Using <header> semantic tag
    return Header(
        H4("App Header Area"),
        cls="container-fluid", # Use container-fluid for full width
        style="background-color: #f0f0f0; padding: 1rem;" # Basic inline style for visibility
    )

def Sidebar():
    """Placeholder for a potential sidebar."""
    # Using <aside> semantic tag
    return Aside(
        H5("Sidebar"),
        Ul(
            Li(A("Link 1", href="#")),
            Li(A("Link 2", href="#")),
        ),
        style="width: 200px; border-right: 1px solid #ccc; padding: 1rem;" # Basic inline style
    )

def MainContentContainer(*content):
    """Container for the main page content, targeted by HTMX."""
    # Using <main> semantic tag
    return Main(
        *content,
        Id="main-content", # Important: ID for HTMX targeting
        cls="container" # Standard Pico container for content centering/padding
    )

def BaseLayout(title: str, *main_content):
    """
    Constructs the full HTML page structure, including head and body.
    Uses the provided title and main content.
    """
    return (
        Title(title),
        Body(
            HeaderBar(),
            Div( # Flex container for sidebar + main
                Sidebar(),
                # MainContentContainer includes H1 now, so pass content directly
                MainContentContainer(*main_content),
                style="display: flex; flex-grow: 1;" # Basic flex layout
            )
            # Footer() could go here later
        )
    )