# Statscrypt Suite

![Python](https://img.shields.io/badge/Python-3.9+-3776ab?logo=python&logoColor=white)
![Electron](https://img.shields.io/badge/Electron-28.0.0-47848f?logo=electron&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)

> **A free, open-source statistical analysis suite for students learning Stata.** Statscrypt provides a Stata-compatible learning environment for students who don't yet have access to commercial statistical software, enabling them to practice data analysis workflows and complete assignments before formally using Stata.

## Overview

Statscrypt is an **educational statistics platform** designed to bridge the gap between aspiring data analysts and professional statistical software. Built with Python and Electron, it offers a Stata-like command interface with modern UI/UX, making it ideal for:

- **Students** learning statistical methods and data analysis
- **Teaching** fundamental statistics concepts
- **Practice** before using commercial software
- **Research prototyping** with open-source tools

## Quick Start

### All Platforms (Windows, macOS, Linux)

**Easiest Option: Run the Launcher**

- **Windows:** Double-click `gui/start.cmd`
- **macOS/Linux:** Run `gui/start` in terminal

Both auto-install dependencies and start the app.

**Alternative: Using Just**

```bash
cd gui
just start
```

## Features

**Core Functionality**
- Load and analyze CSV files
- Descriptive statistics (`summarize`)
- Data exploration (`list`)
- Variable creation and transformation (`gen`)
- Visualizations: histograms & scatter plots (`graph`)
- Conditional analysis (`if` clauses)
- Command history navigation
- File dialog integration (Ctrl+O)

**User Experience**
- Stata-compatible command syntax
- Modern desktop interface
- Cross-platform support (Windows, macOS, Linux)
- Real-time error feedback
- Developer console (F12)

## Usage Examples

```stata
# Load CSV data
use "sales_data.csv"

# Explore the dataset
summarize
list

# Create new variables
gen profit = revenue - cost

# Descriptive analysis
summarize revenue if year > 2020

# Visualizations
graph revenue              # Histogram of revenue
graph revenue profit       # Scatter plot: revenue vs profit
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` / `Cmd+O` | Open file browser |
| `↑ / ↓` | Navigate command history |
| `Enter` | Execute command |
| `F12` | Developer console |
| `Ctrl+Q` / `Cmd+Q` | Quit |

## What's New (Fixed)

 **CRITICAL FIX:** Commands now actually execute (was broken due to JSON communication bug)
 **Better UI:** Redesigned interface with proper layout
 **File Dialog:** Ctrl+O to open files instead of typing paths
 **Command History:** Arrow Up/Down to navigate
 **Error Logging:** F12 to see debug info
 **Cross-Platform:** Justfile for Windows, macOS, and Linux with unified commands
 **Easy Installation:** Run `start.cmd` or `start` script (auto-installs just)
 **Graphs:** Single-variable histograms and two-variable scatter plots

## Installation

### Requirements
- **Node.js** 14+ (Electron runtime)
- **Python** 3.9+ (statistical backend)

Both are auto-detected by the launcher scripts.

### From Source

```bash
# Clone the repository
git clone https://github.com/Statscrypt/Statscript-suite.git
cd statscrypt-suite

# Run the application
cd gui
./start              # macOS/Linux
# or
start.cmd           # Windows
```

## Documentation

- [Startup Guide](gui/STARTUP_GUIDE.md) – Setup troubleshooting
- [Usage Guide](USAGE_GUIDE.md) – Complete command reference

## Technical Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.9+ (pandas, numpy, statsmodels, matplotlib) |
| **Frontend** | Electron 28.0.0 + HTML5/CSS/JavaScript |
| **Communication** | JSON over stdio |
| **Packaging** | PyInstaller (CLI) + Electron-builder (GUI) |

## Development

### Setup

```bash
cd gui
npm install
cd ../engine
pip install -e .[dev]
```

### Run Development Build

```bash
cd gui
npm start
```

### Build for Distribution

```bash
cd gui
just build          # Builds both engine and GUI
# Output in: gui/dist/
```

## Contributing

We welcome contributions from students, educators, and developers! Whether it's bug fixes, new statistical commands, or documentation improvements, your help makes Statscrypt better.

### Getting Started

1. **Fork** the repository on [GitHub](https://github.com/Faadabu/statscrypt-suite)
2. **Clone** your fork locally
   ```bash
   git clone https://github.com/YOUR-USERNAME/statscrypt-suite.git
   cd statscrypt-suite
   ```
3. **Create** a feature branch
   ```bash
   git checkout -b feature/short-description
   ```
4. **Make** your changes
5. **Test** locally with `just start` or `npm start`
6. **Commit** with a clear message
   ```bash
   git commit -m "feat: add new statistical command"
   ```
7. **Push** to your fork and open a [Pull Request](https://github.com/Faadabu/statscrypt-suite/pulls)

### Contribution Types

** Add Statistical Commands**
- Implement new Stata-compatible commands in `engine/src/statscrypt/commands/`
- Update tests and documentation

** Bug Fixes**
- Fork, fix, test, and submit PR with clear description

** Documentation**
- Improve guides, examples, or API documentation
- Fix typos and clarify instructions

** UI/UX Improvements**
- Enhance electron frontend in `gui/src/`
- Better error messages, accessibility features

### Code Standards

- **Python:** Black formatting, isort imports, Pylint checks
- **JavaScript:** ESLint (via pre-commit hooks)
- **Commits:** Use semantic versioning (`feat:`, `fix:`, `chore:`, `docs:`)

Run pre-commit hooks before pushing:
```bash
pre-commit run --all-files
```

### Questions?

- Check existing [Issues](https://github.com/Faadabu/statscrypt-suite/issues)
- Discuss in [Discussions](https://github.com/Faadabu/statscrypt-suite/discussions)
- Email or message on GitHub

---

## Roadmap

**v0.2.0 (Coming Soon)**
- [ ] Support Stata `.dta` file format
- [ ] Additional statistical tests (t-test, chi-square, ANOVA)
- [ ] Data export (CSV, Excel)
- [ ] Command autocomplete

**v0.3.0 (Future)**
- [ ] Session persistence
- [ ] Plugin system
- [ ] Custom chart types
- [ ] Performance optimizations

## Limitations & Future Work

- **File Format:** Currently supports CSV only (`.dta` support in v0.2.0)
- **Single Dataset:** One CSV file at a time
- **Command Set:** Subset of Stata commands (expanding with each release)
- **Performance:** Optimized for datasets < 1GB

## License

**MIT License** – Free to use for any purpose (commercial, educational, personal).

See [LICENSE](LICENSE) for full details.

### You are free to:
 Use in educational settings
 Modify and redistribute
 Use commercially
 Include in proprietary projects

The only requirement: include the original license notice.

---

## About

**Author & Lead Maintainer:** [Faad Abubakar](https://github.com/Faadabu)

Statscrypt was created to democratize access to statistical analysis tools for students worldwide. Your contributions help us achieve that mission.

**Repository:** https://github.com/Statscrypt/Statscript-suite
---

**Made with ❤️ for students learning statistics.**
