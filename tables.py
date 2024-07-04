from dotenv import load_dotenv
import os

# -------------------------------------------
# ---------------- load vars ----------------
# -------------------------------------------

load_dotenv()
pg_pass=os.getenv('PG_PASS')
pg_host=os.getenv('PG_HOST')
scylla_host=os.getenv('SCYLLA_HOST')
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------


pg_config = {
        'database': 'egabee',
        'user': 'egabee',
        'password': pg_pass,
        'host': pg_host,
        'port': '5432'
    }

scylla_config = {
        'contact_points': [scylla_host],
        'keyspace': 'egabee'
    }

#------ is reversed keywords --------- 
column_mapping = {
        'user_validation_codes': {
            'token': 'token_'
        },
        'cosmwasm_contract': {
            'schema': 'schema_'
        }
    }


table_names = [
    # "users",
    # "projects",
    # "auth_methods",
    # "user_auth_tokens",
    # "user_accounts",
    # "user_contacts",
    # "contact_confirmation_codes",
    # "user_telegram_info",
    # "user_email_notifications",
    # "user_slack_info",
    # "user_validation_codes",
    # "user_networks",
    # "user_contracts",
    # "user_tokens",
    # "user_wallets",
    # "user_nfts",
    # "user_relayer",
    # "user_contract_artifacts",
    # "cosmwasm_contract", 
    # "user_rollapp",
    # "alert_rules",
    # "alert_conditions",
    # "actions",
    # "historical_alerts",
    # "webhook_delivery_queue",
    # "web3_actions",
    # "web3_action_runs" ,
    # "cosmos_messages",
    # "cosmos_events",
    # "contracts",
    # "tokens",
    # "account_balances",
    # "relayer_info",
    "rollapp_info"
]
