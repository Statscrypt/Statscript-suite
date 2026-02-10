# Statscrypt v1.0 Roadmap - Student-Ready Release

## Current Status Analysis

### ✅ Working Features
- `use` - Load CSV files
- `summarize` - Basic descriptive statistics (mean, std, min, max)
- `list` - Display first 20 rows
- `graph` - Histogram (1 var) and scatter plot (2 vars)
- Basic `if` conditions (>, <, =)
- `gen` - Variable copying only

### ❌ Critical Gaps for Students
1. **No regression analysis** - Students can't run OLS models
2. **Limited `gen` command** - Can't do arithmetic or transformations
3. **Weak `if` operators** - Missing >=, <=, !=, &, |
4. **No categorical analysis** - No tabulate command
5. **No data cleaning** - Can't drop/keep variables or observations
6. **No data export** - Can't save cleaned datasets

---

## v1.0 Priority Features (Student-Ready)

### 🔴 CRITICAL (Must Have for v1.0)

#### 1. **Regression Analysis** (`regress`)
**Why:** Core requirement for any statistics course.

**Syntax:**
```stata
regress y x1 x2 x3
regress wage education experience
```

**Output:**
- Coefficients
- Standard errors
- t-statistics
- p-values
- R-squared
- Adjusted R-squared
- F-statistic

**Implementation:** Use `statsmodels.api.OLS`

---

#### 2. **Enhanced `gen` Command** (Arithmetic & Functions)
**Why:** Students need to create log transformations, interactions, and derived variables.

**Syntax:**
```stata
gen log_wage = log(wage)
gen age_squared = age * age
gen total = price * quantity
gen interaction = age * education
gen ratio = income / expenses
```

**Supported:**
- Arithmetic: `+`, `-`, `*`, `/`, `^` (power)
- Functions: `log()`, `exp()`, `sqrt()`, `abs()`
- Parentheses for order of operations

**Implementation:** Parse expression tree, evaluate with pandas

---

#### 3. **Tabulation** (`tabulate` or `tab`)
**Why:** Essential for categorical data analysis (frequencies, cross-tabs).

**Syntax:**
```stata
tabulate gender
tabulate gender education
tab region income_bracket
```

**Output:**
- Frequency table
- Percentages
- Two-way cross-tabulation with row/column percentages

**Implementation:** Use `pd.crosstab()` and `value_counts()`

---

#### 4. **Enhanced `if` Conditions**
**Why:** Current implementation is too limited for real analysis.

**Add Support For:**
```stata
summarize if age >= 30
list if salary <= 50000
gen high_earner = 1 if income > 100000
summarize if age > 25 & education >= 16
list if region == "North" | region == "South"
```

**Operators:**
- `>=`, `<=`, `!=`
- `&` (and), `|` (or)
- `==` (equality)

**Implementation:** Improve tokenizer and parser to handle compound conditions

---

#### 5. **Correlation** (`correlate` or `corr`)
**Why:** Standard exploratory analysis tool.

**Syntax:**
```stata
correlate
correlate wage education experience
corr age income
```

**Output:**
- Correlation matrix
- Pairwise correlations

**Implementation:** Use `df.corr()`

---

### 🟡 IMPORTANT (Should Have for v1.0)

#### 6. **Drop Variables/Observations** (`drop`)
**Why:** Data cleaning is essential.

**Syntax:**
```stata
drop age salary          # Drop variables
drop if age < 18         # Drop observations
```

**Implementation:** Use `df.drop()` and boolean indexing

---

#### 7. **Keep Variables/Observations** (`keep`)
**Why:** Inverse of drop, often more intuitive.

**Syntax:**
```stata
keep id name wage        # Keep only these variables
keep if year >= 2020     # Keep only these observations
```

---

#### 8. **Save Data** (`save`)
**Why:** Students need to save cleaned datasets.

**Syntax:**
```stata
save "cleaned_data.csv"
save "output.csv", replace
```

**Implementation:** Use `df.to_csv()`

---

#### 9. **T-tests** (`ttest`)
**Why:** Basic hypothesis testing.

**Syntax:**
```stata
ttest wage == 50000              # One-sample t-test
ttest wage, by(gender)           # Two-sample t-test
```

**Implementation:** Use `scipy.stats.ttest_1samp()` and `ttest_ind()`

---

#### 10. **Count Observations** (`count`)
**Why:** Simple but frequently used.

**Syntax:**
```stata
count
count if age > 30
```

**Implementation:** Use `len(df)` or `df.query().shape[0]`

---

### 🟢 NICE TO HAVE (Can Wait for v1.1)

#### 11. **Rename Variables** (`rename`)
```stata
rename old_name new_name
```

#### 12. **Sort Data** (`sort`)
```stata
sort age
sort wage, descending
```

#### 13. **Display Command** (`display`)
```stata
display 2 + 2
display "Hello World"
```

#### 14. **Help System** (`help`)
```stata
help regress
help gen
```

#### 15. **Do-file Execution** (`do`)
```stata
do "analysis.do"
```

---

## Implementation Priority Order

