from app import app

@app.route('/')
def helloWorld():
    return "Hello World"