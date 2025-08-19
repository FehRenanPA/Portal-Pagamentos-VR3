module.exports = {
  env: {
    browser: true,
    node: true,
    es6: true, // Habilitar suporte a recursos ES6
  },
  parserOptions: {
    ecmaVersion: 2021, // Definindo a versão do ECMAScript como 2021 (suporta recursos ES6+)
    sourceType: 'module', // Permite usar módulos (import/export)
  },
  rules: {
    'no-unused-vars': ['warn', { 'varsIgnorePattern': 'logger' }],
    'prefer-const': 'error', // Garante que 'const' seja preferido em vez de 'let'
    // Adicione outras regras conforme necessário
  },
};
