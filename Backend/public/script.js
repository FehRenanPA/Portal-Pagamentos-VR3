
   
     function showTab(tab) {
        const tabs = document.querySelectorAll('.tab');
        tabs.forEach(t => {
            t.classList.remove('active');
        });
        document.getElementById(tab).classList.add('active');
    }


<<<<<<< HEAD
=======

>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
    document.addEventListener('DOMContentLoaded', () => {
        fetchCargos();
        document.getElementById('name_funcionario').value = '';
        showTab('lista'); // Mostra a aba de cargos ao carregar
    });
<<<<<<< HEAD
    function baixarArquivoExcel() {
        // Define a URL do endpoint para download
        const url = "http://localhost:5000/baixar_excel";

        // Redireciona para a URL para iniciar o download
        window.location.href = url;
    }

=======
 //________________________Baixar Excell_________________________________________ 

  //---- Função para carregar os checkboxes dentro do modal
  function carregarCheckboxes(opcoes) {
    const container = document.getElementById('lista-arquivos-excel');
    container.innerHTML = ''; // Limpa as opções anteriores

    // Filtra as equipes distintas
    const equipesUnicas = new Set(opcoes.map(opcao => opcao.equipe));  // Extrai e filtra as equipes únicas

    // Adiciona os checkboxes ao modal
    equipesUnicas.forEach(equipe => {
        const checkboxWrapper = document.createElement('div');
        checkboxWrapper.classList.add('checkbox-wrapper');  // Aplica a classe CSS

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = equipe; // Usando o nome da equipe para identificar a opção

        const label = document.createElement('label');
        label.textContent = equipe;  // Exibe o nome da equipe

        checkboxWrapper.appendChild(checkbox);
        checkboxWrapper.appendChild(label);
        container.appendChild(checkboxWrapper);
    });
}   

// Função para capturar os arquivos selecionados
function baixarArquivoExcelSelecionado() {
    const checkboxes = document.querySelectorAll('#lista-arquivos-excel input[type="checkbox"]:checked');
    const selecionados = Array.from(checkboxes).map(checkbox => checkbox.value);

    if (selecionados.length > 0) {
        alert("Equipes selecionadas: " + selecionados.join(", "));
        console.log("Equipes selecionadas:", selecionados);
        // Aqui você pode realizar a ação com as equipes selecionadas
    } else {
        alert("Por favor, selecione ao menos uma equipe!");
    }
}

// Função para fechar o modal
function fecharModalExcel() {
    document.getElementById("modal-excel").style.display = "none";
}

// Função para abrir o modal quando o botão for clicado
function abrirModalExcel() {
    // Realiza uma requisição para o backend para buscar as equipes
    fetch('http://127.0.0.1:5000/api/listar_documentos')
        .then(response => response.json())
        .then(data => {
            // Carrega as equipes no modal, passando os dados recebidos do servidor
            carregarCheckboxes(data);
            // Exibe o modal
            document.getElementById("modal-excel").style.display = "flex";
        })
        .catch(error => console.error("Erro ao carregar equipes:", error));
}

// Função para formatar a data no formato "dd/mm/yy"
function formatarData(data) {
    const partes = data.split('-'); // Divide a data no formato "yyyy-mm-dd"
    const ano = partes[0].slice(-2); // Obtém os últimos dois dígitos do ano
    const mes = partes[1];
    const dia = partes[2];
    return `${dia}/${mes}/${ano}`; // Retorna no formato "dd/mm/yy"
}
//---- Envia dados de data e Equipe para gerar o relatorio

function baixarArquivoExcelSelecionado() {
    // Captura as datas
    const dataInicioInput = document.getElementById('data_inicio_relatorio').value;
    const dataFimInput = document.getElementById('data_fim_relatorio').value;

    // Formatação
    const dataInicio = formatarData(dataInicioInput);
    const dataFim = formatarData(dataFimInput);

    // Captura as equipes selecionadas
    const checkboxes = document.querySelectorAll('#lista-arquivos-excel input[type="checkbox"]:checked');
    const equipesSelecionadas = Array.from(checkboxes).map(checkbox => checkbox.value);

    // Validações
    if (!dataInicio || !dataFim) {
        alert("Por favor, preencha as datas de início e fim!");
        return;
    }

    if (equipesSelecionadas.length === 0) {
        alert("Por favor, selecione ao menos uma equipe!");
        return;
    }

    // Log para depuração: verificar o conteúdo das variáveis antes de enviar
    console.log("Data Início:", dataInicio);
    console.log("Data Fim:", dataFim);
    console.log("Equipes Selecionadas:", equipesSelecionadas);

    // Monta o payload para a API /api/relatorio_periodo
    const payloadRelatorio = {
        equipe: equipesSelecionadas,
        data_inicio: dataInicio,
        data_fim: dataFim
    };

    console.log("Payload Enviado:", payloadRelatorio); // Verifique se o payload está correto

    fetch('http://127.0.0.1:5000/api/relatorio_periodo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payloadRelatorio)
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // Recebe os dados da API /api/relatorio_periodo
        } else {
            return response.json().then(errorData => {
                throw new Error(errorData.erro || errorData.message || "Erro desconhecido ao buscar o relatório.");
            });
        }
    })
    .then(data => {
        console.log("Resposta da API /api/relatorio_periodo:", data);
    
        const documentos = Array.isArray(data) ? data : data.documentos;
    
        if (!documentos || documentos.length === 0) {
            throw new Error("Não há documentos disponíveis para gerar o relatório.");
        }
    
        const payloadGerarRelatorio = {
            documentos: documentos
        };
    
        return fetch('http://127.0.0.1:5000/api/gerar_relatorio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payloadGerarRelatorio)
        });
    })
    .then(response => {
        if (response.ok) {
            return response.blob(); // Recebe o arquivo gerado como Blob
        } else {
            return response.json().then(errorData => {
                throw new Error(errorData.erro || errorData.message || "Erro ao gerar o relatório.");
            });
        }
    })
    .then(blob => {
        // Dispara o download do arquivo gerado
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'relatorio_gerado.xlsx'; // Nome sugerido para o download
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url); // Limpa o recurso criado
    })
    .catch(error => {
        console.error("Erro ao gerar o relatório:", error);
        alert(`Erro ao gerar o relatório: ${error.message}`);
    });     
}






