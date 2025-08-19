import { auth } from "./firebase-config.js";
import { onAuthStateChanged, signInWithEmailAndPassword, signOut } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-auth.js";

// Elementos da interface
const loginSection = document.getElementById("login-section");
const logoutSection = document.getElementById("logout-section");
const tabsSection = document.getElementById("tabs-section");
const userEmail = document.getElementById("user-email");
const errorMessage = document.getElementById("error-message");
const loginButton = document.getElementById("login-btn");
const logoutButton = document.getElementById("logout-btn");
const lista = document.getElementById('lista');
const recibo = document.getElementById('recibo');

// Controle de redirecionamento
let hasCheckedAuth = false;

// Função para exibir a seção de login
function showLoginSection() {
    if (loginSection) loginSection.style.display = 'block';
    if (logoutSection) logoutSection.style.display = 'none';
    if (tabsSection) tabsSection.style.display = 'none';
    if (lista) lista.style.display = 'none';
    if (recibo) recibo.style.display = 'none';
}

// Função para exibir a seção de logout e as abas de funcionalidade
function showLogoutSection(userEmailText) {
    if (loginSection) loginSection.style.display = 'none';
    if (logoutSection) logoutSection.style.display = 'block';
    if (tabsSection) tabsSection.style.display = 'block';
    if (userEmail) userEmail.textContent = userEmailText; // Exibe o e-mail do usuário
    showTab('lista'); // Exibe a aba de lista de funcionários ao fazer login
}

// Função para exibir a aba correspondente
function showTab(tabName) {
    // Ocultar todas as abas
    if (lista) lista.style.display = 'none';
    if (funcionarios) funcionarios.style.display = 'none';
    if (recibo) recibo.style.display = 'none';

    // Exibir a aba correspondente
    const tab = document.getElementById(tabName);
    if (tab) tab.style.display = 'block';
}

// Verifica o estado de autenticação
onAuthStateChanged(auth, (user) => {
    if (!hasCheckedAuth) {
        hasCheckedAuth = true;
        const currentPath = window.location.pathname;

        if (!user) {
            // Redireciona para login se não autenticado
            if (!currentPath.endsWith("login.html")) {
                window.location.href = "login.html";
            }
        } else {
            // Redireciona para o dashboard se autenticado
            if (currentPath.endsWith("login.html")) {
                window.location.href = "index.html";
            } else {
                showLogoutSection(user.email);
            }
        }
    }
});

if (loginButton) {
    loginButton.addEventListener("click", async () => {
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        console.log("Tentando login com:", email);

        errorMessage.textContent = ""; // Limpa mensagens de erro

        if (email && password) {
            try {
                const userCredential = await signInWithEmailAndPassword(auth, email, password);
                console.log("Login bem-sucedido. Redirecionando para index.html.");
                window.location.href = "index.html";
            } catch (error) {
                console.error("Erro durante o login:", error);
                mostrarErroLogin(error);
            }
        } else {
            console.warn("Campos de email ou senha estão vazios.");
            errorMessage.textContent = "Por favor, preencha todos os campos.";
        }
    });
}



// Mostra erros no login
function mostrarErroLogin(error) {
    if (error.code === "auth/user-not-found") {
        errorMessage.textContent = "Usuário não encontrado.";
    } else if (error.code === "auth/wrong-password") {
        errorMessage.textContent = "Senha incorreta.";
    } else {
        errorMessage.textContent = "Erro: " + error.message;
    }
}

// Logout
if (logoutButton) {
    logoutButton.addEventListener("click", () => {
        signOut(auth)
            .then(() => {
                // Limpar a interface e redirecionar para login
                showLoginSection();
                window.location.href = "login.html";
            })
            .catch((error) => {
                console.error("Erro ao sair:", error);
            });
    });
}

// Inicializa a interface com base no estado de autenticação
window.onload = function() {
    showLoginSection(); // Exibe a seção de login ao carregar a página
};
