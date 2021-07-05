const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
    mode: "jit",
    purge: [
        './potluck/**/*.html',
        './potluck/**/*.js',
    ],
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {
            screens: {
                // Approx. iPhone 5 horizontal orientation
                "xs": "560px",
                ...defaultTheme.screens,
            }
        },
    },
    // variants: {
    //   extend: {
    //    backgroundColor: ['active'],
    //    textColor: ['active'],
    //   }
    // },
    plugins: [],
}