//_______________________Lista de Funcionarios ________________________________
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
    async function fetchCargos() {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/funcionarios'); 
            if (!response.ok) throw new Error('Network response was not ok');
            const funcionarios = await response.json();
            
        
            
            const funcionarioSelect = document.getElementById('name_funcionario');
            const listaFuncionarios = document.getElementById('lista-funcionarios');
            const totalRegistrosElement = document.getElementById('total-registros');


            funcionarioSelect.innerHTML = ''; // Limpa as opções existentes
            listaFuncionarios.innerHTML = ''; // Limpa a lista existente
            //listaCargos.appendChild(table); // Adiciona a tabela ao elemento


            
            // Cria uma tabela dinamicamente
            const table = document.createElement('table');
            table.style.width = '100%'; // Ajusta a largura da tabela
            table.innerHTML = `
                <thead>
                    <tr>
                        <th>Funcionario</th>
<<<<<<< HEAD
=======
                        <th>Equipe </th>
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
                        <th>Função </th>
                        <th>CPF</th>
                        <th>Chave PIX</th>
                        <th>Hora Base (%)</th>
                        <th>Repouso Remunerado (%)</th>
                        <th>Hora Extra 50%</th>
                        <th>Hora Extra 100%</th>
                        <th>Adicional Noturno (%)</th>
<<<<<<< HEAD
                        <th></th>
=======
                        <th> </th>
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
                    </tr>
                </thead>
                <tbody></tbody>
            `;
            
            const tableBody = table.querySelector('tbody');
            let totalFuncionarios = 0;// Variável para contar o total de funcionários
            
            // Itera sobre as chaves do objeto cargos
            for (const key in funcionarios) {
                if (funcionarios.hasOwnProperty(key)) {
                    totalFuncionarios++; // Incrementa o contador de funcionários
<<<<<<< HEAD
                    const funcionario = funcionarios[key];      
                    
                    
                    // Preenche a tabela com os dados do cargo
                    const row = tableBody.insertRow();
            row.insertCell(0).innerText = funcionario.nome_funcionario || key; // funcionario
            row.insertCell(1).innerText = funcionario.nome_funcao; // Desconto Transporte
            row.insertCell(2).innerText = funcionario.numero_cpf;
            row.insertCell(3).innerText = funcionario.chave_pix;
            row.insertCell(4).innerText = (parseFloat(funcionario.valor_hora_base) || 0).toFixed(2); // Valor Hora Base
            row.insertCell(5).innerText = (parseFloat(funcionario.repouso_remunerado) || 0).toFixed(2); // Vl. Repouso Remunerado
            row.insertCell(6).innerText = (parseFloat(funcionario.valor_hora_extra_um) || 0).toFixed(2); // Valor Hora Extra de 50%
            row.insertCell(7).innerText = (parseFloat(funcionario.valor_hora_extra_dois) || 0).toFixed(2); // Valor Hora Extra de 100%
            row.insertCell(8).innerText = (parseFloat(funcionario.adicional_noturno) || 0).toFixed(2); // Vl. Ad. Noturno
         
=======
                    const funcionario = funcionarios[key];  
                    
                    //console.log(funcionario);
                    
                    // Preenche a tabela com os dados do cargo
                    const row = tableBody.insertRow();
            row.insertCell(0).innerText = funcionario.nome_funcionario || key;// funcionario
            row.insertCell(1).innerText = funcionario.equipe;// funcionario
            row.insertCell(2).innerText = funcionario.nome_funcao; // Desconto Transporte
            row.insertCell(3).innerText = funcionario.numero_cpf;
            row.insertCell(4).innerText = funcionario.chave_pix;
            row.insertCell(5).innerText = (parseFloat(funcionario.valor_hora_base) || 0).toFixed(2); // Valor Hora Base
            row.insertCell(6).innerText = (parseFloat(funcionario.repouso_remunerado) || 0).toFixed(2); // Vl. Repouso Remunerado
            row.insertCell(7).innerText = (parseFloat(funcionario.valor_hora_extra_um) || 0).toFixed(2); // Valor Hora Extra de 50%
            row.insertCell(8).innerText = (parseFloat(funcionario.valor_hora_extra_dois) || 0).toFixed(2); // Valor Hora Extra de 100%
            row.insertCell(9).innerText = (parseFloat(funcionario.adicional_noturno) || 0).toFixed(2); // Vl. Ad. Noturno
            
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
                     
                    // Preenche o select com as opções de cargos
                    const option = document.createElement('option');
                    option.value =key;
                    option.textContent =key;
                    funcionarioSelect.appendChild(option);
                    

<<<<<<< HEAD
                    // Adiciona botão de editar
                    const actionsCell = row.insertCell(9);
                    const editButton = document.createElement('button');
                    editButton.textContent = 'Editar';
                    editButton.onclick = () =>  {
                        const uidFuncionario = option.textContent; 
                        const nomeFuncionario = funcionario.nome_funcionario || option.textContent; // Nome do funcionário
                        const nomefuncao = funcionario.nome_funcao;
=======
                    
                    // Adiciona botão de editar
                    const actionsCell = row.insertCell(10);
                    const editButton = document.createElement('button');
                    editButton.textContent = 'Editar';
                    editButton.onclick   = () =>  {
                        const uidFuncionario = funcionario._id;
                        const nomeFuncionario = funcionario.nome_funcionario || option.textContent; // Nome do funcionário
                        const nomefuncao = funcionario.nome_funcao;
                        const equipe=funcionario.equipe;
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
                        const cpfFuncionario = funcionario.numero_cpf; // CPF do funcionário
                        const chavePix = funcionario.chave_pix
                        const valorHoraBase = funcionario.valor_hora_base
                        const valorHoraExtraUm = funcionario.valor_hora_extra_um
<<<<<<< HEAD
                        const valorHoraExtraDois = funcionario.valor_horas_extras_dois
=======
                        const valorHoraExtraDois = funcionario.valor_hora_extra_dois
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
                        const adicionalNoturno = funcionario.adicional_noturno
                        const repousoRemunerado = funcionario.repouso_remunerado
                        const valorFerias = funcionario.valor_ferias
                        const valorUmTercoFerias = funcionario.valor_um_terco_ferias
                        const valorDecimoTerceiro = funcionario.valor_decimo_terceiro
                        const pagamentoFgts = funcionario.pagamento_fgts
                        const descontoInss = funcionario.desconto_inss
                        const descontoRefeicao = funcionario.desconto_refeicao
                        const descontoTransporte = funcionario.desconto_transporte
                        

<<<<<<< HEAD
                        editarFuncionarioModal(uidFuncionario,nomeFuncionario, nomefuncao, cpfFuncionario, chavePix,valorHoraBase, 
=======
                        editarFuncionarioModal(uidFuncionario,nomeFuncionario, nomefuncao, equipe, cpfFuncionario, chavePix,valorHoraBase, 
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
                            valorHoraExtraUm, valorHoraExtraDois,adicionalNoturno, repousoRemunerado, 
                            valorFerias, valorUmTercoFerias, valorDecimoTerceiro, pagamentoFgts, 
                            descontoInss, descontoRefeicao, descontoTransporte);
                    }
                    
                    actionsCell.appendChild(editButton);
                }
            }
            
<<<<<<< HEAD
=======
            
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
            // Atualiza o contador de registros no HTML
            totalRegistrosElement.textContent = `Total: ${totalFuncionarios}`;

            // Exibe a tabela na página (assumindo que você tenha um elemento para isso)
            
            listaFuncionarios.appendChild(table);
            


        } catch (error) {
            console.error("Erro ao buscar cargos:", error);
        }
        }
                
        // Função para filtrar os funcionários pelo nome e cpf
        function filterFuncionarios() {
            const searchValue = document.getElementById('search-funcionario').value.toLowerCase();
            const rows = document.querySelectorAll('#lista-funcionarios table tbody tr');

            rows.forEach(row => {
                const nomeFuncionario = row.cells[0].innerText.toLowerCase();
                const nomefuncao = row.cells[1].innerText.toLowerCase();
                const cpfFuncionario = row.cells[2].innerText.toLowerCase();
<<<<<<< HEAD
                row.style.display = nomeFuncionario.includes(searchValue) || nomefuncao.includes(searchValue) || cpfFuncionario.includes(searchValue) ? '' : 'none'
            });
        }

      

// **************************   Editar Funcionario **********************************
function editarFuncionarioModal(uidFuncionario, nomeFuncionario, nomefuncao, cpfFuncionario, chavePix, valorHoraBase, valorHoraExtraUm,  
=======
                const equipeFuncionario = row.cells[3].innerText.toLowerCase();
                row.style.display = nomeFuncionario.includes(searchValue) || nomefuncao.includes(searchValue)|| cpfFuncionario.includes(searchValue) || equipeFuncionario.includes(searchValue) ? '' : 'none'
            });
        }
        
