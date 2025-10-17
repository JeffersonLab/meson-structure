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
