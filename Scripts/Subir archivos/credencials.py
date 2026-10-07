# ACCEDER A CREDENCIALES DE AZURE (LIBRERIAS DE AZURE)
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

# LA LIBRERIA DOTENV PERMITE ACCEDER A VALORES DE VARIABLES DE ENTORNO DEFINIDAS EN UN ARCHIVO .ENV
from dotenv import load_dotenv

# LA LIBRERIA OS PERMITE ACCEDER A VARIABLES DE ENTORNO DEL SISTEMA OPERATIVO
import os

# GENERAR UNA INSTANCIA DE DOTENV
load_dotenv()

def obtener_credenciales_azure():

    # SE DECLARAN VARIABLES DE ENTORNO PARA ACCEDER A CREDENCIALES DE AZURE
    cliente_id = os.getenv("AZURE_CLIENT_ID")
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")
    vault_url = os.getenv("AZURE_VAULT_URL")

    secret_name = os.getenv("SECRET_NAME")

    # SE PROCEDE A CREAR UNA CREDENCIAL
    credencial = ClientSecretCredential(
        client_id=cliente_id,               # CLIENTE ID
        client_secret=client_secret,        # CLIENTE SECRETO
        tenant_id=tenant_id                 # TENANT ID
    )

    # SE PROCEDE A CREAR UN CLIENTE PARA ACCEDER AL KEY VAULT
    secret_client = SecretClient(vault_url=vault_url, credential=credencial)

    # ACCEDER A UN SECRETO ESPECIFICO DEL KEY VAULT
    secret = secret_client.get_secret(secret_name)

    return credencial