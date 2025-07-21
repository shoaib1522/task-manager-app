// frontend/.eslintrc.cjs

module.exports = {
  root: true,
  env: { browser: true, es2020: true, node: true },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react/jsx-runtime',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parserOptions: { ecmaVersion: 'latest', sourceType: 'module' },
  settings: { react: { version: '18.2' } },
  plugins: ['react-refresh'],

  // --- THE FIX IS HERE ---
  // The 'globals' object must be a top-level property, NOT inside 'rules'.
  globals: {
    "vi": "readonly",
    "describe": "readonly",
    "it": "readonly",
    "expect": "readonly",
    "beforeEach": "readonly",
  },
  // --------------------

  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
  },
}