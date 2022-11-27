from uvicorn import run


if __name__ == "__main__":
    run(app="app:api", host="0.0.0.0", port=4000)
