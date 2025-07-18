import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.0.21", port=8000, reload=True)

