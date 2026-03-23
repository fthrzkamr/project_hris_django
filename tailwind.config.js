/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/templates/**/*.html',
    './**/static/**/*.js',
  ],
  safelist: [
    'btn', 'btn-ghost', 'btn-circle', 'btn-primary', 'btn-secondary', 'btn-accent', 'btn-info', 'btn-success', 'btn-warning', 'btn-outline', 'btn-sm',
    'navbar', 'navbar-start', 'navbar-center', 'navbar-end',
    'menu', 'menu-title',
    'card', 'card-body', 'card-title',
    'stats', 'stats-vertical', 'stats-horizontal', 'stat', 'stat-title', 'stat-value', 'stat-desc', 'stat-figure',
    'timeline', 'timeline-vertical', 'timeline-start', 'timeline-middle', 'timeline-end', 'timeline-box',
    'dropdown', 'dropdown-content', 'dropdown-end',
    'avatar', 'placeholder',
    'alert', 'alert-info',
    'tooltip', 'tooltip-right',
    'badge',
    'bg-base-100', 'bg-base-200', 'bg-base-300',
    'text-primary', 'text-primary-content', 'text-secondary', 'text-accent', 'text-neutral', 'text-info', 'text-success', 'text-warning', 'text-error',
    'bg-primary', 'bg-secondary', 'bg-accent', 'bg-neutral', 'bg-info', 'bg-success', 'bg-warning', 'bg-error',
    'rounded-box', 'gap-2',
  ],
  theme: {
    extend: {
      fontFamily: {
        'poppins': ['Poppins', 'sans-serif'],
      },
    },
  },
  plugins: [require('daisyui').default || require('daisyui')],
  daisyui: {
    themes: [
      {
        hris: {
          "primary": "#0d9488",           // Teal-600
          "primary-content": "#ffffff",
          "secondary": "#14b8a6",         // Teal-500
          "accent": "#0f766e",            // Teal-700
          "neutral": "#1e293b",           // Slate-800
          "base-100": "#ffffff",
          "base-200": "#f8fafc",          // Slate-50
          "base-300": "#f1f5f9",          // Slate-100
          "info": "#0ea5e9",
          "success": "#22c55e",
          "warning": "#f59e0b",
          "error": "#ef4444",
        },
      },
    ],
    styled: true,
    base: true,
    utils: true,
    logs: false,
  },
}
