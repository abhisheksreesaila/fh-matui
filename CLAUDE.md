# CLAUDE.md - Agent Instructions for fh-matui

## Project Overview

**fh-matui** is an nbdev-style notebook project that compiles into the `fh_matui` Python package. It provides Material Design UI components for FastHTML applications using BeerCSS.

### Philosophy
- **Low JavaScript**: Rely on HTMX for interactivity, minimize custom JS
- **High Fidelity**: Material Design components that look and feel native
- **Fast HTML**: Server-rendered components, no SPA overhead
- **Reusable**: Components designed for use across many projects

### Core Technologies
| Technology | Purpose |
|------------|---------|
| **FastHTML** | Python framework for building HTML with HTMX integration |
| **BeerCSS** | Material Design 3 CSS framework (CDN-based) |
| **nbdev** | Notebook-driven development - code in notebooks, compiles to Python |
| **HTMX** | Dynamic interactions without custom JavaScript |

---

## Project Structure

```
fh-matui/
├── nbs/                    # SOURCE NOTEBOOKS - EDIT HERE!
│   ├── 00_foundations.ipynb  # Base utilities (VEnum, stringify)
│   ├── 01_core.ipynb         # Theme, CSS helpers, constants
│   ├── 02_components.ipynb   # UI components (buttons, forms, etc.)
│   ├── 03_app_pages.ipynb    # Auth pages (LoginScreen)
│   ├── 04_web_pages.ipynb    # Landing page sections
│   ├── 05_datatable.ipynb    # Data tables with CRUD
│   └── index.ipynb           # Package documentation
│
├── fh_matui/               # COMPILED PYTHON - DO NOT EDIT DIRECTLY!
│   ├── foundations.py
│   ├── core.py
│   ├── components.py
│   ├── app_pages.py
│   ├── web_pages.py
│   └── datatable.py
│
├── _proc/                  # Processed notebooks (auto-generated)
├── _docs/                  # Generated documentation
├── settings.ini            # nbdev configuration
└── llms-ctx.txt            # LLM context file (API reference)
```

### CRITICAL: Edit Notebooks, Not Python Files
The Python files in `fh_matui/` are **auto-generated** from notebooks. Always edit the corresponding notebook in `nbs/` and run `nbdev_export` to update Python files.

---

## Module Reference

### foundations.py
Base utilities for string handling and enum support.

| Export | Purpose |
|--------|---------|
| `VEnum` | Enum base class with string concatenation support |
| `stringify(o)` | Convert lists/enums/values to space-separated strings |
| `normalize_tokens(cls)` | Flatten mixed inputs to token list |
| `dedupe_preserve_order(tokens)` | Remove duplicates, keep order |

### core.py
Theme configuration and CSS helper classes.

| Export | Purpose |
|--------|---------|
| `MatTheme.<color>.headers()` | Generate FastHTML headers with BeerCSS theme |
| `BeerCssChain()` | Chainable CSS class builder |
| `beer_hdrs` | Pre-configured BeerCSS CDN headers |
| `SIZES`, `COLORS`, `MARGINS`, etc. | BeerCSS utility class name lists |

**Theme Example:**
```python
# Dark mode with blue theme
hdrs = MatTheme.blue.headers(title="My App", mode="dark")
app = FastHTML(hdrs=hdrs)
```

### components.py
All UI components for building interfaces.

| Category | Components |
|----------|------------|
| **Buttons** | `ButtonT` (chainable styles: `.primary`, `.secondary`, `.destructive`, `.text`, `.ghost`) |
| **Links** | `AT` (anchor styles: `.button`, `.chip`, `.muted`, `.reset`) |
| **Layout** | `Grid`, `GridCell`, `DivHStacked`, `DivVStacked`, `DivCentered`, `DivFullySpaced` |
| **Navigation** | `NavBar`, `NavContainer`, `NavSideBarContainer`, `BottomNav` |
| **Forms** | `LabelInput`, `Select`, `SelectMenu`, `CheckboxX`, `Radio`, `Switch`, `TextArea`, `Range`, `Field`, `FormGrid` |
| **Modals** | `Modal`, `ModalButton`, `ModalTitle`, `ModalBody`, `ModalFooter`, `ModalCancel`, `ModalConfirm` |
| **Feedback** | `Toast`, `Snackbar`, `Progress`, `LoadingIndicator` |
| **Tables** | `Table`, `TableFromLists`, `TableFromDicts`, `Pagination` |
| **Cards** | `Card`, `Toolbar` |
| **Typography** | `TextT`, `TextPresets`, `CodeSpan`, `CodeBlock`, `Blockquote`, `Strong`, `Em`, `Small` |
| **Icons** | `Icon(name, size=None, fill=False)` |
| **Misc** | `FAQItem`, `CookiesBanner`, `Divider`, `Avatar` |

