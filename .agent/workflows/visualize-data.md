---
description: "Generate diverse, publication-quality data visualizations using modern Python visualization libraries. Creates elegant, standalone charts with creative freedom and globally configurable output settings."
---

# visualize-data

Generate diverse, publication-quality data visualizations using modern Python visualization libraries. Creates elegant, standalone charts with creative freedom and globally configurable output settings.

## Global Configuration

Configure default visualization behavior at the top of generated scripts:

```python
# ==================== GLOBAL SETTINGS ====================
OUTPUT_FORMATS = ["png"]                    # Change to: ["png", "pdf", "svg"], ["html", "png"], etc.
OUTPUT_DPI = 300                            # Resolution (300=publication, 150=web)
OUTPUT_DIRECTORY = "visualizations"         # Output folder for all generated files
FIGURE_COUNT = 6                            # Number of standalone charts (range: 4-8)
COLOR_PALETTE = "husl"                      # Options: "husl", "deep", "pastel", "Set2", "Spectral"
STYLE_THEME = "seaborn-v0_8-darkgrid"      # Options: "default", "seaborn-v0_8-darkgrid", "ggplot", "bmh"
INTERACTIVE_ELEMENTS = True                 # Include interactive features where applicable
FIGURE_SIZE = (14, 10)                      # Base figure dimensions
# ============================================================
```

## Visualization Generation Approach

### Step 0: Data Exploration & Intelligence Gathering (CRITICAL)
Before planning any visuals, gain a deep understanding of the data structure and quality by writing and executing a **temporary exploration script**:
1. **Create Exploration Script**: Write a temporary file (e.g., `temp_data_exploration.py`) that performs the following:
   - **Schema Inspection**: `df.info()`, `df.columns`, and `df.head()` to understand names, types, and shape.
   - **Statistical Summary**: `df.describe(include='all')` to identify ranges, means, and potential outliers.
   - **Quality Audit**: Check for missing values (`df.isnull().sum()`) and unique value counts for categorical variables.
   - **Distribution Profiling**: Check skewness or `value_counts()` for key variables to identify data density.
   - **Relationship Scanning**: Check correlations (`df.corr()`) or cross-tabulations for specified variables.
2. **Execute & Analyze**: Run the script in the terminal, capture the output, and analyze the results to inform the visualization strategy.
3. **Automatic Cleanup**: **MANDATORY**: Delete the temporary exploration script immediately after gathering the necessary insights.

**Outcome**: Use these quantified insights to choose chart types that highlight real patterns rather than visualizing noise or empty categories.

### Step 1: Initialization & Planning (MANDATORY)
1. **Create a Todo List**: Immediately create a structured task list to track progress for this session. Update it as work progresses.
2. **Environment Setup**: Verify required libraries are available (pandas, matplotlib, seaborn, plotly, etc.). Install missing dependencies if needed.
3. **Output Directory Setup**: Create the output directory if it doesn't exist. Use `Path(output_directory).mkdir(parents=True, exist_ok=True)`.
4. **Insight Integration**: Review the findings from **Step 0**. Identify unique data characteristics, temporal/spatial aspects, and outliers that deserve specialized visual attention.
5. **Data Preprocessing**: Clean and prepare data (handle missing values, outliers, type conversions) based on the exploration phase. Document all preprocessing.
6. **MCP Documentation Lookup**: Use MCP tools (e.g., `mcp_exa_get_code_context_exa`) to retrieve up-to-date documentation and "best-in-class" code examples for the chosen visualization libraries (Seaborn, Plotly, etc.). Search for "publication quality [library] examples" or "advanced [chart type] styling".
7. **Creative Brainstorming**: Develop a plan for 4-8 unique perspectives. Define the specific analytical objective for each standalone chart and choose the optimal library for each specific visual. Apply creative intelligence to find "hidden" stories revealed during Step 0.

