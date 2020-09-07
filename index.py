from shorturl import app

if __name__ == '__main__':
    # ! Take out the debug argument
    app.run(debug=True, port=8000)