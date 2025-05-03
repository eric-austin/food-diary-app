# Project Structure

This document outlines the organization of the Food Diary App codebase.

## Directory Structure

```
/
├── docs/                        # Project documentation
│   ├── architecture.md          # Architecture decisions and diagrams
│   ├── requirements.md          # Project requirements
│   ├── api/                     # API documentation
│   ├── database/                # Database schema documentation
│   └── deployment/              # Deployment guides
├── app/                         # Application source code
│   ├── main.py                  # Application entry point
│   ├── config.py                # Configuration management
│   ├── database.py              # Database connection and setup
│   ├── models/                  # Database models
│   │   ├── user.py              # User model
│   │   ├── food_entry.py        # Food diary entry model
│   │   └── image.py             # Image storage model
│   ├── components/              # Reusable UI components
│   │   ├── forms.py             # Form components
│   │   ├── layout.py            # Layout components
│   │   └── food_item.py         # Food entry components
│   ├── routes/                  # Route handlers (primarily HTML/HTMX views)
│   │   ├── auth.py              # Authentication routes
│   │   ├── users.py             # User management routes
│   │   ├── food_diary.py        # Food diary entry routes
│   │   └── images.py            # Image upload and processing routes
│   ├── api/                     # Route handlers (primarily JSON data APIs)
│   │   ├── auth.py              # e.g., /api/auth/register, /api/auth/login
│   │   ├── entries.py           # e.g., /api/entries
│   │   └── users.py             # e.g., /api/users/me
│   ├── services/                # Business logic services
│   │   ├── auth.py              # Authentication service
│   │   ├── food_recognition.py  # AI food recognition service
│   │   └── image_storage.py     # Image storage service
│   ├── static/                  # Static assets
│   │   ├── css/                 # CSS stylesheets
│   │   ├── js/                  # JavaScript files (optional)
│   │   └── images/              # Static images
│   ├── views/                   # Page views and templates
│   │   ├── base.py              # Base view functions
│   │   ├── auth/                # Authentication views
│   │   ├── user/                # User profile views
│   │   └── food_diary/          # Food diary views
│   ├── utils/                   # Utility functions and decorators
│   │   └── decorators.py        # Custom decorators
│   └── data/                    # Data storage (for SQLite if used)
├── tests/                       # Test suite
│   ├── test_routes/             # Route handler tests
│   ├── test_services/           # Service tests
│   └── test_models/             # Model tests
├── migrations/                  # Database migrations (if using SQLAlchemy)
├── .env.example                 # Example environment variables
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
└── README.md                    # Project overview
```

## Key Files and Their Responsibilities

### Configuration and Setup
- `main.py`: Application entry point, FastHTML app initialization
- `config.py`: Environment variables and configuration management
- `database.py`: Database connection setup

### Data Layer
- `models/`: Database models for ORM or direct database interfaces
- `data/`: SQLite database storage (if using SQLite)

### Business Logic
- `services/`: Core business logic separated from route handlers
- `routes/`: HTTP route handlers that connect URLs to view functions

### Presentation Layer
- `components/`: Reusable FastHTML FastTags components
- `views/`: Page-level view functions that return complete pages
- `static/`: CSS and static assets

## Code Organization Principles

1. **Separation of Concerns**
   - Models handle data structure
   - Services handle business logic
   - Routes handle request routing
   - Components and views handle presentation

2. **Modularity**
   - Each feature area has its own set of models, routes, and views

3. **Testability**
   - Business logic in services can be tested independently
   - Route handlers have dedicated tests

4. **Configuration Management**
   - Environment-specific configuration via environment variables
   - Secrets never stored in code

## Development Guidelines

- Follow FastHTML conventions for component-based UI construction
- Use FastTags for HTML generation rather than string templates
- Keep components small and focused on a single responsibility
- Use HTMX attributes for dynamic interactions
- Minimize JavaScript, using only when necessary 