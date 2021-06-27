module.exports = {
    purge: [
        './potluck/**/*.html',
        './potluck/**/*.js',
    ],
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {},
    },
    variants: {
      extend: {
       backgroundColor: ['active'],
      }
    },
    plugins: [],
}
