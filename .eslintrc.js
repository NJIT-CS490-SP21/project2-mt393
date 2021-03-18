module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: ["eslint:recommended", "plugin:react/recommended", "airbnb", "airbnb/hooks", "prettier"],
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: "module",
  },
  plugins: ["react"],
  rules: {
    "react/no-array-index-key": "off",
    "react-hooks/exhaustive-deps": "off",
    "react/jsx-filename-extension": "off"
  },
};
