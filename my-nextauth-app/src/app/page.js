// src/app/page.js
'use client';  // Adicione esta linha no topo
import { useState } from 'react';
import LoginModal from './componentes/LoginModal';

export default function Home() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  return (
    <div className="min-h-screen flex flex-col justify-center items-center p-4">
      <h1 className="text-2xl font-bold mb-4">Portal de Pagamentos VR3 Engenharia</h1>
      <button
        onClick={openModal}
        className="bg-blue-500 text-white py-2 px-4 rounded-md"
      >
        Entrar
      </button>

      {/* Exibe o modal quando isModalOpen for true */}
      <LoginModal isOpen={isModalOpen} onClose={closeModal} />
    </div>
  );
}
