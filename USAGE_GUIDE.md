# Statscrypt v1.0 - Complete Usage Guide

## Quick Start

### Loading Data
```stata
use "../shared/sample.csv"
summarize
list
```

## Core Commands

### 1. Data Loading & Inspection

#### Load CSV File
```stata
use "data.csv"
use "C:/Users/Name/Documents/data.csv"
```

#### View Summary Statistics
```stata
summarize
summarize wage education experience
summarize if age >= 30
```

#### List Observations
```stata
list
list name age wage
list if wage > 60000
list age wage if region == "North"
```

#### Count Observations
```stata
count
count if age >= 30
count if gender == "Female" & education >= 18
```

### 2. Creating Variables

#### Simple Variable Creation
```stata
gen age_copy = age
gen wage_thousands = wage
```

#### Arithmetic Operations
```stata
gen wage_per_hour = wage / hours_worked
gen total_comp = wage + 5000
gen age_squared = age ** 2
gen experience_double = experience * 2
```

#### Mathematical Functions
```stata
gen log_wage = log(wage)
gen exp_age = exp(age)
gen sqrt_hours = sqrt(hours_worked)
gen abs_diff = abs(wage - 60000)
```

#### Complex Expressions
```stata
gen interaction = age * education
gen adjusted_wage = (wage - 50000) / 1000
gen performance_index = (performance_score * training_hours) / 100
```

#### Conditional Variable Creation
```stata
gen high_earner = 1 if wage > 70000
gen senior = 1 if age >= 40
gen experienced = 1 if experience >= 15
```

### 3. Data Filtering & Subsetting

#### Drop Variables
```stata
drop id name
drop performance_score training_hours
```

#### Drop Observations
```stata
drop if age < 25
drop if wage < 45000
drop if year < 2022
```

#### Keep Variables
```stata
keep age wage education experience
keep name gender region wage
```

#### Keep Observations
```stata
keep if age >= 30
keep if region == "North" | region == "South"
keep if wage >= 50000 & education >= 16
```

### 4. Statistical Analysis

#### Descriptive Statistics
```stata
summarize wage education experience
summarize wage if gender == "Female"
summarize if year == 2023
```

#### Correlation Analysis
```stata
correlate
correlate wage education experience
corr age wage if region == "North"
```

#### Frequency Tables
```stata
tabulate gender
tabulate region
tabulate gender region
tab department if year == 2023
```

#### Regression Analysis
```stata
regress wage education experience
regress wage age education experience
regress wage education if gender == "Male"
regress wage education experience age
```

#### T-Tests
```stata
ttest wage == 60000
ttest wage gender
ttest performance_score promotion
```

### 5. Data Visualization

#### Histograms
```stata
graph wage
graph age
graph education
```

#### Scatter Plots
```stata
graph wage education
graph age wage
graph experience wage
```

### 6. Saving Data

#### Export to CSV
```stata
save "cleaned_data.csv"
save "analysis_results.csv"
```

## Advanced Examples

### Example 1: Wage Analysis by Gender
```stata
use "../shared/sample.csv"

summarize wage if gender == "Male"
summarize wage if gender == "Female"

ttest wage gender

regress wage education experience if gender == "Female"
regress wage education experience if gender == "Male"
```

### Example 2: Creating Derived Variables
```stata
use "../shared/sample.csv"

gen log_wage = log(wage)
gen age_squared = age ** 2
gen experience_education = experience * education
gen wage_per_hour = wage / hours_worked

summarize log_wage age_squared experience_education
correlate wage log_wage age_squared
```

### Example 3: Regional Analysis
```stata
use "../shared/sample.csv"

tabulate region
summarize wage if region == "North"
summarize wage if region == "South"

count if region == "North"
count if region == "South"

regress wage education experience if region == "North"
```

### Example 4: Performance Analysis
```stata
use "../shared/sample.csv"

gen high_performer = 1 if performance_score >= 85
count if high_performer == 1

summarize wage if high_performer == 1
summarize wage if performance_score < 85

ttest wage high_performer
```

