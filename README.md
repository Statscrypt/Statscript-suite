# Statscrypt Suite - Stata Alternative Built with Python & Electron

A Stata-like statistical analysis tool built with Python backend and Electron frontend. This is a powerful alternative to Stata with a clean, modern interface.

## Quick Start

### All Platforms (Windows, macOS, Linux)

**Option 1: Auto-Bootstrap (Easiest)**

Double-click the appropriate file:
- **Windows:** `gui/start.cmd` ← Recommended
- **macOS/Linux:** `gui/start` (make it executable first)

These will automatically install `just` if needed, then start the app.

**Option 2: Using Just (If already installed)**

```bash
cd gui
just start
```

**Option 3: Manual (No Just required)**

```bash
cd gui
npm install      # First time only
npm start
```

## What's New (Fixed)

 **CRITICAL FIX:** Commands now actually execute (was broken due to JSON communication bug)  
 **Better UI:** Redesigned interface with proper layout  
 **File Dialog:** Ctrl+O to open files instead of typing paths  
 **Command History:** Arrow Up/Down to navigate  
 **Error Logging:** F12 to see debug info  
 **Cross-Platform:** Justfile for Windows, macOS, and Linux with unified commands
 **Easy Installation:** Run `start.cmd` or `start` script (auto-installs just)  
 **Help Menu:** Built-in command reference  

##  Basic Usage

After launching:

```stata
# Load a CSV file
use "path/to/data.csv"

# See summary statistics
summarize

# View data
list

# Create new variable
gen new_var = old_var

# Analyze with conditions
summarize salary if age>30

# Create graphs
graph age
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` / `Cmd+O` | Open file dialog |
| `Arrow Up/Down` | Navigate command history |
| `F12` | Open developer tools / Console |
| `Ctrl+Q` / `Cmd+Q` | Quit application |
| `Enter` | Execute command |

## Available Commands (via Just)

```bash
just start           # Start the application (default)
just dev             # Start in development mode
just install         # Install npm dependencies
just build-engine    # Build Python backend
just build           # Build for distribution

```


## Project Structure

```
statscrypt-suite/
├── engine/              # Python backend
│   ├── src/
│   │   └── statscrypt/
│   │       ├── cli.py
│   │       ├── repl.py
│   │       ├── core/
│   │       └── commands/
│   └── pyproject.toml
├── gui/                 # Electron frontend
│   ├── src/
│   │   ├── main.js      
│   │   ├── renderer.js  
│   │   └── index.html   
│   ├── start.bat       
│   └── start.sh         
├── shared/
│   └── sample.csv       # Sample data for testing
└── docs/
```


## Documentation

- **[JUSTFILE_GUIDE.md](JUSTFILE_GUIDE.md)** - How to use Just (recommended!)
- **[STARTUP_GUIDE.md](gui/STARTUP_GUIDE.md)** - Setup guide
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Commands and examples
- **[MIGRATION_TO_JUSTFILE.md](MIGRATION_TO_JUSTFILE.md)** - Why we use Just

## Features

### Current
- Load CSV files
- Summary statistics (`summarize`)
- View data (`list`)
- Generate variables (`gen`)
- Conditional analysis (`if` clauses)
- Graphs (`graph`)
- File dialog
- Command history
- Professional UI

### Planned
- Support for .dta (Stata) files
- More statistical commands
- Data export/save
- Session management
- Command autocomplete
- Plugin system

## Technical Stack

- **Backend:** Python 3.9+ with pandas, numpy, matplotlib
- **Frontend:** Electron + HTML/CSS/JavaScript
- **Communication:** JSON over stdio
- **Packaging:** PyInstaller (Python) + Electron-builder (App)

## Requirements

### To Run
- Node.js 14+ (for Electron)
- Python 3.9+ (if building from source)

If you just use `start.bat`/`start.sh`, these will be auto-detected.

### To Build Production Version
```bash
npm run build
```

This creates a standalone executable in the `dist/` folder.

## Development

### Setup
```bash
cd gui
npm install
```

### Run in Development
```bash
npm start
```

### Build Python Engine
```bash
pip install -e .[dev]
pyinstaller statscrypt.spec --distpath ../gui/resources/engine
```

## Contributing

Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## Example Workflow

```stata
# 1. Load data
use "sales_data.csv"

# 2. Explore
summarize
list

# 3. Analyze
summarize revenue if year>2020
summarize salary if department=Engineering

# 4. Transform
gen revenue_millions = revenue

# 5. Visualize
graph revenue
graph salary
```

## Known Limitations

- Only CSV format currently (Stata .dta support coming)
- Limited to single CSV loading
- Graph functionality depends on matplotlib
- Some Stata commands not yet implemented

## Learning Stata Syntax?

The command syntax is compatible with Stata:

```stata
command [varlist] [if condition] [in range]
```

Examples:
```stata
summarize age income
list if age>30
gen new_var = old_var
```

## Support

If something doesn't work:

1. **Check the Console** (F12 → Console tab)
2. **Try** restarting the application

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

You are free to:
- ✅ Use this software for any purpose
- ✅ Modify and distribute it
- ✅ Use it in commercial projects
- ✅ Sublicense it

The only requirement is to include the license notice.

**Last Updated:** 2026-02-08