### Step 2: Standalone Chart Generation (Strictly Single Panel)
Generate 4-8 **separate, standalone visualizations** with creative freedom—each chart:
- **NO MULTI-PANEL VISUALS**: Each file must contain exactly one chart. No subplots, no faceted grids in one file, no dashboards.
- **File naming convention (MANDATORY)**: Files must be named with sequential numbering first, followed by a descriptive title related to the chart content. Format: `01_chart_title.png`, `02_chart_title.png`, `03_chart_title.png`, etc. The number (01-08) comes first, then an underscore, then a descriptive title that reflects what the chart shows (e.g., `01_distribution_analysis.png`, `02_scatter_with_regression.png`, `03_temporal_trends.png`).
- **Single perspective per file**: One focused insight per visualization. Layered elements (e.g., trendlines on scatter) are encouraged, but multiple axes/panels are forbidden.
- **Independent analysis**: Each chart stands alone with complete axis labels and captions.
- **No linking**: Charts are independent, not connected through interactive filters or selections.

### Step 3: Multi-Perspective Visualization Diversity
Select diverse chart types with creative freedom to choose from:

**Core Visualization Types**:
- Statistical distributions (violin plots, ridge plots, density curves)
- Relational analysis (scatter plots with regression/confidence intervals, joint distributions)
- Comparative patterns (box plots, categorical plots - each as a standalone file)
- Temporal trends (line charts, area plots, time-series decomposition)
- Multivariate relationships (heatmaps, correlation matrices, parallel coordinates)
- Advanced techniques (3D surfaces, animated transitions, interactive hover details)

**Inspiration from Modern Libraries**:
- **Plotly**: Interactive 3D visualizations, animated transitions, hover details
- **Seaborn**: Statistical graphics with automatic confidence intervals and aesthetic refinement
- **Altair**: Declarative visualizations (one chart per output)
- **Matplotlib**: Publication-ready static output with fine-grained customization
- **HoloViews/Bokeh**: Large dataset handling, interactive zooming (standalone charts only)
- **Polars integration**: High-performance data operations before visualization

**Creative Combination Strategies** (each as separate file):
- Distribution analysis with trend overlay
- Comparative breakdowns across categorical dimensions
- Temporal progression visualizations
- Relationship and correlation displays
- Network-style relationship diagrams
- Color-coded statistical analysis with annotations

### Step 4: Academic Publication Quality Standards
Ensure scholarly excellence through:
- **Visual clarity**: Appropriate chart selection for data patterns, clear labeling, logical color schemes
- **Statistical rigor**: Confidence intervals, significance markers, proper error representations
- **Aesthetic polish**: Professional typography, consistent styling, accessibility-compliant colors
- **Information efficiency**: High data-to-ink ratio, minimal decoration, focused visual hierarchy
- **Reproducibility**: Complete code documentation with random seed management for consistent results
- **Format flexibility**: Easy one-setting changes at script top for multiple output formats/resolutions

### Step 5: Code Generation & Execution
Produce professional Python scripts with:
- **Clean organization**: Imports section, global settings, helper functions, main visualization pipeline
- **Modular design**: Separate functions for each chart type enabling selective regeneration
- **Reproducibility**: Set random seeds (`np.random.seed(42)`, `random.seed(42)`) at the start for consistent results
- **File naming (MANDATORY)**: Use sequential numbering (01, 02, 03, etc.) followed by underscore and descriptive title related to the chart content. 
  - **Format**: `NN_chart_title.png` where NN is zero-padded number (01-08) and chart_title describes the visualization
  - **Examples**: `01_distribution_analysis.png`, `02_scatter_with_regression.png`, `03_temporal_trends.png`, `04_correlation_heatmap.png`
  - **Rules**: Number must come first, use zero-padding (01 not 1), descriptive title must relate to chart content, number sequentially from 01 up to total count (4-8)
- **Error handling**: Graceful handling of missing values, data type conversions, edge cases
- **Performance optimization**: Efficient data subsetting for large datasets, vectorized operations. For very large datasets (>100K rows), consider sampling or aggregation.
- **Memory management**: Close figures explicitly (`plt.close()` or `fig.close()`) to prevent memory leaks
- **Documentation**: Clear comments explaining each visualization's purpose and analytical approach
- **Extensibility**: Easy modification of chart parameters without touching core logic

