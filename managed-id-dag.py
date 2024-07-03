import pyodbc,struct
from datetime import datetime
from azure.identity import DefaultAzureCredential,AzureCliCredential,ManagedIdentityCredential


asql_driver="{ODBC Driver 17 for SQL Server}" #Variable.get("ASQL-DRIVER-SKIPPED-JOB")
asql_db="[sqldb-mlx-dev001]"#"[sqldb-mlx-dev001]" #Variable.get("ASQL-DB-SKIPPED-JOB")
asql_client_id="437ac755-97cf-4d77-b58c-7f8f50784c0a" #Variable.get("AKS-IDENTITY")
asql_server="sql-mlx-dev001.database.windows.net" #Variable.get("ASQL-SERVER-SKIPPED-JOB")


def get_asql_conn():

    connection_string=f"Driver={asql_driver};Server=tcp:{asql_server},1433;Database={asql_db};"
    #credential = DefaultAzureCredential(managed_identity_client_id=asql_client_id)
    credential = ManagedIdentityCredential(client_id=asql_client_id)
    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256
    conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    print(f"conn::{conn}")
    
    cursor = conn.cursor()
    sql_script=f"select count(*) from {asql_db}.bridge.[WorkflowFollowupStatusType]"
 
    cursor.execute(sql_script)
    conn.commit()
    cursor.close()
    conn.close()
 

get_asql_conn()





