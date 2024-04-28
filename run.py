''' This is the entry point of the application. It creates the app and runs it. 

The app is created using the app factory pattern.

Contributors:
    - Sam Sui
    - Jovi Yoshioka
'''

# Package modules
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)