//__________________________ Gerador de etiquetas ___________________________

  // Função para abrir o modal
function abrirModal() { 
    document.getElementById("modal-gerar-etiqueta").style.display = "flex";
}

// Função para fechar o modal
function fecharModal() {
    document.getElementById("modal-gerar-etiqueta").style.display = "none";
}

// Função para gerar a etiqueta
function gerarEtiqueta() {
    const dataInicio = document.getElementById("data-inicio").value;
    const dataFim = document.getElementById("data-fim").value;

    // Verifica se as datas estão preenchidas
    if (!dataInicio || !dataFim) {
        alert("Por favor, preencha as datas de início e fim.");
        return;
    }

    // Configuração para envio da requisição ao backend
    const payload = {
        data_inicio: dataInicio,
        data_fim: dataFim
    };

    fetch('http://127.0.0.1:5000/api/gerar-etiquetas', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro na resposta da rede');
        }
        return response.blob();
    })
    .then(blob => {
        // Baixa o arquivo gerado pelo backend
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'etiquetas.pdf';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);

        // Fecha o modal após gerar a etiqueta
        fecharModal();
    })
    .catch(error => {
        console.error("Erro ao gerar etiqueta:", error);
        alert("Erro ao gerar etiqueta. Tente novamente.");
    });
}

//____________________________ Editar Funcionario  _______________________________________

