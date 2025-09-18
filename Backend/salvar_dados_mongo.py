from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging
from datetime import datetime, date

# Configuração básica de logging
logging.basicConfig(
    level=logging.DEBUG,  # Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

load_dotenv()

def converter_datas(dado):
    for key, value in dado.items():
        if isinstance(value, date):  # Corrigido para usar 'date' em vez de 'datetime.date'
            dado[key] = datetime.combine(value, datetime.min.time())
    return dado

class MongoDBHandler:
    def __init__(self, database_name, collection_name):
        try:
            self.client = MongoClient(os.getenv("MONGO_URI"))
            self.db = self.client[database_name]
            self.colecao = self.db[collection_name]
            logger.info("Conexão com MongoDB estabelecida com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao conectar com MongoDB: {e}")
            raise  # Relevanta a exceção caso haja erro na conexão
    

    def inserir_dado(self, dado):
        """
        Insere um documento na coleção.
        """
        try:
            dado = converter_datas(dado)  # Converte datas antes de inserir
            logger.debug(f"Dados a serem inseridos: {dado}")
            result = self.colecao.insert_one(dado)  # Corrigido para self.colecao
            logger.info(f"Dado inserido com ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Erro ao inserir dado: {e}")
            logger.debug(f"Detalhes do dado que causou o erro: {dado}")  # Mostra os dados tentados]
            logger.exception("Detalhes completos da exceção:")
            return None 

    def buscar_dado(self, data_inicio=None, data_fim=None):
        """
        Busca documentos na coleção com base em um intervalo de datas.

        :param data_inicio: Data inicial (string no formato 'YYYY-MM-DD').
        :param data_fim: Data final (string no formato 'YYYY-MM-DD').
        :return: Lista de documentos encontrados.
        """
        try:
            filtro = {}
<<<<<<< HEAD
            if data_inicio:
                filtro["data_inicio"] = {"$gte": data_inicio}
            if data_fim:
                filtro["data_fim"] = {"$lte": data_fim}
=======
            if data_inicio and data_fim:
                filtro = {
                "data_inicio": data_inicio,  # data_inicio do documento deve ser igual a data_inicio fornecida
                "data_fim": data_fim         # data_fim do documento deve ser igual a data_fim fornecida
            }
>>>>>>> b2341e7889e447dffaa274c107459a9a67c2cca6

            logger.debug(f"Usando o filtro: {filtro}")
            
            # Busca no banco de dados
            resultado = self.colecao.find(filtro)
            return list(resultado)  # Converte o cursor em uma lista
        except Exception as e:
            print(f"Erro ao buscar dado: {e}")
            return []
        
    def buscar_por_filtro(self, equipes=None, data_inicio=None, data_fim=None):
        """
        Busca documentos com base em filtros opcionais.
        :param equipe: Nome da equipe (opcional)
        :param data_inicio: Data de início (opcional)
        :param data_fim: Data de fim (opcional)
        :return: Lista de documentos encontrados
        """
        try:
            # Construindo o filtro dinamicamente
            filtro = {}
            if equipes:
                filtro["equipe"] = {"$in": equipes}
            if data_inicio:
<<<<<<< HEAD
                filtro["data_inicio"] = {"$gte": data_inicio}
            if data_fim:
                filtro["data_fim"] = {"$lte": data_fim}
=======
                filtro["data_inicio"] = data_inicio
            if data_fim:
                filtro["data_fim"] = data_fim
>>>>>>> b2341e7889e447dffaa274c107459a9a67c2cca6

            logger.debug(f"Usando o filtro: {filtro}")

            # Executa a busca no banco de dados
            resultado = self.colecao.find(filtro)
            return list(resultado)  # Retorna os documentos encontrados
        except Exception as e:
            logger.error(f"Erro ao buscar dados com filtro: {e}")
            logger.exception("Detalhes completos da exceção:")
            return []
        

    def atualizar_dado(self, filtro, novo_valor):
        """
        Atualiza documentos que correspondem ao filtro.
        """
        try:
            resultado = self.colecao.update_many(filtro, {"$set": novo_valor})  # Corrigido para self.colecao
            print(f"{resultado.modified_count} documentos atualizados.")
            return resultado.modified_count
        except Exception as e:
            print(f"Erro ao atualizar dado: {e}")
            return 0

    def remover_dado(self, filtro):
        """
        Remove documentos que correspondem ao filtro.
        """
        try:
            resultado = self.colecao.delete_many(filtro)  # Corrigido para self.colecao
            print(f"{resultado.deleted_count} documentos removidos.")
            return resultado.deleted_count
        except Exception as e:
            print(f"Erro ao remover dado: {e}")
            return 0
        
        
    def inserir_ou_atualizar_dado(self, dado):
        """
        Atualiza ou insere um documento na coleção.
        Se existir um documento com o mesmo CPF e datas iguais, ele será atualizado.
        Caso contrário, será criado um novo registro.
        """
        try:
            dado = converter_datas(dado)  # Converte datas antes de inserir

            # Filtro para buscar um registro existente
            filtro = {
                "cpf": dado["cpf"],
                "data_inicio": dado["data_inicio"],
                "data_fim": dado["data_fim"]
            }

            # Define os dados a serem atualizados
            atualizacao = {"$set": dado}

            # Executa a operação de upsert
            result = self.colecao.update_one(filtro, atualizacao, upsert=True)

            if result.matched_count > 0:
                logger.info(f"Registro atualizado: CPF={dado['cpf']}")
            elif result.upserted_id:
                logger.info(f"Novo registro criado com ID: {result.upserted_id}")
            else:
                logger.warning("Nenhuma operação foi realizada.")

            return result.upserted_id or result.matched_count
        except Exception as e:
            logger.error(f"Erro ao inserir ou atualizar dado: {e}")
            logger.exception("Detalhes completos da exceção:")
            return None