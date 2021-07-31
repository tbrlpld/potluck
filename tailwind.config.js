const defaultTheme = require('tailwindcss/defaultTheme')
const colors = require('tailwindcss/colors')

module.exports = {
    mode: "jit",
    purge: [
        './potluck/**/*.html',
        './potluck/**/*.js',
    ],
    darkMode: false, // or 'media' or 'class'
    theme: {
        colors: {
            ...colors,
            primary: colors.blueGray,
        },
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
