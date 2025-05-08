import markdownItKatex from 'markdown-it-katex';
import { withMermaid } from "vitepress-plugin-mermaid";
import lightbox from "vitepress-plugin-lightbox"


export default withMermaid({
    title: 'Meson Structure',
    description: 'Documentation for meson-structure analysis',
    base: '/meson-structure/',

    // Improved head settings with proper KaTeX styling
    head: [
        ['link', { rel: 'stylesheet', href: 'https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.css' }],
        ['link', { rel: 'icon', type: 'image/png', href: '/favicon.png' }],
        ['meta', { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }],
    ],

    // Enhanced theme configuration
    themeConfig: {
        // Logo (create a simple logo and place it in docs/public/)
        logo: 'logo.png',

        // Improved navigation
        nav: [
            { text: 'Home', link: '/' },
            {
                text: 'Resources',
                items: [
                    { text: 'Wiki', link: 'https://wiki.jlab.org/cuawiki/index.php/Meson_Structure_Functions' },
                    { text: 'Meetings', link: 'https://wiki.jlab.org/cuawiki/index.php/EIC_Meson_SF_Meeting_Material_and_Summaries' },
                    { text: 'Data', link: '/data' },
                    { text: 'GitHub', link: 'https://github.com/JeffersonLab/meson-structure' }
                ]
            },
        ],

        // Expanded sidebar with better organization
        sidebar: [
            {
                text: 'Getting Started',
                collapsed: false, // Ensure this is not collapsed
                items: [
                    { text: 'Landing', link: '/' },
                    { text: 'Campaign 2025-03', link: '/campaign' },
                ]
            },
            {
                text: 'Data & Analysis',
                link: '/data',
                items: [
                    { text: 'Data Access', link: '/data' },
                    { text: 'MC Variables', link: '/mc-variables' },
                    { text: 'EDM4EIC Tree', link: '/edm4eic-tree' },
                    { text: 'Analysis', link: '/analysis' },

                ]
            },
            {
                text: 'Tutorials',
                link: '/tutorials',
                items: [
                    { text: 'Overview', link: '/tutorials' },
                    { text: '.1 Uproot', link: '/tutorials/01_using_uproot' },
                    { text: '.2 Metadata', link: '/tutorials/02_metadata' },
                    { text: '.3 References', link: '/tutorials/03_references' },
                ]
            },
            {
                text: 'Results',
                items: [
                    { text: 'Publications', link: '/publications' },
                    { text: 'Plots', link: '/plots' },
                ]
            }
        ],

        // Footer customization
        footer: {
            message: 'Released under the MIT License.',
            copyright: 'Copyright © 2025 Meson Structure Collaboration'
        },

        // Social links
        socialLinks: [
            { icon: 'github', link: 'https://github.com/JeffersonLab/meson-structure' }
        ],

        // Search configuration
        search: {
            provider: 'local'
        },

        // Layout customization for large screens
        outline: {
            level: [2, 3],
            label: 'On this page'
        },

        // Additional helpful features
        editLink: {
            pattern: 'https://github.com/JeffersonLab/meson-structure/edit/main/docs/:path',
            text: 'Edit this page on GitHub'
        },

        // Dark/Light theme toggle (enabled by default)
        appearance: true
    },

    // Enable KaTeX for math rendering
    markdown: {
        config: (md) => {
            md.use(markdownItKatex);
            md.use(lightbox, {});
        }
    },

    // Fix layout issues on large screens
    vite: {
        css: {
            preprocessorOptions: {
                scss: {
                    additionalData: `
            // Add any global SCSS variables here
          `
                }
            }
        }
    }
});