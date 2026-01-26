# Managing website

 **The website is**:

- a part of the [meson-structure](https://github.com/JeffersonLab/meson-structure) repository. Sources at [docs/](https://github.com/JeffersonLab/meson-structure/tree/main/docs)
- updated automatically on every commit to the `main` branch
- if there are errors building the website, they will be visible on the [GitHub Actions](https://github.com/JeffersonLab/meson-structure/actions) page
- built using [VitePress](https://vitepress.vuejs.org/) and hosted on [GitHub Pages](https://pages.github.com/)


## Directory Structure

- All website content is stored in [docs/](https://github.com/JeffersonLab/meson-structure/tree/main/docs)
- Side menu is defined in [docs/.vitepress/config.ts](https://github.com/JeffersonLab/meson-structure/blob/main/docs/.vitepress/config.mts#L38)
- Images/resources and markdown texts are separated in directories (but all are inside [docs/](https://github.com/JeffersonLab/meson-structure/tree/main/docs)).
  - Markdown/Text files are stored in `docs/...`
  - Images are stored in `docs/public/...`
  ```bash
    # text:
    docs/campaign-YYYY-MM/my-study.md
    # images:
    docs/public/analysis/campaign-YYYY-MM/my-study/5x41/01_example.jpg
  ```
  - VitePress automatically copies all files from `docs/public/` to resulting site root during the build process. So to reference an image one can
  ```markdown
    # image references (without docs/public):
    ![example](/analysis/campaign-2025-08/my-study/5x41/01_example.jpg)
  ```


### Analysis results

According to the above (and also EIC guidelines)

- **Place analysis markdown documentation in:**
  ```
  docs/campaign-YYYY-MM/<analysis-name>.md
  ```

  *Example:*

  ```
  docs/campaign-2025-08/acceptance.md
  docs/campaign-2025-08/acceptance_ff.md
  ```

- **Place plots by beam energy in:**
  ```
  docs/public/analysis/campaign-YYYY-MM/<analysis-topic>/<beam-energy>/
  ```

  *Example:*
  ```
  docs/public/analysis/campaign-2025-08/acceptance/5x41/01_example.png
  docs/public/analysis/campaign-2025-08/acceptance/10x100/01_example.png
  ```

- Reference images in markdown files, you use absolute paths starting from `docs/public/`:

  *Example:*

  > If image is located on the disk at:
  >
  > ```
  > docs/public/analysis/campaign-2025-08/acceptance/5x41/01_example.png
  > ```
  >
  > Reference it in markdown as:
  >
  > ```markdown
  > ![Description](/analysis/campaign-2025-08/acceptance/5x41/01_example.png)
  > ```

## Naming Conventions

**Files:** Use lowercase with underscores
- `acceptance_study.md`
- `lambda_decay_kinematics.md`

**Images:** Prefix with numbers for ordering
- `01_q2_distribution.png`
- `02_t_spectrum.png`
- `03_xbj_correlation.png`


## Vue Components for Analysis Pages

Custom Vue components are available to create interactive analysis pages with energy comparison features.
Components are located in `docs/.vitepress/theme/components/`.

### BeamEnergyCompareViewer & BeamEnergyComparePlot

These components work together to display plots across different beam energies with comparison capabilities.

**Features:**
- Configure plot sources (paths) per page - no hardcoded paths
- Automatically generates dropdown options for single energies and all pairwise comparisons
- Global selector controls all plots on the page
- Each plot also has an individual selector for flexible viewing

**Basic Usage:**

```md
<script setup>
const sources = {
  '5×41 GeV': '/analysis/campaign-2025-08/acceptance/5x41/',
  '10×100 GeV': '/analysis/campaign-2025-08/acceptance/10x100/',
  '10×130 GeV': '/analysis/campaign-2025-08/acceptance/10x130/',
  '18×275 GeV': '/analysis/campaign-2025-08/acceptance/18x275/'
}
</script>

# My Analysis Page

<BeamEnergyCompareViewer :sources="sources">

## Section Title

<BeamEnergyComparePlot
  plot-name="01_my_plot.png"
  title="My Plot Title"
  description="Description of what this plot shows."
/>

<BeamEnergyComparePlot
  plot-name="02_another_plot.png"
  title="Another Plot"
/>

</BeamEnergyCompareViewer>
```

**How it works:**

1. Define a `sources` object in `<script setup>` mapping labels to base paths
2. Wrap your content with `<BeamEnergyCompareViewer :sources="sources">`
3. Use `<BeamEnergyComparePlot>` for each plot, specifying only the filename

**The `sources` object:**

```js
const sources = {
  'label1': '/path/to/label1/plots/',
  'label2': '/path/to/label2/plots/',
  // ... more labels
}
```

- **Keys** are displayed directly as dropdown labels (use any format you want)
- **Values** are base paths where plots are stored
- Comparisons are auto-generated for all pairs (e.g., "label1 vs label2")

**BeamEnergyComparePlot props:**

| Prop | Required | Description |
|------|----------|-------------|
| `plot-name` | Yes | Filename of the plot (e.g., `"01_decay_points.png"`) |
| `title` | No | Title displayed above the plot |
| `description` | No | Description text below the title |

**Example for a different campaign:**

```md
<script setup>
const sources = {
  '5×41 GeV': '/analysis/campaign-2025-10/kinematics/5x41/',
  '18×275 GeV': '/analysis/campaign-2025-10/kinematics/18x275/'
}
</script>

<BeamEnergyCompareViewer :sources="sources">

<BeamEnergyComparePlot
  plot-name="q2_distribution.png"
  title="Q² Distribution"
/>

</BeamEnergyCompareViewer>
```

**Example comparing campaign versions:**

```md
<script setup>
const sources = {
  'Campaign 2025-08': '/analysis/campaign-2025-08/results/',
  'Campaign 2025-10': '/analysis/campaign-2025-10/results/'
}
</script>

<BeamEnergyCompareViewer :sources="sources">

<BeamEnergyComparePlot plot-name="summary.png" title="Summary" />

</BeamEnergyCompareViewer>
```

**Generated dropdown options:**

For sources with keys `['5×41 GeV', '10×100 GeV', '10×130 GeV', '18×275 GeV']`, the dropdown will show:

- **Single:** 5×41 GeV, 10×100 GeV, 10×130 GeV, 18×275 GeV
- **Comparisons:** 5×41 GeV vs 10×100 GeV, 5×41 GeV vs 10×130 GeV, etc.


## Run locally

To preview the website on your local machine
you need to have [Node.js](https://nodejs.org/en/) installed.
If it is not installed yet, e.g. use volta:

Install dependencies (first time only):

```bash
cd meson-structure/docs
npm install
```

Start development server (run command in docs/ directory):

```bash
npm run dev
```

Open your browser to the URL shown (typically localhost:5173)
The development server will automatically reload when you make changes to markdown files.
