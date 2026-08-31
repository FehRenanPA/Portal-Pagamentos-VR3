// firebase-config.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/9.23.0/firebase-auth.js";

// Configuração do Firebase
const firebaseConfig = {
    apiKey: "AIzaSyD10AX72GASmdiTl9rhlGrUm7vLHz2yNzw",
    authDomain: "portal-pagamento-vr3.firebaseapp.com",
    projectId: "portal-pagamento-vr3",
    storageBucket: "portal-pagamento-vr3.appspot.com",
    messagingSenderId: "705628574086",
    appId: "1:705628574086:web:43a2e4553f309607381c07",
};

// Inicializa o Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { app, auth };
