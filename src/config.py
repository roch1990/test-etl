from os import getenv as env


class Config:

    app_name = 'aiohttp-blog'
    app_env = 'stage'

    app_log_level = env('LOG_LEVEL', 'DEBUG')

    db_host = env('DB_HOST', '192.168.122.1')
    db_port = env('DB_PORT', 5432)
    db_name = env('DB_NAME', 'test')
    db_pass = env('DB_PASS', 'test')
    db_user = env('DB_USER', 'test')

    source_url = "http://api.coincap.io/v2/rates"

    migrations = int(env('MIGRATIONS', 0))
