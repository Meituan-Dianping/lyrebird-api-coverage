module.exports = {
  env: {
    browser: true,
    es6: true,
  },
  extends: [
    'plugin:vue/essential',
    'airbnb-base',
  ],
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly',
  },
  parserOptions: {
    ecmaVersion: 2018,
    sourceType: 'module',
  },
  plugins: [
    'vue',
  ],
  rules: {
    quotes: [1, "single"], //引号类型
    "quote-props": [2, "as-needed"], // 双引号自动变单引号
    semi: [2, "never"], //分号
    "comma-dangle": [1, "always-multiline"], // 对象或数组多行写法时，最后一个值加逗号
    "space-after-keywords": [0, "always"], //关键字后面是否要空一格
    "comma-dangle": [2, "always-multiline"], // 逗号
  },
};
