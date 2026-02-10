# Statscrypt Suite - Usage Examples

## Getting Started

### Example 1: Basic Data Analysis

```stata
# Step 1: Load a CSV file
use "sample.csv"

# Step 2: View summary statistics
summarize

# Step 3: Look at the first 20 rows
list

# Step 4: Check specific columns
summarize age salary
```

### Example 2: Creating New Variables

```stata
# Load data
use "data.csv"

# Create a copy of an existing variable
gen age_copy = age

# Get summary for the new variable
summarize age age_copy

# List both variables
list age age_copy
```

### Example 3: Conditional Analysis

```stata
# Load data
use "data.csv"

# Summary statistics only for ages greater than 30
summarize age if age>30

# Summary for specific variable with condition
summarize salary if salary>50000

# List all rows matching a condition
list if age>25

# Supported conditions: >, <
# (>= and <= are not yet supported)
```

### Example 4: Data Visualization

```stata
# Load data
use "data.csv"

# Create a histogram of age distribution
graph age

# Create a scatter plot of age vs salary
graph age salary

# Note: graph only works with numeric variables
```

## Command Reference

### Loading Data

```stata
use "path/to/file.csv"
use "C:/Users/YourName/Documents/data.csv"
use "../data/mydata.csv"
```

### Viewing Data

```stata
# Show summary statistics for all columns
summarize

# Summary for specific columns
summarize age salary

# Show first 20 rows
list

# Show specific columns
list age salary department

# What variables are available?
# Check the "Variables" panel on the right side
```

### Generating Variables

```stata
# Copy an existing variable (only operation supported)
gen age_copy = age
gen income_backup = income

# Note: 'gen' currently only supports copying.
# Arithmetic operations are not yet supported.
```

### Conditional Analysis

#### Supported Conditions

```stata
# Greater than
summarize if salary>50000
list if age>25

# Less than
summarize if age<30
list if salary<100000

# Equal to (basic comparison)
summarize if age=30

# Note: Currently supported operators are: >, <, =
# Not yet supported: >=, <=, !=
```

### Creating Visualizations

```stata
# Create a histogram (single numeric variable)
graph age
graph income

# Create a scatter plot (two numeric variables)
graph age income
graph salary age

# Note: Both variables must be numeric
# Use 'gen' to convert categorical data if needed
```

## Tips and Tricks

### Using File Dialog
- Press **Ctrl+O** (Windows/Linux) or **Cmd+O** (Mac)
- A file browser will open
- Select any CSV file
- The file will be loaded automatically

### Command History
- Press **↑** (Up arrow) to see previous commands
- Press **↓** (Down arrow) to go forward in history
- Edit and re-run with Enter

### Debugging
- Press **F12** to open developer tools
- Look at the Console tab for error messages
- Check the Review panel for command history

### File Paths
- Use forward slashes `/` instead of backslashes `\`
- Relative paths work from the GUI directory
- Absolute paths work too: `C:/Users/Name/data.csv`

### CSV Files
- **First row should contain column headers**
- Use comma-separated values
- Quoted values are supported: `"Some, value"`

## Current Limitations

| Feature | Status | Notes |
|---------|--------|-------|
| `gen` arithmetic | ❌ Not supported | Only `gen newvar = oldvar` (copy) works |
| `if` operators | Partial | Only `>`, `<`, `=` supported. Not: `>=`, `<=`, `!=` |
| Multiline input | ❌ Not supported | Commands must be entered one line at a time. `///` continuation planned for v0.2.0 |
| `graph` customization | ❌ Not supported | Histograms (1 var) and scatter plots (2 vars) only |
| Data export | ❌ Not supported | Coming in v0.2.0 |
| `.dta` files | ❌ Not supported | Only CSV for now |

## Common Issues and Solutions

### Issue: "Invalid 'gen' command syntax"
**Solution:** `gen` only supports copying variables:
- ✅ `gen age_copy = age` works
- ❌ `gen new_age = age / 2` fails (arithmetic not supported)

### Issue: "File not found"
**Solution:** Check the file path is correct. Use forward slashes `/` in paths.

### Issue: "No data loaded"
**Solution:** Run `use "path/to/file.csv"` first before other commands.

### Issue: "Variables not found"
**Solution:** Make sure variable names are spelled correctly (case-sensitive).

### Issue: Conditional commands fail
**Solution:** Only `>`, `<`, `=` operators are supported:
- ✅ `summarize if age>30` works
- ✅ `list if salary<50000` works
- ❌ `summarize if age>=30` fails (`>=` not yet supported)

### Issue: Graph window won't open
**Solution:** Make sure:
1. Data is loaded with `use "file.csv"`
2. Variable names are spelled correctly
3. **Variables are numeric** (text/categorical variables can't be plotted)
   - `graph age` ✅ works (numeric)
   - `graph gender` ❌ fails (categorical text)

### Issue: Commands not working
**Solution:**
1. Check F12 console for error messages
2. Make sure Python engine started (should see "ready" message)
3. Try restarting the application

## Sample Data

A sample CSV file is included at: `../shared/sample.csv`

To use it:
```stata
use "../shared/sample.csv"
summarize
```

## Advanced Usage

### Combining Commands

```stata
# Load, analyze, and create variables
use "data.csv"
summarize age
gen age_copy = age
list age age_copy
summarize age age_copy if age>25
```

### Exploring Data

```stata
# First, load the data
use "mydata.csv"

# See what variables you have (check Variables panel)

# Get overview of all columns
summarize

# Look at some data
list

# Check specific columns
list column1 column2 column3

# Find values above a threshold
summarize if column_name>1000

# Find values below a threshold
list if salary<50000
```

## Next Steps

- Try loading the sample CSV file
- Practice with the `summarize` command
- Experiment with `gen` to create new variables
- Use conditional analysis with `if`
- Create visualizations with `graph`

## Getting Help

- Check **File > Commands Help** menu
- Press **F12** for developer console
- Review the Review panel for command history
- Check error messages in the main output area
