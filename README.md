# GitEyes

Welcome to **GitEyes** - Transform GitHub documentation into interactive, book-like reading experiences!

GitEyes is an educational project that provides a clean, distraction-free interface for browsing, reading, and interacting with documentation hosted on GitHub repositories. It's perfect for studying codebases and technical documentation with enhanced readability.

![GitEyes Logo](/src/giteyes/static/images/giteyes-logo.svg)

## 📚 Project Overview

GitEyes offers:

- **GitHub Content Transformation:** Converts repository documentation into a readable book format
- **Tree Navigation:** Intuitive navigation through repository file structures
- **Markdown Rendering:** Beautiful rendering of markdown files with syntax highlighting
- **Search Functionality:** Find specific content across multiple repositories
- **Bookmarking:** Save your favorite documentation for quick access
- **Dark/Light Mode:** Toggle between reading modes for comfortable viewing

## 🌟 Live Example

Try viewing this popular Data Engineering resource with GitEyes for a more comfortable reading experience:

[Data Engineering Cookbook by Andreas Kretz](http://127.0.0.1:8000/view/andkret/Cookbook/blob/master/README.md)

## ⚙️ Current Implementation

1. **Core Features:**
   - Repository parsing and content extraction
   - Hierarchical navigation of documentation
   - Markdown to HTML conversion with enhanced styling
   - Dark/Light mode for comfortable reading
   - Progress tracking across documents

2. **Web Interface:**
   - FastAPI backend with Jinja2 templates
   - Responsive design for desktop and mobile reading
   - Clean, distraction-free reading experience
   - Customizable font size and reading preferences

## 🛠 Technology Stack

- **Backend:**
  - Python 3.10+
  - FastAPI for the web framework
  - Requests library for HTTP operations
  - BeautifulSoup for HTML parsing (when needed)

- **Frontend:**
  - HTML/CSS for layout and styling
  - JavaScript for interactivity
  - Markdown-it for rendering
  - Highlight.js for code syntax highlighting

- **Development Tools:**
  - Poetry for dependency management
  - Ruff for linting
  - MyPy for type checking

## 🚀 Getting Started

### 1. Prerequisites
You need Python 3.10 or later and Poetry. Install Poetry using:
```bash
curl -sSL https://install.python-poetry.org | python3
```

### 2. Clone the Repository
```bash
git clone https://github.com/Hugues-DTANKOUO/giteyes.git
cd giteyes
```

### 3. Install Dependencies
```bash
poetry install
```

### 4. Configuration (Optional)
To customize the application's behavior:
```bash
# Configuration is handled through environment variables
export GITEYES_DEBUG=True  # Enable debug mode
```

### 5. Development Server
Start the local development server:
```bash
poetry run server
```

### 6. Local Access
Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## 📂 Key Features

1. **Repository Explorer**
   - Browse repositories and their directory structure
   - Filter by file types and directories
   - [View Implementation](/src/giteyes/explorer.py)

2. **Content Renderer**
   - Markdown rendering with syntax highlighting
   - Support for images and diagrams
   - [View Implementation](/src/giteyes/renderer.py)

3. **Search Engine**
   - Full-text search across documentation
   - Quick navigation to search results
   - [View Implementation](/src/giteyes/search.py)

4. **User Preferences**
   - Customizable reading experience
   - History tracking and bookmarks
   - [View Implementation](/src/giteyes/preferences.py)

## 🤝 Contributing

Contributions are welcome! Check out our [Contributing Guide](CONTRIBUTING.md) for details about:
- Project setup
- Development workflow
- Code style guidelines
- Testing requirements

Ways to contribute:
- Improving repository parsing
- Enhancing the reading experience
- Expanding supported content types
- Adding search capabilities
- Fixing bugs

## 🧑‍💻 About the Author

Maintained by **Hugues Dtankouo**, a Senior Full Stack Developer with extensive Python experience.

📧 **Contact:** [huguesdtankouo@gmail.com](mailto:huguesdtankouo@gmail.com)  
🔗 **LinkedIn:** [Hugues Dtankouo](https://www.linkedin.com/in/dtankouo)  
🔗 **GitHub:** [Hugues-DTANKOUO](https://github.com/Hugues-DTANKOUO)  

## 📄 License & Documentation

- **License:** [MIT License](LICENSE)
- **Change Log:** [CHANGELOG.md](CHANGELOG.md)

## 🚧 Project Status

This is an early-stage project with basic functionality implemented. Future plans include:
- User authentication for private repositories
- Offline reading mode
- Advanced content searching
- Mobile application version
- Community annotations and highlights

Contributions and feedback are highly appreciated!

## 🎯 Current Focus

The project is currently focused on:
1. Improving the parsing algorithm for different repository structures
2. Enhancing the reading interface
3. Adding more metadata extraction
4. Supporting more content types beyond Markdown