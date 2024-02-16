module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  parser: "vue-eslint-parser",
  extends: [
    "standard-with-typescript",
    "plugin:vue/vue3-recommended",
    "@unocss",
    "plugin:prettier/recommended",
    "./.eslintrc-auto-import.json",
  ],
  parserOptions: {
    parser: "@typescript-eslint/parser",
    ecmaVersion: "latest",
    sourceType: "module",
    project: ["./tsconfig.json", "./tsconfig.app.json", "./tsconfig.node.json"],
    extraFileExtensions: [".vue"],
  },
  plugins: ["vue", "@typescript-eslint"],
  rules: {
    // 关闭下面/// <reference path="..." />, /// <reference types="..." />,  /// <reference lib="..." /> 校验
    "@typescript-eslint/triple-slash-reference": "off",
  },
};
