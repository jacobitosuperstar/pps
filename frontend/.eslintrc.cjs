module.exports = {
  env: {
    browser: true,
    es2021: true,
    "vitest-globals/env": true,
  },
  extends: [
    "plugin:react/recommended",
    "standard",
    "prettier",
    "plugin:vitest-globals/recommended",
  ],
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: "latest",
    sourceType: "module",
  },
  plugins: ["react", "@typescript-eslint", "vitest"],
  rules: {
    "react/react-in-jsx-scope": "off",
  },
};
