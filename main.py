from uvicorn import run


if __name__ == "__main__":
    run(app="app:api", port=4000, reload=True)
