from eve import Eve

app = Eve()

if __name__ == '__main__':
    # ! Always take out the debug argument
    # ! Default port is 5000
    app.run(debug=True)