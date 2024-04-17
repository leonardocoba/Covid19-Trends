import dash
import query
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server


# Adding custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <style>
            .login-page-container {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: grey;
                padding: 20px; /* Add some padding */
            }
            .login-form {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 15px;
                margin-top: 40px; /* Add margin to top to separate from title */
            }
            .login-input {
                width: 250px;
                height: 40px;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ddd;
            }
            .login-button, .signup-button {
                cursor: pointer;
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
                background-color: #007bff;
                color: white;
                font-size: 16px;
            }
            .signup-button {
                background-color: #28a745;
            }
            .login-title {
                color: white;
                text-align: center;
                margin-bottom: 20px; /* Increased margin-bottom to separate from the login form */
                font-size: 48px; /* Increased font size */
                margin-top: 100px; /* Set margin top to 0 to stick at the top */
                width: 100%;
                position: absolute;
                top: 0; /* Position at the top */
                left: 0; /* Align to left */
            }
        </style>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
