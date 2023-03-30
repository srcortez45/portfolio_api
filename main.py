if __name__ == '__main__':
    from uvicorn import run as uvicorn_run
    from app.utils.settings import cnf
    uvicorn_run(
    "app:app",
    host=cnf.HOST,
    port=cnf.APP_CONFIG.PORT,
    reload=cnf.DEBUG,
    proxy_headers=cnf.proxy_headers
    )