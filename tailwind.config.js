module.exports = {
    mode: "jit",
    purge: [
        './potluck/**/*.html',
        './potluck/**/*.js',
    ],
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {},
    },
    // variants: {
    //   extend: {
    //    backgroundColor: ['active'],
    //    textColor: ['active'],
    //   }
    // },
    plugins: [],
}
