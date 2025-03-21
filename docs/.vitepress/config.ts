import markdownItKatex from 'markdown-it-katex';

export default {
    title: 'Meson Structure',
    description: 'Documentation for meson-structure analysis',
    base: '/meson-structure/',

    // Improved head settings with proper KaTeX styling
    head: [
        ['link', { rel: 'stylesheet', href: 'https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.css' }],
        ['link', { rel: 'icon', type: 'image/png', href: '/logo.png' }],
        ['meta', { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }],
    ],

    // Enhanced theme configuration
    themeConfig: {
        // Logo (create a simple logo and place it in docs/public/)
        logo: '/logo.png',

        // Improved navigation
        nav: [
            { text: 'Home', link: '/' },
            { text: 'Documentation', link: '/mc-variables' },
            { text: 'GitHub', link: 'https://github.com/JeffersonLab/meson-structure' },
        ],

        // Expanded sidebar with better organization
        sidebar: [
            {
                text: 'Getting Started',
                collapsed: false, // Ensure this is not collapsed
                items: [
                    { text: 'Introduction', link: '/' },
                    { text: 'Campaign 2025-03', link: '/campaign' },
                ]
            },
            {
                text: 'Data & Analysis',
                items: [
                    { text: 'Data Access', link: '/data' },
                    { text: 'MC Variables', link: '/mc-variables' },
                    { text: 'Analysis Guide', link: '/analysis' },
                ]
            },
            {
                text: 'Results',
                items: [
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
            pattern: 'https://github.com/yourusername/meson-structure/edit/main/docs/:path',
            text: 'Edit this page on GitHub'
        },

        // Dark/Light theme toggle (enabled by default)
        appearance: true
    },

    // Enable KaTeX for math rendering
    markdown: {
        config: (md) => {
            md.use(markdownItKatex);
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
};