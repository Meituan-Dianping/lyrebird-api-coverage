module.exports = {
  env: {
    browser: true,
    es6: true,
  },
  extends: ['plugin:vue/essential', 'airbnb-base'],
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly',
  },
  parserOptions: {
    ecmaVersion: 2018,
    sourceType: 'module',
  },
  plugins: ['vue'],
  rules: {
    quotes: [1, 'single'], //引号类型
    'quote-props': [2, 'as-needed'], // 双引号自动变单引号
    semi: [2, 'never'], //分号
    'comma-dangle': [1, 'always-multiline'], // 对象或数组多行写法时，最后一个值加逗号
    'space-after-keywords': [0, 'always'], //关键字后面是否要空一格
    'comma-dangle': [2, 'always-multiline'], // 逗号
    'no-param-reassign': 0, //禁止给参数重新赋值
    'no-bitwise': 0, //禁止使用按位运算符
    'no-restricted-syntax': 0,
    'vue/no-side-effects-in-computed-properties': 0,
    'import/no-unresolved': 0,
    'no-prototype-builtins': 0,
    'consistent-return': 0,
  },
};
