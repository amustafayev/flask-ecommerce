

Demo E-commerce App implemented in flask

### Hot To Run in Local

- ### How to setup environment
    
    ```shell script
    $ git clone git@github.com:amustafayev/flask-ecommerce.git
    $ cd flask-ecommerce
    
    $ virtualenv venv
    $ source venv/bin/activate
    
    $ pip install -r requirements.txt
    ```

- ### How to migrate
    
    ```shell script
    $ flask db init 
    $ flask db migrate -m "Initial Migration"
    $ flask db upgrade  
    ```

- ### How to start
    
    ```shell script
    $ flask run -p 8000 --debug
    ```
- ### Links
    Application: http://127.0.0.1:8000
    
    Admin Panel: http://127.0.0.1:8000/admin