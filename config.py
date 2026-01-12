class Config:
    # MySQL Database Configuration
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'              # Your MySQL username
    MYSQL_PASSWORD = 'rootroot' # Your MySQL password
    MYSQL_DB = 'ehr_system'          # Database name
    
    # Flask Configuration
    SECRET_KEY = '46734c7ddb5909c0d5fdd3a46fbebcb1b3f0724c7225ae202a0ff878bc4bbc03'
    
    # Upload Configuration
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
