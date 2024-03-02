module.exports = {
  purge: [
    './src/**/*.html',
    './src/**/*.js',
    './src/**/*.css',
    './src/**/*.img',
    './src/**/*.tailwind-favicons',

  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      zIndex: {
        '-1': '-1',
      },
      flexGrow: {
        '5' : '5'
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
