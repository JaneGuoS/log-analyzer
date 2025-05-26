clear
export MONGODB_URL='mongodb+srv://guojingy:Z31RkCXUT4fFJ3Dv@logcluster.iqnxm86.mongodb.net/?tlsAllowInvalidCertificates=true'
export MONGODB_DBNAME='logs_database'

export LOGS_DIR='../store/logs'
export STREAMLIT_SERVER_FOLDER_WATCH_BLACKLIST="venv,env,site-packages,torch"

streamlit run main.py