### Step 6: Iterative Execution & Visual Review (MANDATORY)
1. **Run & Fix**: Execute the generated Python code. If errors occur (missing libraries, data type issues), fix them immediately and rerun until execution is 100% successful.
2. **File Verification**: Verify all expected output files were created. Check that file count matches the planned number of visualizations (4-8 files).
3. **Visual Quality Review**: Inspect the generated image files. If a chart looks "messy," "amateur," or "cluttered," **go back and refine the code** until the visual output is elegant, professional, and clean.
4. **Academic Publication Standards**: Check for visual clarity, professional typography, consistent styling, and accessibility-compliant colors. Ensure high data-to-ink ratio and focused visual hierarchy.
5. **Iterate Until Perfect**: Continue refining code and regenerating visuals until all charts meet publication-quality standards.
6. **Update Todo List**: Mark completed tasks in the todo list as work progresses.

### Step 7: Output Delivery & Concise Documentation
- **Minimal README**: Provide exactly ONE concise `README.md` in the output directory that includes:
  - Brief description of the analysis performed
  - List of generated visualizations with file names and brief descriptions
  - Data source information
  - Key insights or findings (if applicable)
  - Technical details (libraries used, DPI, formats)
- **Code Comments**: Ensure the Python script has clear comments explaining the purpose of each visualization function.

## Advanced Capabilities

### Creative Intelligence
- **Emergent pattern detection**: Identify unusual data relationships suggesting novel visualizations
- **Aesthetic Refinement**: Continuous iteration until visuals meet scholarly standards
- **Standalone multi-scale analysis**: Transition between aggregate and granular perspectives through separate files
- **Domain adaptation**: Real estate, finance, economics, and academic research contexts
- **Methodological soundness**: Econometric models, causal inference graphics, hypothesis visualization

### Standalone Chart Suite Design
- **Independent files**: Each chart saved separately with sequential naming starting from 01 (e.g., `01_distribution_analysis.png`, `02_scatter_with_regression.png`, `03_temporal_trends.png`, etc.)
- **File naming format**: Number first (01-08), then underscore, then descriptive title related to chart content
- **Self-contained visualizations**: Each chart stands alone with complete axis labels and captions
- **No dashboard linking**: Charts are independent, not connected through interactive filters
- **Portfolio approach**: Entire suite suitable for papers, presentations, or reports
- **Batch generation**: All charts generated in one run with consistent styling and palette

## Input Specifications

### Data Sources
- **Variable analysis**: "private_equity_ownership vs facility_closure_rate" (specify two variables)
- **Dataset path**: "path/to/data.csv" or "path/to/data.parquet" (Polars or Pandas)
- **DataFrame object**: Direct Python DataFrame with context instructions
- **Existing figure**: Path to image file for alternative design perspectives

### Query Format
- Minimal specification: "variable_x vs variable_y" with automatic creative choices
- Contextual hints: "senior housing markets", "real estate trends", "financial performance"
- Format requests: "--formats png,pdf,svg" (overrides global settings)
- Statistical options: "--with-regression --show-intervals --alpha 0.05"

## Usage Examples

### Example 1: Minimal Specification (Creative Freedom)
```
/visualize-data private_equity_ownership vs facility_closure_rate
```
**Result**: AI chooses 4-8 complementary standalone charts and a concise README summary.

### Example 2: Dataset Exploration
```
/visualize-data --dataset "data/senior_housing_panel.csv" --explore
```
**Result**: 4-8 independent visualization files (PNG) and a concise README explanation.

### Example 3: Format Override
```
/visualize-data revenue vs profit_margin --formats png,pdf,svg --dpi 300
```
**Result**: Each chart generated in all format variants with sequential numbering and descriptive titles (e.g., `01_distribution_analysis.png`, `01_distribution_analysis.pdf`, `01_distribution_analysis.svg`, `02_scatter_with_regression.png`, etc.)

### Example 4: Context-Driven Analysis
```
/visualize-data --dataset "data/finance.csv" --context "portfolio diversification effects"
```
**Result**: 4-6 separate, self-contained PNG files with domain-specific insights

### Example 5: Large Dataset Exploration
```
/visualize-data --dataset "data/transactions.parquet" --large-dataset
```
**Result**: Efficient rendering with optimized chart types for millions of data points, each saved individually

## Visualization Examples Generated

### Statistical Distribution Analysis (Separate File)
- Violin plots with categorical overlays showing distribution characteristics

### Relational Patterns (Separate File)
- Scatter plots with regression lines and confidence intervals (95%)

