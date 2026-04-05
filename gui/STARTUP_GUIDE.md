# Statscrypt Suite - Quick Start Guide

## Starting the Application

### All Platforms - Auto Bootstrap (Easiest!)

**Windows:**
```
Double-click: start.cmd
```

**macOS/Linux:**
```bash
chmod +x start
./start
```

These scripts will automatically:
1. Check if `just` task runner is installed
2. Auto-install `just` if needed
3. Check for Node.js
4. Install dependencies if needed
5. Build the Python engine
6. Start the application

### All Platforms - Using Just Commands

If you have `just` installed, open terminal in `gui` folder:

```bash
just start
just build
just clean
just help
```

### Manual Method (No Task Runner Needed)

```bash
cd gui
npm install
npm start
```

## Basic Commands

### Loading Data
```stata
use "path/to/file.csv"
```

### Summary Statistics
```stata
summarize
summarize variable_name
```

### List Data
```stata
list
list variable1 variable2
```

### Generate New Variable
```stata
gen new_var = old_var
```

### Conditional Analysis
```stata
summarize variable if condition
```

### Create Graphs
```stata
graph variable_name
```

## Tips

- Use **Ctrl+O** (or Cmd+O on Mac) to open a file dialog
- Use **Arrow Up/Down** keys to navigate command history
- Press **F12** to open developer tools for debugging
- Check the **File > Commands Help** menu for available commands
- The **Review** panel shows your command history
- The **Variables** panel displays available variables once data is loaded

## Troubleshooting

### "Python engine is not running"
- Make sure you have Python 3.9+ installed
- Try running the startup script again
- Check the developer console (F12) for errors

### Commands not executing
- Make sure your CSV file path is correct and the file exists
- Check that variable names are spelled correctly

### Variables not showing
- Load a CSV file first using the `use` command
- Make sure the CSV file has headers

## Building for Distribution

To create a standalone application executable:
```bash
npm run build
```

Or just build without packaging:
```bash
npm run build-python-engine
```
