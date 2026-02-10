# Statscrypt Roadmap

## v1.1.0 (Minor Release - Q2 2026)

### Data Management Enhancements
- [ ] `rename` - Rename variables
- [ ] `sort` - Sort data by variables
- [ ] `order` - Reorder variables
- [ ] `replace` - Replace values in existing variables
- [ ] `encode`/`decode` - Convert between string and numeric

### Statistical Tests
- [ ] `chi2` - Chi-square tests for categorical data
- [ ] `anova` - Analysis of variance
- [ ] `pwcorr` - Pairwise correlation with significance tests

### Usability
- [ ] Command autocomplete
- [ ] Syntax highlighting in command input
- [ ] Variable labels support
- [ ] Value labels for categorical variables
- [ ] Command history persistence across sessions

## v1.2.0 (Minor Release - Q3 2026)

### Advanced Statistics
- [ ] `logit` - Logistic regression
- [ ] `probit` - Probit regression
- [ ] Robust standard errors for regression
- [ ] Clustered standard errors

### Data Import/Export
- [ ] `.dta` file format support (Stata files)
- [ ] Excel file import/export
- [ ] JSON data import
- [ ] Multiple dataset support

### Visualization
- [ ] Box plots
- [ ] Bar charts for categorical data
- [ ] Customizable plot titles and labels
- [ ] Export plots to PNG/PDF

## v1.3.0 (Minor Release - Q4 2026)

### Scripting & Automation
- [ ] `do` - Execute do-files (script files)
- [ ] `log` - Session logging
- [ ] Multiline command support with `///`
- [ ] Comment support with `//` and `/* */`
- [ ] Macro variables

### Data Transformation
- [ ] `reshape` - Wide to long and vice versa
- [ ] `merge` - Merge datasets
- [ ] `append` - Append datasets
- [ ] `collapse` - Aggregate data
- [ ] `egen` - Extended generate functions

## v2.0.0 (Major Release - 2026)

### Time Series Analysis
- [ ] `tsset` - Declare time series data
- [ ] `tsline` - Time series plots
- [ ] Lag and lead operators
- [ ] Moving averages
- [ ] ARIMA models

### Panel Data
- [ ] `xtset` - Declare panel data
- [ ] `xtreg` - Panel regression (fixed/random effects)
- [ ] `xtsum` - Panel summary statistics
- [ ] `xtdescribe` - Panel data description

### Advanced Features
- [ ] Matrix operations
- [ ] Programming with loops (`foreach`, `forvalues`)
- [ ] Conditional execution (`if`, `else`)
- [ ] User-defined functions
- [ ] Plugin system for extensions

### Performance
- [ ] Large dataset optimization (>1GB)
- [ ] Parallel processing for regressions
- [ ] Memory management improvements
- [ ] Lazy loading for big data

## v2.1.0+ (Future)

### Machine Learning
- [ ] Decision trees
- [ ] Random forests
- [ ] K-means clustering
- [ ] Principal component analysis (PCA)

### Reporting
- [ ] Export results to Word/PDF
- [ ] Automatic table formatting
- [ ] Regression table output (publication-ready)
- [ ] Summary statistics tables

### Collaboration
- [ ] Cloud storage integration
- [ ] Share analysis workflows
- [ ] Version control for do-files
- [ ] Collaborative editing

### Education Features
- [ ] Interactive tutorials
- [ ] Built-in help system with examples
- [ ] Sample datasets library
- [ ] Assignment templates for instructors

## Community Requests

Vote for features at: https://github.com/Faadabu/statscrypt-suite/discussions

### Most Requested
1. Stata .dta file support
2. Do-file execution
3. Logistic regression
4. Panel data commands
5. Time series analysis

## Contributing

Want to help implement these features? See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Priority is given to features that:
- Benefit students learning statistics
- Are commonly used in coursework
- Maintain Stata compatibility
- Have clear use cases

## Release Schedule

- **Minor releases** (v1.x): Every months
- **Major releases** (v2.x): 3 months
- **Patch releases** (v1.x.y): As needed for bug fixes

## Feedback

Submit feature requests and bug reports at:
https://github.com/Statscrypt/Statscript-suite/issues