function editarFuncionarioModal(uidFuncionario, nomeFuncionario, nomefuncao, equipe, cpfFuncionario, chavePix, valorHoraBase, valorHoraExtraUm,  
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
    valorHoraExtraDois, adicionalNoturno, repousoRemunerado, valorFerias, valorUmTercoFerias, valorDecimoTerceiro,
    pagamentoFgts, descontoInss, descontoRefeicao, descontoTransporte) {
    
        console.log("Chamada da função para editar funcionário");
        console.log("UID recebido 2:", uidFuncionario);
    
        // Se o UID estiver `null`, isso significa que o problema está na chamada da função
        if (!uidFuncionario) {
            console.error("UID do funcionário está null!");
        }

    // Abrir o modal
    const modal = document.getElementById('editModal');
    modal.style.display = 'block';
     // Atribuindo o UID ao campo oculto
    console.log("UID do Funcionário a ser atribuído:", uidFuncionario);
<<<<<<< HEAD

    document.getElementById('data-id').value = uidFuncionario; // Atribuindo ao campo oculto
    document.getElementById('nome_funcionario').value = nomeFuncionario;
    document.getElementById('nome_funcao').value = nomefuncao;
=======
    console.log("UID do Funcionário Teste:", uidFuncionario);

    document.getElementById('_id').value = uidFuncionario; // Atribuindo ao campo oculto
    document.getElementById('nome_funcionario').value = nomeFuncionario;
    document.getElementById('nome_funcao').value = nomefuncao;
    document.getElementById('equipe').value = equipe;
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
    document.getElementById('numero_cpf').value = cpfFuncionario;
    document.getElementById('chave_pix').value = chavePix;
    document.getElementById('valor_hora_base').value = (parseFloat(valorHoraBase) || 0).toFixed(2);
    document.getElementById('valor_hora_extra_um').value = (parseFloat(valorHoraExtraUm) || 0).toFixed(2);
    document.getElementById('valor_hora_extra_dois').value = (parseFloat(valorHoraExtraDois) || 0).toFixed(2);
    document.getElementById('adicional_noturno').value = (parseFloat(adicionalNoturno) || 0).toFixed(2);
    document.getElementById('repouso_remunerado').value = (parseFloat(repousoRemunerado) || 0).toFixed(2);
    document.getElementById('valor_ferias').value = (parseFloat(valorFerias) || 0).toFixed(2);
    document.getElementById('valor_um_terco_ferias').value = (parseFloat(valorUmTercoFerias) || 0).toFixed(2);
    document.getElementById('valor_decimo_terceiro').value = (parseFloat(valorDecimoTerceiro) || 0).toFixed(2);
    document.getElementById('pagamento_fgts').value = (parseFloat(pagamentoFgts) || 0).toFixed(2);
    document.getElementById('desconto_inss').value = (parseFloat(descontoInss) || 0).toFixed(2);
    document.getElementById('desconto_refeicao').value = (parseFloat(descontoRefeicao) || 0).toFixed(2);
    document.getElementById('desconto_transporte').value = (parseFloat(descontoTransporte) || 0).toFixed(2);


    // Função para fechar o modal
    document.querySelector('.close').onclick = function() {
        modal.style.display = 'none';
    }
   
<<<<<<< HEAD


    // Verifica se o formulário existe antes de adicionar o event listener
    const editForm = document.getElementById('editForm');
    if (editForm) {
        editForm.addEventListener('submit', async function(event) {
            event.preventDefault(); // Impede o envio padrão do formulário  


            const formData = {
                nome_funcionario: document.getElementById('nome_funcionario').value.trim(),
                nome_funcao: document.getElementById('nome_funcao').value.trim(),
                numero_cpf: document.getElementById('numero_cpf').value.trim(),
                chave_pix: document.getElementById('chave_pix').value.trim(),
                valor_hora_base: parseFloat(document.getElementById('valor_hora_base').value),
                valor_hora_extra_um: parseFloat(document.getElementById('valor_hora_extra_um').value),
                valor_hora_extra_dois: parseFloat(document.getElementById('valor_hora_extra_dois').value),
                adicional_noturno: parseFloat(document.getElementById('adicional_noturno').value),
                repouso_remunerado: parseFloat(document.getElementById('repouso_remunerado').value),
                valor_ferias: parseFloat(document.getElementById('valor_ferias').value),
                valor_um_terco_ferias: parseFloat(document.getElementById('valor_um_terco_ferias').value),
                valor_decimo_terceiro: parseFloat(document.getElementById('valor_decimo_terceiro').value),
                pagamento_fgts: parseFloat(document.getElementById('pagamento_fgts').value),
                desconto_inss: parseFloat(document.getElementById('desconto_inss').value),
                desconto_refeicao: parseFloat(document.getElementById('desconto_refeicao').value),
                desconto_transporte: parseFloat(document.getElementById('desconto_transporte').value),
            };
             console.log('Dados enviados:', formData);

            try {
                const response = await fetch(`http://127.0.0.1:5000/api/funcionario/${uidFuncionario}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });

                if (!response.ok) {
                    let errorMessage;
                    try {
                        const error = await response.json();
                        errorMessage = error.message || 'Erro desconhecido';
                    } catch (jsonError) {
                        errorMessage = await response.text();
                    }

                    alert(`Erro: ${errorMessage}`);
                    throw new Error(`Erro na atualização: ${errorMessage}`);
                }

                alert('Funcionário atualizado com sucesso!');

                // Fechar o modal
                modal.style.display = 'none';

                // Atualizar a página
                location.reload();

            } catch (error) {
                console.error('Erro ao salvar os dados:', error);
                alert('Erro ao salvar os dados. Tente novamente.');
            }
        });
    } else {
        console.error('O formulário com ID "editForm" não foi encontrado.');
    }



  // ********* Criar Funcionario *************
   document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('funcionario-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Impede o envio padrão do formulário

    const formData = new FormData(event.target);    
    //const cargoData = Object.fromEntries(formData);

        // Coleta e estrutura os dados do formulário
        const funcionariData = {
=======
    
        // Verifica se o formulário existe antes de adicionar o event listener
        const editForm = document.getElementById('editForm');
        if (editForm) {
            editForm.addEventListener('submit', async function(event) {
                event.preventDefault(); // Impede o envio padrão do formulário  
    
                const funcionarioId =  editForm.dataset.id; // Obtém o ID do funcionário
                const formData = {
                    nome_funcionario: document.getElementById('nome_funcionario').value.trim(),
                    nome_funcao: document.getElementById('nome_funcao').value.trim(),
                    equipe: document.getElementById('equipe').value.trim(),
                    numero_cpf: document.getElementById('numero_cpf').value.trim(),
                    chave_pix: document.getElementById('chave_pix').value.trim(),
                    valor_hora_base: parseFloat(document.getElementById('valor_hora_base').value) ,
                    valor_hora_extra_um: parseFloat(document.getElementById('valor_hora_extra_um').value),
                    valor_hora_extra_dois: parseFloat(document.getElementById('valor_hora_extra_dois').value),
                    adicional_noturno: parseFloat(document.getElementById('adicional_noturno').value),
                    repouso_remunerado: parseFloat(document.getElementById('repouso_remunerado').value),
                    valor_ferias: parseFloat(document.getElementById('valor_ferias').value),
                    valor_um_terco_ferias: parseFloat(document.getElementById('valor_um_terco_ferias').value),
                    valor_decimo_terceiro: parseFloat(document.getElementById('valor_decimo_terceiro').value),
                    pagamento_fgts: parseFloat(document.getElementById('pagamento_fgts').value),
                    desconto_inss: parseFloat(document.getElementById('desconto_inss').value),
                    desconto_refeicao: parseFloat(document.getElementById('desconto_refeicao').value),
                    desconto_transporte: parseFloat(document.getElementById('desconto_transporte').value),
                };
                 console.log('Dados enviados:', );
    
                try {
                    const response = await fetch(`http://127.0.0.1:5000/api/funcionario/${uidFuncionario}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(formData)
                    });
    
                    if (!response.ok) {
                        let errorMessage;
                        try {
                            const error = await response.json();
                            errorMessage = error.message || 'Erro desconhecido';
                            
                        } catch (jsonError) {
                            errorMessage = await response.text();
                        }
    
                        alert(`Erro: ${errorMessage}`);
                        throw new Error(`Erro na atualização: ${errorMessage}`);
                    }
    
                    alert('Funcionário atualizado com sucesso!');
    
                    // Fechar o modal
                    modal.style.display = 'none';
    
                    // Atualizar a página
                    location.reload();
    
                } catch (error) {
                    console.error('Erro completo:', error);
                    alert(`Erro ao salvar os dados: ${error.message || 'Erro desconhecido'}`);
                }
            });
        } else {
            console.error('O formulário com ID "editForm" não foi encontrado.');
        }
    }
    

