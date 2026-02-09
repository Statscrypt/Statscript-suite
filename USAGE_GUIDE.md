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

### Example 2: Creating and Analyzing New Variables

```stata
# Load data
use "data.csv"

# Create a new variable based on an existing one
gen age_years_decade = age

# Get summary for the new variable
summarize age age_years_decade

# List both variables
list age age_years_decade
```

### Example 3: Conditional Analysis

```stata
# Load data
use "data.csv"

# Summary statistics only for ages > 30
summarize age if age>30

# Summary for specific variable with condition
summarize salary if salary>50000

# List all rows matching a condition
list if age>25
```

### Example 4: Data Visualization

```stata
# Load data
use "data.csv"

# Create a graph of age distribution
graph age

# Create a graph of salary
graph salary
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
# Copy an existing variable
gen copy_of_age = age

# Create derived variables
gen salary_half = salary
gen id_copy = employee_id
```

### Conditional Analysis

#### Supported Conditions

```stata
# Equal to
summarize if age=30

# Greater than
summarize if salary>50000

# Less than
summarize if age<25

# Greater than or equal
summarize if age>=18

# Less than or equal
summarize if salary<=100000

# Not equal
summarize if department!=Sales
```

### Creating Visualizations

```stata
# Create a graph
graph age
graph salary
graph department
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

## Common Issues and Solutions

### Issue: "File not found"
**Solution:** Check the file path is correct. Use forward slashes `/` in paths.

### Issue: "No data loaded"
**Solution:** Run `use "path/to/file.csv"` first before other commands.

### Issue: "Variables not found"
**Solution:** Make sure variable names are spelled correctly (case-sensitive).

### Issue: Commands not working
**Solution:** 
1. Check F12 console for error messages
2. Make sure Python engine started (should see "ready" message)
3. Try restarting the application

### Issue: Graph window won't open
**Solution:** Make sure data is loaded and valid variable names are used.

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
summarize age age_copy if age>30
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

# Find ranges
summarize if column_name>1000
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

