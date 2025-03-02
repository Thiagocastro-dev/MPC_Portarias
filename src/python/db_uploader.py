import os
import requests
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

class CouchDBUploader:
    def __init__(self, host='couchdb', port=5984, user='admin', password='mpc123'):
        self.base_url = f'http://{host}:{port}'
        self.auth = (user, password)
        self.batch_size = 100  # Número de documentos a serem carregados em cada lote

    def delete_database(self, db_name):
        """Delete database if it exists"""
        url = f'{self.base_url}/{db_name}'
        response = requests.delete(url, auth=self.auth)
        return response.status_code in [200, 404]
    
    def create_database(self, db_name):
        """Create a new database"""
        url = f'{self.base_url}/{db_name}'
        response = requests.put(url, auth=self.auth)
        
        # Criar os índices para melhor desempenho
        if response.status_code == 201:
            self._create_indexes(db_name)
        
        return response.status_code == 201
    
    def _create_indexes(self, db_name):
        """Create indexes for better query performance"""
        indexes = [
            {
                "index": {"fields": ["content"]},
                "name": "content-index",
                "type": "json"
            },
            {
                "index": {"fields": ["type"]},
                "name": "type-index",
                "type": "json"
            }
        ]
        
        for index in indexes:
            url = f'{self.base_url}/{db_name}/_index'
            requests.post(url, json=index, auth=self.auth)
    
    def upload_batch(self, db_name, documents):
        """Upload multiple documents in one request"""
        url = f'{self.base_url}/{db_name}/_bulk_docs'
        data = {"docs": documents}
        response = requests.post(url, json=data, auth=self.auth)
        return response.ok

def upload_batches_concurrently(uploader, db_name, document_batches):
    """Upload batches concurrently using ThreadPoolExecutor"""
    success_count = 0
    error_count = 0
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(uploader.upload_batch, db_name, batch): batch
            for batch in document_batches
        }
        for future in as_completed(futures):
            batch = futures[future]
            try:
                if future.result():
                    success_count += len(batch)
                    logging.info(f"Batch uploaded successfully: {len(batch)} documents")
                else:
                    error_count += len(batch)
                    logging.error(f"Error uploading batch of {len(batch)} documents")
            except Exception as e:
                error_count += len(batch)
                logging.error(f"Exception during batch upload: {str(e)}")
    
    return success_count, error_count

def recreate_database_and_upload(text_dir, database_name):
    """Recreate database and upload documents"""
    uploader = CouchDBUploader()
    
    # Deletar a base existente
    logging.info(f"Deleting existing database: {database_name}")
    if not uploader.delete_database(database_name):
        logging.error("Error deleting existing database")
        return False
    
    # Criar a nova base
    logging.info(f"Creating new database: {database_name}")
    if not uploader.create_database(database_name):
        logging.error("Error creating new database")
        return False
    
    # preparar documentos para upload em lote
    documents = []
    for filename in os.listdir(text_dir):
        if filename.endswith('.txt'):
            try:
                file_path = os.path.join(text_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                doc_id = os.path.splitext(filename)[0]
                documents.append({
                    '_id': doc_id,
                    'content': content,
                    'type': 'portaria'
                })
            except Exception as e:
                logging.error(f"Error processing file {filename}: {str(e)}")
    
    # Divide os documentos em lotes
    batch_size = uploader.batch_size
    document_batches = [documents[i:i + batch_size] for i in range(0, len(documents), batch_size)]
    
    # Carregar lotes simultaneamente
    logging.info(f"Uploading {len(documents)} documents in {len(document_batches)} batches")
    success_count, error_count = upload_batches_concurrently(uploader, database_name, document_batches)
    
    logging.info(f"Upload completed. Success: {success_count}, Errors: {error_count}")
    return success_count > 0