### app_pages.py
Pre-built pages and app shells for authenticated applications.

| Export | Purpose |
|--------|---------|
| `LoginScreen` | Split-screen OAuth login with customizable branding |
| `TopLayout` | Top-nav-only app shell with full-width content |
| `TopContent` | Wrap HTMX partial responses for TopLayout |

### web_pages.py
Landing page components for marketing sites.

| Export | Purpose |
|--------|---------|
| `HeroSection` | Full-width hero with CTAs |
| `FeaturesGrid` | Bento-style feature cards |
| `FeatureShowcase` | Alternating text/image rows |
| `PricingSection` | Pricing card with features |
| `FAQSection` | Expandable FAQ items |
| `PageFooter` | Multi-column footer |
| `LandingNavBar` | Sticky navigation bar |
| `LandingPage` | Complete landing page composition |

### datatable.py
Data tables with pagination, search, sorting, and CRUD operations.

| Export | Purpose |
|--------|---------|
| `DataTable` | UI-only paginated table (you handle routes) |
| `DataTableResource` | Full-stack CRUD: auto-registers routes, forms, save handlers |
| `CrudContext` | Rich context for CRUD hooks (request, user, db, record) |
| `table_state_from_request` | Extract pagination params from request |

**DataTableResource Example:**
```python
products = DataTableResource(
    app=app,
    base_route="/products",
    columns=[
        {"key": "name", "label": "Name", "searchable": True},
        {"key": "price", "label": "Price"}
    ],
    get_all=lambda req: db.products(),
    get_by_id=lambda req, id: db.products[id],
    create=lambda req, data: db.products.insert(data),
    update=lambda req, id, data: db.products.update(id, data),
    delete=lambda req, id: db.products.delete(id),
    title="Products"
)
# Auto-registers: GET /products, GET /products/action, POST /products/save
```

---

## Key Patterns

### Button Styles
```python
Button("Click", cls=ButtonT.primary)           # Filled primary
Button("Click", cls=ButtonT.secondary)         # Filled secondary
Button("Click", cls=ButtonT.destructive)       # Error/danger
Button("Click", cls=ButtonT.text)              # Text only
Button("Click", cls=ButtonT.ghost)             # Transparent
Button("Click", cls=ButtonT.primary.large)     # Chainable sizes
```

### Grid Layout
```python
# Responsive grid with automatic column calculation
Grid(
    Card("Item 1"),
    Card("Item 2"),
    Card("Item 3"),
    cols=3  # 3 columns on desktop, stacks on mobile
)

# Explicit spans
Grid(
    GridCell("Wide", span="s12 m6 l8"),
    GridCell("Narrow", span="s12 m6 l4")
)
```

### Forms
```python
# Floating label input
LabelInput(label="Email", id="email", input_type="email", prefix_icon="mail")

# Native select with HTMX
Select("Option A", "Option B", "Option C",
       name="choice", label="Select One",
       hx_get="/update", hx_trigger="change")

# Toggle switch
Switch("Dark Mode", name="dark_mode", checked=True)
```

### Modals
```python
# Trigger button + modal
Button("Open", data_ui="#my-modal"),
*Modal(
    ModalTitle("Confirm Action"),
    ModalBody("Are you sure?"),
    footer=ModalFooter(
        ModalCancel(modal_id="my-modal"),
        ModalConfirm(modal_id="my-modal")
    ),
    id="my-modal"
)
```

### TopLayout
```python
# Full-width app shell with top navigation
TopLayout(
    H3("Dashboard"), DashboardGrid(),
    nav_bar=NavBar(A("Home", href="/"), A("Dash", href="/dash"),
                   brand=H5("MyApp")),
)

# Route pattern — use TopContent for HTMX partials
@rt("/dashboard")
def get(req):
    page = DashboardGrid()
    if 'HX-Request' in req.headers:
        return TopContent(page)              # HTMX partial
    return TopLayout(page, nav_bar=my_navbar())  # Full page
```

