
   
     function showTab(tab) {

        
        const tabs = document.querySelectorAll('.tab');
        tabs.forEach(t => {
            t.classList.remove('active');
        });
        document.getElementById(tab).classList.add('active');
    }


    document.addEventListener('DOMContentLoaded', () => {
        fetchCargos();
        document.getElementById('name_funcionario').value = '';
        showTab('lista'); // Mostra a aba de cargos ao carregar
    });
    function baixarArquivoExcel() {
        // Define a URL do endpoint para download
        const url = "http://localhost:5000/baixar_excel";

        // Redireciona para a URL para iniciar o download
        window.location.href = url;
    }

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
                        <th>Função </th>
                        <th>CPF</th>
                        <th>Chave PIX</th>
                        <th>Hora Base (%)</th>
                        <th>Repouso Remunerado (%)</th>
                        <th>Hora Extra 50%</th>
                        <th>Hora Extra 100%</th>
                        <th>Adicional Noturno (%)</th>
                        <th></th>
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
         
                     
                    // Preenche o select com as opções de cargos
                    const option = document.createElement('option');
                    option.value =key;
                    option.textContent =key;
                    funcionarioSelect.appendChild(option);
                    

                    // Adiciona botão de editar
                    const actionsCell = row.insertCell(9);
                    const editButton = document.createElement('button');
                    editButton.textContent = 'Editar';
                    editButton.onclick = () =>  {
                        const uidFuncionario = option.textContent; 
                        const nomeFuncionario = funcionario.nome_funcionario || option.textContent; // Nome do funcionário
                        const nomefuncao = funcionario.nome_funcao;
                        const cpfFuncionario = funcionario.numero_cpf; // CPF do funcionário
                        const chavePix = funcionario.chave_pix
                        const valorHoraBase = funcionario.valor_hora_base
                        const valorHoraExtraUm = funcionario.valor_hora_extra_um
                        const valorHoraExtraDois = funcionario.valor_horas_extras_dois
                        const adicionalNoturno = funcionario.adicional_noturno
                        const repousoRemunerado = funcionario.repouso_remunerado
                        const valorFerias = funcionario.valor_ferias
                        const valorUmTercoFerias = funcionario.valor_um_terco_ferias
                        const valorDecimoTerceiro = funcionario.valor_decimo_terceiro
                        const pagamentoFgts = funcionario.pagamento_fgts
                        const descontoInss = funcionario.desconto_inss
                        const descontoRefeicao = funcionario.desconto_refeicao
                        const descontoTransporte = funcionario.desconto_transporte
                        

                        editarFuncionarioModal(uidFuncionario,nomeFuncionario, nomefuncao, cpfFuncionario, chavePix,valorHoraBase, 
                            valorHoraExtraUm, valorHoraExtraDois,adicionalNoturno, repousoRemunerado, 
                            valorFerias, valorUmTercoFerias, valorDecimoTerceiro, pagamentoFgts, 
                            descontoInss, descontoRefeicao, descontoTransporte);
                    }
                    
                    actionsCell.appendChild(editButton);
                }
            }
            
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
                row.style.display = nomeFuncionario.includes(searchValue) || nomefuncao.includes(searchValue) || cpfFuncionario.includes(searchValue) ? '' : 'none'
            });
        }

      

// **************************   Editar Funcionario **********************************
function editarFuncionarioModal(uidFuncionario, nomeFuncionario, nomefuncao, cpfFuncionario, chavePix, valorHoraBase, valorHoraExtraUm,  
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

    document.getElementById('data-id').value = uidFuncionario; // Atribuindo ao campo oculto
    document.getElementById('nome_funcionario').value = nomeFuncionario;
    document.getElementById('nome_funcao').value = nomefuncao;
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
    
        // Verifica se há uma opção selecionada
        if (selectedOption) {
            console.log(`Funcionário selecionado: ${selectedOption.textContent}`);
            console.log(`Chave selecionada: ${selectedOption.value}`);
            console.log(`Nome da função: ${selectedOption.dataset.nomeFuncao}`);
            
            // Preenche o campo 'name_funcionario' com o nome do funcionário
            document.getElementById('name_funcionario').value = selectedOption.textContent;
    
            // Preenche o campo 'nome_funcao' com o valor armazenado no data-attribute
            document.getElementById('nome_cargo').value = selectedOption.dataset.nomeFuncao; // Corrigido de 'nome_cago' para 'nome_funcao'
        } else {
            console.warn("Nenhuma opção válida selecionada.");
        }
    });
    
    
        loadFuncionarios();
    });


    // Cadastro para pagamento e imprimir PDF -> Gerador do PDF
   
    document.getElementById('gerarDocumentoButton').addEventListener('click', async function(event) {
        event.preventDefault();
    
        const formData = new FormData(document.getElementById('recibo-form'));
        const reciboData = Object.fromEntries(formData);
    
        // Obter o campo select que contém os funcionários
        const funcionarioSelect = document.getElementById('name_funcionario');
    
        // Verifica se o select existe antes de tentar acessar o valor
        if (!funcionarioSelect) {
            console.error('Elemento select com id "name_funcionario" não encontrado.');
            return;
        }
    
        const funcionarioId = funcionarioSelect.value;

        // Verifica se um funcionário foi selecionado
        if (!funcionarioId) {
            console.log('Valor enviado', funcionarioId)
            console.log('Valor enviado2', funcionarioSelect.value)
             console.log('Valor enviado3', funcionarioSelect)
            console.error('Por favor, selecione um funcionário.');
            return;
        }
    
        // Continue com o processamento do formulário...
        console.log('Funcionário selecionado agora:', funcionarioId);
        // Você pode adicionar mais lógica aqui para continuar o processo de geração do documento
    

    
        // Fetch para obter os dados do cargo
        const funcionarioResponse = await fetch(`http://127.0.0.1:5000/api/funcionarios/${funcionarioId}`);
        if (!funcionarioResponse.ok) {
        console.error('Erro ao buscar dados funcionario:', funcionarioResponse.statusText);
        return;
        }
        const funcionario = await funcionarioResponse.json();

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
        reciboData.name_funcionario = checkAndParseString(reciboData.name_funcionario);
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
        reciboData.data_pagamento = formatDate(reciboData.data_pagamento);
        reciboData.valor_diarias = checkAndParse(reciboData.valor_diarias, 10);

        

        // Verifique se todos os campos obrigatórios estão preenchidos
        const requiredFields = ['data_inicio','data_fim', 'data_pagamento','nome_cargo','name_funcionario','horas_trabalhadas', 'horas_extras_um', 'horas_extras_dois', 'horas_noturnas', 'valor_diarias', 'correcao_positiva', 'correcao_negativa'];


        //Valida os dados enviados -> Valor fucionario === string // Demais tem que ser float.
        for (const field of requiredFields) {
        const value = reciboData[field];
        // Verifica se o campo é nome_funcionario
        if (field === 'name_funcionario'|| field === 'nome_cargo' ) {  
        if (typeof value !== 'string' || value.trim() === '') {
            console.error(`Campo obrigatório "${field}" é inválido.`);
            return;
        }
        } 

        // Verifica se o campo é data_inicio ou data_fim
        else if (field === 'data_inicio' || field === 'data_fim' || field === 'data_pagamento' ) {
        if (!value || new Date(value.split('-').reverse().join('-')).toString() === "Invalid Date") {
            const errorMessage = `Preenchimento do campo "${field}" é obrigatorio!.`;
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
    