### Example 5: Data Cleaning Workflow
```stata
use "../shared/sample.csv"

count
drop if age < 25
drop if wage < 45000
count

keep age gender education experience wage region
summarize

save "cleaned_sample.csv"
```

### Example 6: Comprehensive Analysis
```stata
use "../shared/sample.csv"

gen log_wage = log(wage)
gen age_squared = age ** 2
gen interaction = education * experience

regress log_wage education experience age age_squared
correlate wage education experience age

tabulate gender
tabulate region department

keep if year >= 2022
count
save "recent_data.csv"
```

## Conditional Operators

### Comparison Operators
- `>` Greater than
- `<` Less than
- `>=` Greater than or equal
- `<=` Less than or equal
- `==` Equal to
- `!=` Not equal to

### Logical Operators
- `&` AND
- `|` OR

### Examples
```stata
list if age >= 30 & wage < 60000
summarize if gender == "Female" | region == "North"
drop if age < 25 | age > 65
keep if education >= 16 & experience >= 10
count if wage >= 50000 & wage <= 80000
```

## Mathematical Functions

- `log(x)` - Natural logarithm
- `exp(x)` - Exponential
- `sqrt(x)` - Square root
- `abs(x)` - Absolute value

### Examples
```stata
gen log_wage = log(wage)
gen exp_score = exp(performance_score / 100)
gen sqrt_hours = sqrt(training_hours)
gen abs_deviation = abs(wage - 65000)
```

## Tips & Best Practices

### 1. Always Check Your Data First
```stata
use "data.csv"
summarize
list
count
```

### 2. Create Derived Variables Before Analysis
```stata
gen log_wage = log(wage)
gen age_squared = age ** 2
regress log_wage education experience age age_squared
```

### 3. Use Descriptive Variable Names
```stata
gen wage_per_hour = wage / hours_worked
gen high_performer = 1 if performance_score >= 85
gen senior_employee = 1 if age >= 40
```

### 4. Save Intermediate Results
```stata
use "raw_data.csv"
drop if age < 18
keep if year >= 2020
save "cleaned_data.csv"
```

### 5. Document Your Analysis
```stata
use "data.csv"
summarize
gen log_wage = log(wage)
regress log_wage education experience
save "analysis_ready.csv"
```

## Common Workflows

### Exploratory Data Analysis
```stata
use "data.csv"
summarize
count
tabulate gender
tabulate region
correlate wage education experience age
graph wage education
```

### Regression Analysis
```stata
use "data.csv"
gen log_wage = log(wage)
gen age_squared = age ** 2
correlate log_wage education experience age
regress log_wage education experience age age_squared
```

### Comparative Analysis
```stata
use "data.csv"
summarize wage if gender == "Male"
summarize wage if gender == "Female"
ttest wage gender
regress wage education experience if gender == "Male"
regress wage education experience if gender == "Female"
```

### Data Preparation
```stata
use "raw_data.csv"
count
drop if age < 18
drop if wage < 20000
keep age gender education experience wage region
gen log_wage = log(wage)
save "clean_data.csv"
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` / `Cmd+O` | Open file browser |
| `↑ / ↓` | Navigate command history |
| `Enter` | Execute command |
| `F12` | Developer console |
| `Ctrl+Q` / `Cmd+Q` | Quit |

## Troubleshooting

### "No data loaded"
Run `use "filename.csv"` first

### "Variable not found"
Check spelling and case sensitivity

### "Invalid syntax"
Check command syntax in examples above

### Graph won't display
Ensure variables are numeric

### File not found
Use forward slashes: `C:/Users/Name/data.csv`

## Sample Dataset

The included `sample.csv` contains:
- 50 employee records
- Variables: id, name, age, gender, education, experience, wage, hours_worked, region, department, performance_score, training_hours, promotion, year
- Perfect for testing all features

### Try These Commands
```stata
use "../shared/sample.csv"
summarize wage education experience
tabulate gender region
gen log_wage = log(wage)
regress wage education experience age
correlate wage education experience
graph wage education
```

## Getting Help

- Press `F12` for developer console
- Check error messages in output panel
- Review command history
- Consult this guide for syntax examples
