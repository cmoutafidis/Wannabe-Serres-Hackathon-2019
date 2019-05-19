DATABASE_CONFIG = {
    'host': 'localhost',
    'dbName': 'apachelogs',
    'user': 'user',
    'password': 'password',
    'createSchemas': [
                    """CREATE TABLE IF NOT EXISTS apachelogs.requests (
                      id INT NOT NULL AUTO_INCREMENT,
                      remote_host VARCHAR(255) NULL,
                      remote_logname VARCHAR(255) NULL,
                      remote_user VARCHAR(255) NULL,
                      time_received_tz_isoformat VARCHAR(255) NULL,
                      request_first_line VARCHAR(255) NULL,
                      request_method VARCHAR(255) NULL,
                      request_url VARCHAR(255) NULL,
                      request_http_ver VARCHAR(255) NULL,
                      request_url_scheme VARCHAR(255) NULL,
                      request_url_netloc VARCHAR(255) NULL,
                      request_url_path VARCHAR(255) NULL,
                      request_url_query VARCHAR(255) NULL,
                      request_url_fragment VARCHAR(255) NULL,
                      request_url_username VARCHAR(255) NULL,
                      request_url_password VARCHAR(255) NULL,
                      request_url_hostname VARCHAR(255) NULL,
                      request_url_port VARCHAR(255) NULL,
                      status VARCHAR(255) NULL,
                      response_bytes_clf VARCHAR(255) NULL,
                      request_type VARCHAR(45) NULL DEFAULT 'OK',
                      PRIMARY KEY (id));
    ""","""CREATE TABLE IF NOT EXISTS apachelogs.uniqueips (
                      id INT NOT NULL AUTO_INCREMENT,
                      ip VARCHAR(255) NULL,
                      country VARCHAR(255) NULL,
                      totalRequests INT NULL,
                      code VARCHAR(255) NULL,
                      PRIMARY KEY (id));
    """
    ]
}