### CSS Chaining
```python
# Build complex class strings safely
cls = BeerCssChain().small.primary.bold.round
str(cls)  # "small primary bold round"

# Use directly in components
Div("Content", cls=str(BeerCssChain().padding.center.elevate))
```

### HTMX Patterns
```python
# NavBar with SPA-style navigation
NavBar(
    A("Home", href="/"),
    A("About", href="/about"),
    hx_boost=True,          # Enable HTMX for all links
    hx_target="#main-content"  # Swap into main content area
)

# Route handler returning partial or full page
@rt("/dashboard")
def dashboard(req):
    content = DashboardContent()
    if 'HX-Request' in req.headers:
        return content  # HTMX: return partial
    return AppLayout(content)  # Full page: wrap in layout
```

---

## Development Workflow

### Build Commands
```bash
nbdev_export      # Compile notebooks to Python modules
nbdev_preview     # Preview documentation site
nbdev_test        # Run tests from notebooks
nbdev_clean       # Clean generated files
```

### Creating a New Component

1. **Choose the right notebook**: Most UI components go in `02_components.ipynb`

2. **Add export directive** at the top of the cell:
   ```python
   #| export
   def MyComponent(*c, cls='', **kwargs):
       """Brief description.

       Args:
           c: Children/content
           cls: Additional CSS classes
           **kwargs: Passed to underlying element
       """
       return Div(*c, cls=f"my-class {cls}", **kwargs)
   ```

3. **Add usage examples** in subsequent cells (without `#| export`):
   ```python
   # Example usage
   def ex_mycomponent():
       return MyComponent("Hello", cls="primary")

   preview(ex_mycomponent())
   ```

4. **Export and test**:
   ```bash
   nbdev_export
   ```

---

## Code Style Guidelines

### BeerCSS First
- Use BeerCSS native classes whenever possible
- Avoid custom CSS unless absolutely necessary
- Reference: https://www.beercss.com/

### Type-Safe Classes
```python
# Good: Use enums for autocomplete and typo prevention
Button("Click", cls=ButtonT.primary)
P("Text", cls=TextT.large)

# Avoid: Raw strings are error-prone
Button("Click", cls="primery")  # Typo won't be caught
```

### Composable Components
```python
# Good: Small, focused components
def UserCard(name, avatar_url):
    return Card(
        DivHStacked(
            Avatar(src=avatar_url),
            H4(name)
        )
    )

# Avoid: Monolithic components with many responsibilities
```

### HTMX Over JavaScript
```python
# Good: HTMX for interactions
Button("Load More",
       hx_get="/items?page=2",
       hx_target="#items-list",
       hx_swap="beforeend")

# Avoid: Custom JavaScript unless necessary
```

### Consistent Parameter Patterns
```python
# Follow FastHTML conventions
def MyComponent(
    *c,                    # Children/content (positional)
    cls: str = '',         # CSS classes
    **kwargs               # Pass-through to element
):
```

---

## Common BeerCSS Classes

### Sizing
`tiny`, `small`, `medium`, `large`, `extra`

### Colors
`primary`, `secondary`, `tertiary`, `error`, `surface`, `surface-container`

### Spacing
`padding`, `margin`, `no-padding`, `no-margin`, `small-padding`, `large-margin`

### Layout
`row`, `column`, `center`, `middle`, `wrap`, `no-wrap`

### Effects
`round`, `circle`, `elevate`, `blur`, `shadow`

### Typography
`bold`, `italic`, `uppercase`, `small-text`, `large-text`

---

## Troubleshooting

### Changes Not Appearing
1. Did you run `nbdev_export`?
2. Did you edit the notebook (not the .py file)?
3. Try restarting the Python kernel/server

### Import Errors
```python
# Full import (recommended)
from fh_matui.components import *

# Selective import
from fh_matui.core import MatTheme, BeerCssChain
from fh_matui.components import Grid, Card, Button, ButtonT
```

### Preview Not Working
Ensure you have a running FastHTML app in the notebook:
```python
app = FastHTML(hdrs=MatTheme.blue.headers())
server = JupyUvi(app, port=5000)
preview = partial(HTMX, app=app, port=5000)
```
