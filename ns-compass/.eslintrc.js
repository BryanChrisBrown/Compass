module.exports = {
  env: {
    browser: true,
    es2020: true,
  },
  extends: [
    'plugin:react/recommended',
    'airbnb',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 11,
    sourceType: 'module',
  },
  plugins: [
    'react',
    // '@typescript-eslint',
  ],
  rules: {
    'linebreak-style': 'off',
    quotes: 'warn',
    'react/jsx-filename-extension': 'off',
    'react/destructuring-assignment': 'off',
    'no-use-before-define': 'warn',
    'space-before-function-paren': 'off',
    camelcase: 'off',
    'jsx-a11y/anchor-is-valid': 'off',
    'jsx-a11y/click-events-have-key-events': 'off',
    'jsx-a11y/interactive-supports-focus': 'off',
  },
};
