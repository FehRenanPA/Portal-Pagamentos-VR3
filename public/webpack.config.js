const Dotenv = require('dotenv-webpack');

module.exports = {
    // Outras configurações do Webpack

    plugins: [
        new Dotenv()
    ],
    
    // Outras configurações como entrada, saída, etc.
};
