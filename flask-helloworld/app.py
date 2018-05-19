from flask import Flask

#create application object
app = Flask(__name__)

#use decorator to link view function to the url
@app.route("/")
@app.route("/hello")
def hello_world():
  return 'Hello, world!'

#start development server
if __name__ == '__main__':
  app.run()