### Phase 1: Core Statistical Analysis (Week 1-2)
1. ✅ **Regression** (`regress`) - Day 1-3
2. ✅ **Enhanced `gen`** (arithmetic) - Day 4-5
3. ✅ **Tabulate** - Day 6-7

### Phase 2: Data Management (Week 3)
4. ✅ **Enhanced `if`** (>=, <=, !=, &, |) - Day 8-9
5. ✅ **Correlation** - Day 10
6. ✅ **Drop/Keep** - Day 11-12
7. ✅ **Save** - Day 13-14

### Phase 3: Additional Stats (Week 4)
8. ✅ **T-test** - Day 15-16
9. ✅ **Count** - Day 17
10. ✅ Testing & Bug Fixes - Day 18-21

---

## Minimum Viable Student Product (MVSP)

For a student to use Statscrypt for a typical intro statistics/econometrics course, you MUST have:

1. **`regress`** - Run OLS regressions
2. **`gen` with arithmetic** - Create transformations
3. **`tabulate`** - Analyze categorical data
4. **Enhanced `if`** - Filter data properly
5. **`correlate`** - Exploratory analysis

**With these 5 features, students can:**
- Load and explore data
- Clean and transform variables
- Run descriptive statistics
- Perform regression analysis
- Analyze categorical variables
- Complete 80% of typical homework assignments

---

## Technical Implementation Notes

### 1. Regression (`regress`)
```python
import statsmodels.api as sm

def run_regress(session, variables):
    y = session.df[variables[0]]
    X = session.df[variables[1:]]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    return model.summary().as_text()
```

### 2. Enhanced `gen` (Expression Parser)
```python
import ast
import operator
import numpy as np

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}

FUNCTIONS = {
    'log': np.log,
    'exp': np.exp,
    'sqrt': np.sqrt,
    'abs': np.abs,
}

def eval_expression(expr, df):
    tree = ast.parse(expr, mode='eval')
    # Recursively evaluate AST nodes
    # Replace variable names with df[var]
    # Apply operators and functions
```

### 3. Tabulate
```python
def run_tabulate(session, variables):
    if len(variables) == 1:
        counts = session.df[variables[0]].value_counts()
        pct = counts / counts.sum() * 100
        return pd.DataFrame({'Freq': counts, 'Percent': pct})
    else:
        return pd.crosstab(
            session.df[variables[0]],
            session.df[variables[1]],
            margins=True
        )
```

### 4. Enhanced `if` Conditions
Update tokenizer to recognize:
- `>=`, `<=`, `!=`
- `&`, `|`

Update parser to build condition tree:
```python
def parse_condition(tokens):
    # Convert: age > 30 & income < 50000
    # To: (df['age'] > 30) & (df['income'] < 50000)
```

---

## Testing Strategy

### Unit Tests Needed
- `test_regress.py` - OLS regression with known results
- `test_gen_arithmetic.py` - Expression evaluation
- `test_tabulate.py` - Frequency tables
- `test_conditions.py` - Complex if statements
- `test_correlate.py` - Correlation matrices

### Integration Tests
- Load data → clean → transform → regress → save
- Conditional analysis with compound conditions
- Multi-variable tabulation

### Sample Datasets for Testing
1. **wages.csv** - wage, education, experience, gender
2. **sales.csv** - product, region, revenue, quantity
3. **students.csv** - grade, study_hours, attendance, major

---

## Documentation Updates

### Update USAGE_GUIDE.md
- Add regression examples
- Show gen arithmetic syntax
- Demonstrate tabulate usage
- Explain compound if conditions

### Create COMMAND_REFERENCE.md
- Complete syntax for each command
- Examples for each command
- Common error messages

### Update README.md
- Highlight new v1.0 features
- Update feature comparison table
- Add "What can students do?" section

---

## Success Criteria for v1.0

A student should be able to:

✅ Load a dataset
✅ Explore with summarize, list, correlate
✅ Create new variables with arithmetic
✅ Filter data with complex conditions
✅ Analyze categorical data with tabulate
✅ Run OLS regression
✅ Create visualizations
✅ Save cleaned data

**If a student can complete a typical econometrics problem set using only Statscrypt, v1.0 is ready.**

---

## Post-v1.0 Roadmap (v1.1+)

- ANOVA (`anova`)
- Chi-square tests (`chi2`)
- Logistic regression (`logit`)
- Panel data commands (`xtset`, `xtreg`)
- Time series (`tsset`, `tsline`)
- Do-file execution
- Log files
- .dta file support
- Command autocomplete
- Syntax highlighting

---

## Estimated Timeline

- **Phase 1 (Core Stats):** 2 weeks
- **Phase 2 (Data Mgmt):** 1 week
- **Phase 3 (Testing):** 1 week
- **Total:** 4 weeks to student-ready v1.0

---

## Questions to Answer Before Starting

1. Should `gen` support `if` modifiers? (e.g., `gen high = 1 if income > 50000`)
2. Should `regress` support robust standard errors?
3. Should `tabulate` show chi-square statistics?
4. Should we support variable labels in v1.0?
5. Should `save` support formats other than CSV?

---

**Bottom Line:** Focus on `regress`, enhanced `gen`, `tabulate`, enhanced `if`, and `correlate`. These 5 features make Statscrypt viable for students. Everything else is secondary.