### Comparative Analysis (Separate File)
- Box plots with individual data points and statistical annotations

### Temporal Trends (Separate File)
- Line charts with confidence bands

### Advanced Multivariate (Separate File)
- 3D surface plots for continuous response surfaces or correlation heatmaps

### Supplementary Perspective (Separate File)
- Network graphs, parallel coordinates, or domain-specific visualization

## Quality Assurance Process

### Data Validation
- Missing value detection and impact assessment
- Outlier identification with statistical justification
- Distribution shape analysis (skewness, kurtosis)
- Data type verification and smart conversion

### Visual Testing
- **No multi-panel check**: Verify each output file contains exactly one chart.
- **Aesthetic verification**: Review actual generated image files. If visuals appear unprofessional, cluttered, or amateur, refine the code and regenerate until charts are elegant and publication-ready.
- Information-to-ink ratio optimization
- Accessibility color scheme verification
- Typography consistency and readability

### Methodological Rigor
- Appropriate statistical test selection
- Confidence interval calculation methods
- Multiple comparison correction where applicable
- Effect size reporting alongside p-values

### Output Verification
- File format generation confirmation
- Resolution and DPI correctness
- File count verification (matches expected 4-8 visualizations)
- File size reasonableness (not unexpectedly large or small)
- Cross-platform rendering consistency
- All files readable and properly formatted

## Common Pitfalls to Avoid

- **Multi-panel visuals**: Never create subplots, faceted grids, or dashboards in a single file
- **Forgotten figure cleanup**: Always call `plt.close()` or `fig.close()` after saving to prevent memory issues
- **Stale exploration scripts**: Always delete temporary data exploration scripts (`temp_data_exploration.py`) after use
- **Inconsistent styling**: Use global matplotlib rcParams settings for consistent fonts, sizes, and colors
- **Missing error handling**: Handle missing data, empty datasets, and edge cases gracefully
- **Poor file naming**: Use sequential numbering first (01, 02, 03, etc.), then underscore, then descriptive title related to chart content. Format must be `01_chart_title.png`, not generic names or titles without numbers.
- **Skipping visual review**: Always inspect actual output files, not just code
- **No reproducibility**: Always set random seeds for any random operations
- **Large file sizes**: For high DPI outputs, consider file size implications

## Success Metrics

- ✅ **Data Intelligence**: Initial exploration performed via temporary script to understand distributions and statistics before coding. Cleanup of temp scripts confirmed.
- ✅ **Diverse standalone charts**: 4-8 complementary visualizations with different analytical perspectives
- ✅ **Strictly single panel**: Every file contains exactly one chart; NO subplots or grids.
- ✅ **Validated Execution**: Code runs successfully and generates all files.
- ✅ **Visual Excellence**: Charts have been reviewed and refined for a clean, professional look.
- ✅ **Concise Documentation**: One minimal README explaining the suite.
- ✅ **Independent files**: Each chart as standalone file with complete context and labeling
- ✅ **Publication ready**: High DPI, clear labeling, professional styling, color-blind accessible
- ✅ **Reproducible**: Complete code documentation, random seed management, data provenance tracking
- ✅ **Creative Intelligence**: Visuals reveal non-obvious patterns identified during the exploration phase.

## Technical Stack

**Core Libraries**:
- Matplotlib/Seaborn: Static publication-quality plots (NO subplots). Use `plt.close()` after each figure.
- Plotly: Interactive 3D and animated visualizations. Use `kaleido` for static exports.
- Altair: Declarative charts (one per output)
- Pandas/Polars: Data manipulation and preparation

**Output Rendering**:
- Matplotlib backends for PNG/PDF/SVG
- Plotly HTML export for interactive web viewing
- Cairo/Pillow for format conversion
- Kaleido for Plotly raster outputs

**Best Practices**:
- Always set `bbox_inches='tight'` when saving matplotlib figures for clean edges
- Use `facecolor='white'` to ensure consistent backgrounds
- For large datasets, use `sns.scatterplot()` with `alpha` parameter or sample data before plotting
- Set figure size before creating plots: `fig, ax = plt.subplots(figsize=(14, 10))`
- Use consistent font settings across all charts (see matplotlib rcParams configuration)
