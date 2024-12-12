const functions = require("firebase-functions");
const { exec } = require("child_process");
const path = require("path");

const backendDir = path.join(__dirname, "functions", "Backend");

exports.api = functions
  .https
  .onRequest((req, res) => {
    console.log("Chamando a aplicação Flask...");
    console.log(`Caminho do Backend: ${backendDir}`);

    exec("python app.py", { cwd: backendDir }, (error, stdout, stderr) => {
        if (error) {
            console.error(`Erro ao executar Flask: ${stderr}`);
            return res.status(500).send(`Erro ao rodar o Flask: ${stderr}`);
        }

        console.log(`Resposta do Flask: ${stdout}`);
        res.send(stdout);  // Enviar a resposta do Flask para o cliente
    });
});
