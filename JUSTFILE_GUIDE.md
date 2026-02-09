# Justfile - Cross-Platform Task Runner Guide

## What is Just?

`Just` is a cross-platform command runner (like `make` but better). It allows you to define and run tasks with a single unified syntax across Windows, macOS, and Linux.

**Why use Just instead of separate scripts?**
- One `.Justfile` for all platforms
- No .bat, .ps1, .sh duplicates
- No learning different syntax per OS
- Same commands everywhere
- Professional, industry standard

## Installing Just

### Option 1: Auto-Installation (Recommended)

Just run the bootstrap scripts - they'll auto-install `just` if needed:

**Windows:**
```
Double-click: gui/start.cmd
```

**macOS/Linux:**
```bash
chmod +x gui/start
./gui/start
```

### Option 2: Manual Installation

#### Windows
**With Cargo (Rust package manager):**
```powershell
cargo install just
```

**With Package Manager:**
```powershell
choco install just        # Chocolatey
# or
scoop install just        # Scoop
# or
winget install Casey.Just # Windows Package Manager
```

**Or download prebuilt:**
https://github.com/casey/just/releases

#### macOS
**With Homebrew:**
```bash
brew install just
```

**Or download:**
https://github.com/casey/just/releases

#### Linux
**With package manager:**
```bash
# Debian/Ubuntu
sudo apt-get install just

# Fedora
sudo dnf install just

# Arch
sudo pacman -S just
```

**Or download:**
https://github.com/casey/just/releases

## Using Just with Statscrypt

### Available Commands

```bash
just              # Show available commands
just start        # Start the app
just dev          # Start in dev mode
just install      # Install npm deps
just build-engine # Build Python engine
just build        # Build for distribution
just dist         # Create distribution package
just clean        # Clean build artifacts
just update       # Update dependencies
just version      # Show version info
just help         # Show detailed help
```

### Quick Start

```bash
cd gui
just start         
```

### Define Custom Tasks

Edit `Justfile` to add your own commands:

```makefile
# Build and start
build-and-run:
    just build
    just start

# Dev with Python watch
dev-watch:
    just dev
```

Then run: `just build-and-run`

## How the Justfile Works

The `Justfile` in `gui/` contains recipes (tasks):

```makefile
# Install dependencies
install:
    #!/usr/bin/env bash
    echo "Installing npm dependencies..."
    npm install
    echo "✓ Dependencies installed"

# Start development mode
start:
    #!/usr/bin/env bash
    if [ ! -d "node_modules" ]; then
        echo "Dependencies not found. Installing..."
        npm install
    fi
    echo "Starting Statscrypt Suite..."
    npm start

# Build for distribution
dist:
    #!/usr/bin/env bash
    echo "Creating distribution package..."
    just build-engine
    npm run dist
    echo "✓ Distribution package created"
```

Each recipe:
- Is defined with `recipeame:`
- Contains shell commands (Bash)
- Runs on any platform with `just recipeame`

## Benefits Over Platform-Specific Scripts

| Feature | Platform Scripts (.bat, .sh, .ps1) | Justfile |
|---------|-------------------------------------|----------|
| Windows | ✓ Works | ✓ Works |
| macOS | ✓ Works | ✓ Works |
| Linux | ✓ Works | ✓ Works |
| Single Syntax | ✗ No (3 versions) | ✓ Yes (1 file) |
| Maintainability | ✗ Hard (keep in sync) | ✓ Easy (one source) |
| Documentation | ✗ Limited | ✓ Built-in |
| Task Dependencies | ✗ Manual | ✓ Automatic |
| Error Handling | ✗ Basic | ✓ Robust |

## Advanced Usage

### Sequential Tasks
```bash
just build && just start
```

### Variables
```makefile
PYTHON_BIN := "/usr/bin/python3"

test:
    {{PYTHON_BIN}} -m pytest
```

### Conditional Execution
```makefile
dev:
    @if [ ! -d "node_modules" ]; then \
        just install; \
    fi
```

### Multiple OS Support
```makefile
info:
    echo "System: $(uname -s)"
    echo "Home: $HOME"
```

## Troubleshooting

### Command not found: just
**Solution:** Install just (see "Installing Just" section above)

### Permission denied on start script
**Solution:**
```bash
chmod +x gui/start
```

### Justfile not found
**Make sure you're in the gui folder:**
```bash
cd gui
just start
```

### Task failed
**Check the error output and ensure:**
1. All dependencies are installed (`just install`)
2. Python 3.9+ is available
3. Node.js is installed

## Learning More

- **Official Justfile docs:** https://just.systems
- **GitHub:** https://github.com/casey/just
- **Examples:** https://github.com/casey/just/tree/master/examples

## Summary

For Statscrypt Suite, using Justfile means:

 **Windows, macOS, Linux users all use the same commands**
 **Easy to add new tasks without duplicating code**
 **Professional, industry-standard tooling**
 **Future-proof for expanding the project**

**Just use `just start` and it works everywhere!**
