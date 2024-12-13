const functions = require("firebase-functions");
const { exec } = require("child_process");
const path = require("path");

// Caminho absoluto para o diretório Backend
const backendDir = path.join(__dirname, "Backend");

// Função HTTP do Firebase que inicia o Flask (Python)
exports.api = functions.https.onRequest((req, res) => {
    console.log("Iniciando execução da aplicação Flask...");
    console.log(`Caminho do Backend: ${backendDir}`);

    // Comando para rodar o Flask
    const command = process.platform === "win32" ? "python app.py" : "python3 app.py";

    // Execução do comando no diretório especificado
    exec(command, { cwd: backendDir }, (error, stdout, stderr) => {
        if (error) {
            // Log detalhado do erro
            console.error("Erro completo:", error);
            console.error(`stderr: ${stderr}`);
            console.error(`stdout antes do erro: ${stdout}`);
            return res.status(500).send(`Erro ao rodar o Flask: ${stderr}`);
        }

        // Caso a execução seja bem-sucedida
        console.log("Flask executado com sucesso!");
        console.log(`Resposta do Flask: ${stdout}`);
        res.send(stdout); // Retorna a resposta do Flask para o cliente
    });
});