//________________________________ Cadastro de Funcionarios __________________________________________
  
    document.getElementById('funcionario-form').addEventListener('submit', async function(event) {
        console.log("Formulário enviado.");    
        console.log("Script de JavaScript carregado.");

        event.preventDefault(); // Impede o envio padrão do formulário

        // Coleta e estrutura os dados do formulár
        const funcionariData = {
            //_id : uidFuncionario,
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
            nome_funcionario: document.getElementById('nome_funcionario_c').value.trim(),
            numero_cpf: document.getElementById('numero_cpf_c').value.trim(),
            chave_pix: document.getElementById('chave_pix_c').value.trim(),
            valor_hora_base: parseFloat(document.getElementById('valor_hora_base_c').value) || 0,
            valor_hora_extra_um: parseFloat(document.getElementById('valor_hora_extra_um_c').value) || 0,
            valor_hora_extra_dois: parseFloat(document.getElementById('valor_hora_extra_dois_c').value) || 0,
            adicional_noturno: parseFloat(document.getElementById('adicional_noturno_c').value) || 0,
            repouso_remunerado: parseFloat(document.getElementById('repouso_remunerado_c').value) || 0,
            desconto_inss: parseFloat(document.getElementById('desconto_inss_c').value) || 0,
            desconto_refeicao: parseFloat(document.getElementById('desconto_refeicao_c').value) || 0,
            desconto_transporte: parseFloat(document.getElementById('desconto_transporte_c').value) || 0,
            pagamento_fgts: parseFloat(document.getElementById('pagamento_fgts_c').value) || 0,
            valor_decimo_terceiro: parseFloat(document.getElementById('valor_decimo_terceiro_c').value) || 0,
            valor_ferias: parseFloat(document.getElementById('valor_ferias_c').value) || 0,
            valor_um_terco_ferias: parseFloat(document.getElementById('valor_um_terco_ferias_c').value) || 0,
            nome_funcao: document.getElementById('nome_funcao_c').value.trim(),
<<<<<<< HEAD
            equipe: document.getElementById('equipe_c').value.trim(),
        };


                        const numericFields = [
                        'valor_hora_base',
                        'valor_hora_extra_um',
                        'valor_hora_extra_dois',
                        'adicional_noturno',
                        'repouso_remunerado',
                        'desconto_inss',
                        'desconto_refeicao',
                        'desconto_transporte',
                        'pagamento_fgts',
                        'valor_decimo_terceiro',
                        'valor_ferias',
                        'valor_um_terco_ferias'
                        ];

    // Captura os dados do formulário
    numericFields.forEach(field => {    
    funcionariData[field] = parseFloat(funcionariData[field]) || 0; // Corrigido para usar 'field'
    });


     //********************* Select para a criação do recibo. ***************************
        $(document).ready(function() {
        $('#name_funcionario').select2({
            placeholder: "Selecione um funcionário",
            allowClear: true,
            width: 'resolve',
            tags: true
        });
    
        async function loadFuncionarios() { 
            try {
                const response = await fetch('http://127.0.0.1:5000/api/funcionarios');
                const funcionarios = await response.json();
                console.log("Funcionários recebidos 00:", funcionarios);
    
                const selectElement = document.getElementById('name_funcionario');
                console.log("selectElement:", selectElement); // Verifique se o elemento foi encontrado
                selectElement.innerHTML = ''; // Limpa as opções atuais
    
                for (const key in funcionarios) {
                    if (funcionarios[key].nome_funcionario) {
                        const option = document.createElement('option');
                        option.value = key; // Chave UID para busca posterior
                        option.textContent = funcionarios[key].nome_funcionario; // Exibe nome do funcionário
                        option.dataset.nomeFuncao = funcionarios[key].nome_funcao || ''; // Armazena nome_funcao como atributo data
                        
                        console.log(`Adicionando opção: ${option.textContent} com key: ${key} e nome_funcao: ${option.dataset.nomeFuncao}`);
                        
                        selectElement.appendChild(option);
                    } else {
                        console.warn(`Funcionário com key: ${key} não tem nome_funcionario.`);
                    }
                }
            } catch (error) {
                console.error("Erro ao carregar funcionários:", error);
            }
        }
    
     // Evento para preencher os campos quando um funcionário é selecionado
    $('#name_funcionario').on('change', (event) => {
        const selectedOption = event.target.options[event.target.selectedIndex];
    
=======
            equipe: document.getElementById('equipe_c').value.trim()
        };

        console.log("Dados a serem enviados:", JSON.stringify(funcionariData));

        try {
            const response = await fetch('http://127.0.0.1:5000/api/criar_funcionario', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(funcionariData)
            });

            if (response.ok) {
                const data = await response.json();
                document.getElementById('message').textContent = data.message;  // Exibe a mensagem de sucesso

                alert('Cadastro de funcionário criado com sucesso!');
                fetchCargos();
                location.reload();
            } else {
                const errorData = await response.json();
                console.error('Erro ao cadastrar funcionário:', errorData);
                alert(`Erro: ${errorData.message || 'Funcionário ja dastrado.'}`);
            }
        } catch (error) {
            alert('Cadastro de funcionário criado com sucesso!');
            fetchCargos();
            location.reload();

        }
    });

    
 //__________________________ Select para a criação do recibo. ___________________________  
 $(document).ready(function () {
    // Inicialização do Select2 no campo de seleção
    $('#name_funcionario').select2({
        placeholder: "Selecione um funcionário",
        allowClear: true,
        width: 'resolve',
        tags: true
    });

    // Função para carregar a lista de funcionários e preencher o dropdown
    async function loadFuncionarios() {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/funcionarios');
            const funcionarios = await response.json();

            const selectElement = document.getElementById('name_funcionario');
            selectElement.innerHTML = ''; // Limpa as opções atuais

            // Adiciona a opção padrão
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = 'Selecione um funcionário';
            selectElement.appendChild(defaultOption);

            // Itera sobre os funcionários e cria as opções do dropdown
            for (const uid in funcionarios) {
                const funcionario = funcionarios[uid];
                if (funcionario.nome_funcionario) {
                    const option = document.createElement('option');
                    option.value = funcionario._id; // Define o UID (_id) como valor
                    option.textContent = funcionario.nome_funcionario; // Define o nome do funcionário como texto
                    option.dataset.nomeFuncao = funcionario.nome_funcao || ''; // Define o nome da função como atributo data
                    selectElement.appendChild(option); // Adiciona a opção ao dropdown
                } else {
                    console.warn(`Funcionário sem nome: ${uid}`);
                }
            }
        } catch (error) {
            console.error("Erro ao carregar funcionários:", error);
        }
    }

    // Evento para preencher os campos quando um funcionário é selecionado
    $('#name_funcionario').on('change', (event) => {
        const selectedOption = event.target.options[event.target.selectedIndex];

>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
        // Verifica se há uma opção selecionada
        if (selectedOption) {
            console.log(`Funcionário selecionado: ${selectedOption.textContent}`);
            console.log(`Chave selecionada: ${selectedOption.value}`);
            console.log(`Nome da função: ${selectedOption.dataset.nomeFuncao}`);
<<<<<<< HEAD
            
            // Preenche o campo 'name_funcionario' com o nome do funcionário
            document.getElementById('name_funcionario').value = selectedOption.textContent;
    
            // Preenche o campo 'nome_funcao' com o valor armazenado no data-attribute
            document.getElementById('nome_cargo').value = selectedOption.dataset.nomeFuncao; // Corrigido de 'nome_cago' para 'nome_funcao'
=======

            // Preenche o campo 'name_funcionario' com o nome do funcionário
            document.getElementById('name_funcionario').value = selectedOption.textContent;

            // Preenche o campo 'nome_cargo' com o valor armazenado no data-attribute
            document.getElementById('nome_cargo').value = selectedOption.dataset.nomeFuncao || ''; 

            // Salva a chave do funcionário e outros dados na variável
            funcionarioChave = selectedOption.value;    
            nomeFuncionarioSelecionado = selectedOption.value;
            const nomeFuncaoSelecionada = selectedOption.dataset.nomeFuncao;

            console.log(`Chave do funcionário salva: ${funcionarioChave}`);
            console.log(`Nome do funcionário salvo: ${nomeFuncionarioSelecionado}`);
            console.log(`Função salva: ${nomeFuncaoSelecionada}`);
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
        } else {
            console.warn("Nenhuma opção válida selecionada.");
        }
    });
<<<<<<< HEAD
    
    
        loadFuncionarios();
    });


    // Cadastro para pagamento e imprimir PDF -> Gerador do PDF
   
=======

    // Carrega a lista de funcionários ao carregar a página
    loadFuncionarios();
});


    
// ____________________________Cadastro para pagamento e imprimir PDF -> Gerador do PDF_____________________
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
    document.getElementById('gerarDocumentoButton').addEventListener('click', async function(event) {
        event.preventDefault();
    
        const formData = new FormData(document.getElementById('recibo-form'));
        const reciboData = Object.fromEntries(formData);
<<<<<<< HEAD
=======
        
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
    
        // Obter o campo select que contém os funcionários
        const funcionarioSelect = document.getElementById('name_funcionario');
    
        // Verifica se o select existe antes de tentar acessar o valor
        if (!funcionarioSelect) {
            console.error('Elemento select com id "name_funcionario" não encontrado.');
            return;
        }
    
<<<<<<< HEAD
        const funcionarioId = funcionarioSelect.value;

        // Verifica se um funcionário foi selecionado
        if (!funcionarioId) {
            console.log('Valor enviado', funcionarioId)
            console.log('Valor enviado2', funcionarioSelect.value)
             console.log('Valor enviado3', funcionarioSelect)
            console.error('Por favor, selecione um funcionário.');
=======
        const funcionarioId= funcionarioChave || funcionarioSelect.value;

        // Verifica se um funcionário foi selecionado
        if (!funcionarioId) {
           console.error('Por favor, selecione um funcionário.');
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
            return;
        }
    
        // Continue com o processamento do formulário...
<<<<<<< HEAD
        console.log('Funcionário selecionado agora:', funcionarioId);
        // Você pode adicionar mais lógica aqui para continuar o processo de geração do documento
    

    
=======
        console.log('Funcionário selecionado agora  foi e será:', funcionarioId);
         

>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
        // Fetch para obter os dados do cargo
        const funcionarioResponse = await fetch(`http://127.0.0.1:5000/api/funcionarios/${funcionarioId}`);
        if (!funcionarioResponse.ok) {
        console.error('Erro ao buscar dados funcionario:', funcionarioResponse.statusText);
        return;
        }
        const funcionario = await funcionarioResponse.json();
<<<<<<< HEAD
=======
        console.log('Funcionário encontrado:', funcionario);
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba

        //Definir um valor default em caso de valor zerado ou null
        const checkAndParse = (value) => {  
        const parsedValue = parseFloat(value);
        return isNaN(parsedValue) ? 0.00 : parsedValue;
        };

        // Função para formatar data para DD-MM-YYYY
        const formatDate = (dateString) => {
        const [year, month, day] = dateString.split('-');
        return `${day}-${month}-${year}`; // Formato DD/MM/YYYY
        };
        function checkAndParseString(value, defaultValue = "") {
            if (typeof value === "string") {
                return value.trim(); // Remove espaços em branco
            }
            return defaultValue; // Retorna um valor padrão se não for uma string
        }
        
        // Apenas adicionar os campos CPF e Chave PIX como strings ao reciboData
<<<<<<< HEAD
        reciboData.name_funcionario = checkAndParseString(reciboData.name_funcionario);
=======
        reciboData.name_funcionario = checkAndParseString(nomeFuncionarioSelecionado);
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
        reciboData.nome_cargo = checkAndParseString(reciboData.nome_cargo);
        reciboData.horas_trabalhadas = checkAndParse(reciboData.horas_trabalhadas, 10,);
        reciboData.horas_extras_um = checkAndParse(reciboData.horas_extras_um, 10);
        reciboData.horas_extras_dois = checkAndParse(reciboData.horas_extras_dois, 10);
        reciboData.horas_noturnas = checkAndParse(reciboData.horas_noturnas, 10);
        reciboData.repouso_remunerado = checkAndParse(reciboData.repouso_remunerado, 10);
        reciboData.correcao_positiva = checkAndParse(reciboData.correcao_positiva, 10);
        reciboData.correcao_negativa = checkAndParse(reciboData.correcao_negativa, 10);
        reciboData.data_inicio = formatDate(reciboData.data_inicio);
        reciboData.data_fim = formatDate(reciboData.data_fim);
<<<<<<< HEAD
        reciboData.data_pagamento = formatDate(reciboData.data_pagamento);
        reciboData.valor_diarias = checkAndParse(reciboData.valor_diarias, 10);

        

        // Verifique se todos os campos obrigatórios estão preenchidos
        const requiredFields = ['data_inicio','data_fim', 'data_pagamento','nome_cargo','name_funcionario','horas_trabalhadas', 'horas_extras_um', 'horas_extras_dois', 'horas_noturnas', 'valor_diarias', 'correcao_positiva', 'correcao_negativa'];

=======
        reciboData.data_pagamento= formatDate(reciboData.data_pagamento);
        reciboData.valor_diarias =checkAndParse(reciboData.valor_diarias, 10);
        reciboData.parcela_vale =checkAndParse(reciboData.parcela_vale, 10);
        reciboData.diferenca_calculo =checkAndParse(reciboData.diferenca_calculo, 10);

        console.log('Valor de name_funcionario:', reciboData.name_funcionario);
        console.log('Valor de nome_cargo:', reciboData.nome_cargo);
        console.log('Valor de data_pagamento:', reciboData.data_pagamento);


        // Verifique se todos os campos obrigatórios estão preenchidos
        const requiredFields = ['data_inicio','data_fim', 'data_pagamento','nome_cargo','name_funcionario','horas_trabalhadas', 'horas_extras_um', 'horas_extras_dois', 'horas_noturnas', 'valor_diarias', 'correcao_positiva', 'correcao_negativa','parcela_vale','diferenca_calculo'];
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba

        //Valida os dados enviados -> Valor fucionario === string // Demais tem que ser float.
        for (const field of requiredFields) {
        const value = reciboData[field];
<<<<<<< HEAD
        // Verifica se o campo é nome_funcionario
        if (field === 'name_funcionario'|| field === 'nome_cargo' ) {  
        if (typeof value !== 'string' || value.trim() === '') {
            console.error(`Campo obrigatório "${field}" é inválido.`);
=======

        // Verifica se o campo é nome_funcionario
        if (field === 'name_funcionario'|| field === 'nome_cargo' ) {  
        if (typeof value !== 'string' || value.trim() === '') {
            alert('Nome do Cargo  e Nome Funcionario são obrigátorios');
            console.error(`Campo obrigatório "${field}" é inválido.`);
            alert('Nome e Cargo são Obrigatorios!')
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
            return;
        }
        } 

        // Verifica se o campo é data_inicio ou data_fim
        else if (field === 'data_inicio' || field === 'data_fim' || field === 'data_pagamento' ) {
        if (!value || new Date(value.split('-').reverse().join('-')).toString() === "Invalid Date") {
            const errorMessage = `Preenchimento do campo "${field}" é obrigatorio!.`;
<<<<<<< HEAD
=======
            alert('O campos de Data são Obrigatorios!')
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
            console.error(errorMessage);

            
            // Exibir a mensagem de erro no front-end
            const errorElement = document.getElementById('error-message');
            errorElement.textContent = errorMessage; // Define o texto da mensagem
            errorElement.style.display = 'block'; // Torna a mensagem visível

                    // Ocultar a mensagem após 5 segundos
            setTimeout(() => {
                errorElement.style.display = 'none'; // Esconde a mensagem
            }, 5000); 

            return;
        }
        }
        
        // Para outros campos que são numéricos
        else {
        if (value === undefined || value === null || isNaN(value)) {
            console.error(`Campo obrigatório "${field}" é inválido.`);
            
            return;
        }
        }

<<<<<<< HEAD
        }   

        
        // Envie os dados para o backend
        const response = await fetch('http://127.0.0.1:5000/api/criar_recibo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(reciboData),
        mode:'cors'

        });
        
        //const responseData = await response.json();  // Caso você precise processar a resposta como JSON
        

        if (response.ok) {

        const contentType = response.headers.get('Content-Type');
        if (contentType && contentType.includes('application/pdf')) {  
        // Ler o PDF como blob
        const blob = await response.blob();

        // Cria um link para download do PDF
        const url = window.URL.createObjectURL(blob);
        const iframe = document.createElement('iframe');
        iframe.style.width = '100%';
        iframe.style.height = '600px';
        iframe.src = url;
        document.getElementById('documentContentPreview').innerHTML = ''; // Limpar conteúdo anterior
        document.getElementById('documentContentPreview').appendChild(iframe);



        // Configura o evento de clique no botão de imprimir PDF
        document.getElementById('printDocumentButton').onclick =  function() { 
            const a = document.createElement('a');
            //const url = window.URL.createObjectURL(blob);
            a.href = url;
            a.download = `${reciboData.name_funcionario} de ${reciboData.data_inicio} ate ${reciboData.data_fim}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        };
        

        // Configura o evento de clique no botão "Cancelar"
        document.querySelector('.btn-secondary[data-bs-dismiss="modal"]').onclick = function() {
            $('#documentPreviewModal').modal('hide'); // Fecha o modal
            };
        // Exibe o modal se necessário
        $('#documentPreviewModal').modal('show');

            } else {
                console.error('Erro: A resposta não é um PDF. Tipo de conteúdo:', contentType);
            }
            } else {
            console.error('Erro ao gerar o olerite:', response.statusText);
            }
            
    });
  

        // Fechar mensagens 
        messageDiv.addEventListener('click', function() {
        messageDiv.style.display = 'none'; // Esconde a mensagem ao clicar na mensagem
        location.reload(); // Recarrega a página ao fechar a mensagem
        });
    });

    

});
    }
    
=======
        } 
            // Enviar os dados para o backend
        console.log('Chegou aqui: antes de gerarRecibo');
        await gerarRecibo(reciboData);  
        

        //***************************  Envie os dados para o backend ***********************   
        async function gerarRecibo(reciboData) {
            console.log('Chegou aqui: Depois de gerarRecibo'); 
        
            // Validação dos dados obrigatórios antes de enviar para o backend
            console.log('Dados enviados ao backend:', reciboData);
        
            // Verifique se os campos obrigatórios estão presentes
            if (!reciboData.data_inicio || !reciboData.data_fim || !reciboData.name_funcionario || !reciboData.nome_cargo) {
                console.error('Dados obrigatórios faltando!');
                alert('Dados obrigatórios faltando!');
                return; // Se faltar algum dado, não envia a requisição
            }
        
            try {
                console.log('Enviando dados para o backend...');
        
                const response = await fetch('http://127.0.0.1:5000/api/criar_recibo', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(reciboData),
                    mode: 'cors'
                });
        
                if (response.ok) {
                    const contentType = response.headers.get('Content-Type');
                    if (contentType && contentType.includes('application/pdf')) {
                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
        
                        // Preencher o iframe com o PDF
                        const iframe = document.createElement('iframe');
                        iframe.style.width = '100%';
                        iframe.style.height = '600px';
                        iframe.src = url;
                        document.getElementById('documentContentPreview').innerHTML = '';
                        document.getElementById('documentContentPreview').appendChild(iframe);
        
                        // Configurar download
                        document.getElementById('printDocumentButton').onclick = function () {
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = `${funcionario.nome_funcionario} de ${reciboData.data_inicio} até ${reciboData.data_fim}.pdf`;
                            document.body.appendChild(a);
                            a.click();
                            window.URL.revokeObjectURL(url);
                            document.body.removeChild(a);
                            console.log("Botão de download acionado.");
                        };
        
                        // Fechar o modal
                        document.querySelector('.btn-secondary[data-bs-dismiss="modal"]').onclick = function () {
                            $('#documentPreviewModal').modal('hide');
                        };
        
                        // Mostrar o modal
                        $('#documentPreviewModal').modal('show');
                    } else {
                        console.error('Erro: A resposta não é um PDF. Tipo de conteúdo:', contentType);
                    }
                } else {
                    const errorData = await response.json();
                    console.error('Erro ao gerar o olerite:', errorData.error);
                    alert('Erro ao gerar o olerite: ' + errorData.error);
                    console.log('Erro detalhado do backend:', errorData);
                }
            } catch (error) {
                console.error('Erro inesperado:', error);
                alert('Erro inesperado ao tentar gerar o recibo.');
            }
        }
        
            });
>>>>>>> 28922aefcf2966260ba3410c7ef92d079acbdbba
