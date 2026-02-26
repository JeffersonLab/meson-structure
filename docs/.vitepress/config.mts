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
                ]
            },
            {
                text: 'Data',
                link: '/data',
                items: [
                    { text: 'Data Access', link: '/data' },
                    { text: 'CSV Data', link: '/data-csv' },
                    { text: 'Campaigns', link: '/campaigns' },
                ]
            },
            {
                text: 'Campaign 2026-03',
                link: '/campaign-2026-03/campaign-2026-03',
                items: [
                    {text: "Reco DIS All", link: '/campaign-2025-10/reco-dis-all'},
                ]
            },
            {
                text: 'Campaign 2025-10',
                link: '/campaign-2025-10/campaign-2025-10',
                items: [
                    {text: "Reco DIS All", link: '/campaign-2025-10/reco-dis-all'},
                ]
            },

            {
                text: 'Analysis',
                link: '/analysis',
                items: [
                    { text: 'Analysis', link: '/analysis' },
                    { text: 'MC Variables', link: '/mc-variables' },
                    { text: 'EDM4EIC Tree', link: '/edm4eic-tree' },
                    { text: 'EDM4EIC Diagram', link: '/edm4eic-diagram' },
                    { text: 'EDM4HEP Tree', link: '/edm4hep-tree' },
                ]
            },
            {
                text: 'Learning',
                link: '/tutorials',
                items: [
                    { text: 'Resources', link: '/learning'},
                    { text: 'Tutorials', link: '/tutorials:'},
                    { text: '&nbsp;&nbsp;&nbsp;&nbsp;Python CSV', link: '/tutorials/py-csv' },
                    { text: '&nbsp;&nbsp;&nbsp;&nbsp;Python EDM4EIC', link: '/tutorials/py-edm4eic-uproot' },
                    { text: '&nbsp;&nbsp;&nbsp;&nbsp;C++ EDM4EIC', link: '/tutorials/cpp-edm4eic' },
                    { text: '&nbsp;&nbsp;&nbsp;&nbsp;IFarm jobs', link: '/tutorials/ifarm' }
                ]
            },
            {
                text: 'Other',
                items: [
                    { text: 'Publications', link: '/publications' },
                    { text: 'Dynamic plots', link: '/eg-dynamic-plots' },
                    { text: 'Decay plots', link: '/plots_decays' },
                    { text: 'Manage website', link: '/manage-website' },
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