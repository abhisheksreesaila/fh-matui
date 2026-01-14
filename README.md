
## What is fh-matui?

**fh-matui** is a Python library that brings Google's Material Design to [FastHTML](https://fastht.ml/) applications. It provides a comprehensive set of pre-built UI components that integrate seamlessly with FastHTML's hypermedia-driven architecture.

Built on top of [BeerCSS](https://www.beercss.com/) (a lightweight Material Design 3 CSS framework), fh-matui enables you to create modern, responsive web interfaces entirely in Python — no JavaScript required.

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🎨 **Material Design 3** | Modern, beautiful components following Google's latest design language |
| ⚡ **Zero JavaScript** | Build interactive UIs entirely in Python with FastHTML |
| 📱 **Responsive** | Mobile-first design with automatic breakpoint handling |
| 🌙 **Dark Mode** | Built-in light/dark theme support with 20+ color schemes |
| 🧩 **Composable** | Chainable styling APIs inspired by MonsterUI |
| 📊 **Data Tables** | Full-featured tables with pagination, search, sorting, and CRUD |
| 🔧 **nbdev-powered** | Literate programming with documentation built from notebooks |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        fh-matui                              │
├─────────────────────────────────────────────────────────────┤
│  Foundations     │  Core styling utilities, helpers, enums  │
│  Core            │  Theme system, MatTheme color presets    │
│  Components      │  Buttons, Cards, Modals, Forms, Tables   │
│  App Pages       │  Full-page layouts, navigation patterns  │
│  Data Tables     │  DataTable, DataTableResource for CRUD   │
│  Web Pages       │  Landing pages, marketing components     │
├─────────────────────────────────────────────────────────────┤
│  BeerCSS         │  Material Design 3 CSS framework         │
│  FastHTML        │  Python hypermedia web framework         │
└─────────────────────────────────────────────────────────────┘
```

## 🎨 Available Themes

fh-matui includes 15+ pre-configured Material Design 3 color themes:

| Theme | Preview | Theme | Preview |
|-------|---------|-------|---------|
| `MatTheme.red` | 🔴 | `MatTheme.pink` | 🩷 |
| `MatTheme.purple` | 🟣 | `MatTheme.deepPurple` | 💜 |
| `MatTheme.indigo` | 🔵 | `MatTheme.blue` | 💙 |
| `MatTheme.lightBlue` | 🩵 | `MatTheme.cyan` | 🌊 |
| `MatTheme.teal` | 🩶 | `MatTheme.green` | 💚 |
| `MatTheme.lightGreen` | 🍀 | `MatTheme.lime` | 💛 |
| `MatTheme.yellow` | 🌟 | `MatTheme.amber` | 🧡 |
| `MatTheme.orange` | 🟠 | `MatTheme.deepOrange` | 🔶 |

**Usage:**
```python
# Choose your theme
app, rt = fast_app(hdrs=[MatTheme.deepPurple.headers()])
```

## 🚀 Quick Start

Here's a minimal example to get you started:

```python
from fasthtml.common import *
from fh_matui.core import MatTheme
from fh_matui.components import Button, Card, FormField

# Create a themed FastHTML app
app, rt = fast_app(hdrs=[MatTheme.indigo.headers()])

@rt('/')
def home():
    return Div(
        Card(
            H3("Welcome to fh-matui!"),
            P("Build beautiful Material Design apps with Python."),
            Button("Get Started", cls="primary"),
        ),
        cls="padding"
    )

serve()
```

## 📦 Installation

```bash
pip install fh-matui
```

### Dependencies

fh-matui automatically includes:
- **python-fasthtml** - The core FastHTML framework
- **BeerCSS** - Loaded via CDN for Material Design 3 styling

### What This Code Does

1. **`MatTheme.indigo.headers()`** - Loads BeerCSS with the indigo color scheme
2. **[`Card`](https://abhisheksreesaila.github.io/fh-matui/components.html#card)** - Creates a Material Design card component with elevation
3. **[`FormField`](https://abhisheksreesaila.github.io/fh-matui/components.html#formfield)** - Generates a styled input with floating label
4. **`Button`** - Renders a Material Design button with ripple effects

## 📚 Module Reference

| Module | Description | Key Components |
|--------|-------------|----------------|
| [Foundations](https://abhisheksreesaila.github.io/fh-matui/foundations.html) | Base utilities and helper functions | `BeerHeaders`, `display`, styling helpers |
| [Core](https://abhisheksreesaila.github.io/fh-matui/core.html) | Theme system and styling | `MatTheme`, color presets, theme configuration |
| [Components](https://abhisheksreesaila.github.io/fh-matui/components.html) | UI component library | `Button`, `Card`, `FormField`, `FormModal`, `Grid` |
| [App Pages](https://abhisheksreesaila.github.io/fh-matui/app_pages.html) | Application layouts | Navigation, sidebars, full-page layouts |
| [Data Tables](https://abhisheksreesaila.github.io/fh-matui/datatable.html) | Data management components | `DataTable`, `DataTableResource`, CRUD operations |
| [Web Pages](https://abhisheksreesaila.github.io/fh-matui/web_pages.html) | Marketing/landing pages | Hero sections, feature grids, testimonials |

## 🛠️ Development

### Install in Development Mode

```bash
# Clone the repository
git clone https://github.com/user/fh-matui.git
cd fh-matui

# Install in editable mode
pip install -e .

# Make changes under nbs/ directory, then compile
nbdev_prepare
```

## 🤝 Why fh-matui?

| Challenge | fh-matui Solution |
|-----------|-------------------|
| **CSS complexity** | Pre-built Material Design 3 components via BeerCSS |
| **JavaScript fatigue** | FastHTML handles interactivity declaratively |
| **Component consistency** | Unified API across all components |
| **Dark mode support** | Built-in with automatic system preference detection |
| **Responsive design** | Mobile-first grid system and responsive utilities |
| **Form handling** | [`FormField`](https://abhisheksreesaila.github.io/fh-matui/components.html#formfield), [`FormGrid`](https://abhisheksreesaila.github.io/fh-matui/components.html#formgrid), [`FormModal`](https://abhisheksreesaila.github.io/fh-matui/components.html#formmodal) for rapid form building |
| **Data management** | [`DataTable`](https://abhisheksreesaila.github.io/fh-matui/table.html#datatable) and [`DataTableResource`](https://abhisheksreesaila.github.io/fh-matui/table.html#datatableresource) for CRUD operations |

## 📄 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](https://github.com/user/fh-matui/blob/main/LICENSE) file for details.

---

**Built with ❤️ using FastHTML and nbdev**