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
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #333; /* Dark background for night mode */
                color: #ccc; /* Light text color for readability in night mode */
            }
            .login-page-container, .home-page-container {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background-color: #333; /* Consistent background color */
            }
            .login-form {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 15px;
            }
            .login-input, .signup-button, .login-button {
                width: 250px;
                height: 40px;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #555;
                background-color: #222;
                color: #ddd;
            }
            .login-button, .signup-button {
                background-color: #0056b3; /* Slightly darker blue for better contrast */
                border: none;
            }
            .signup-button {
                background-color: #006400; /* Darker green for better contrast */
            }
            .home-page-container {
                display: flex;
                flex-direction: row;
                width: 100%;
            }
            .filters-container {
                width: 25%;
                height: 100vh; /* Full height */
                padding: 20px;
                background-color: #444; /* Slightly lighter shade for contrast */
                overflow-y: auto; /* Adds scroll to filters if they overflow vertically */
            }
            .graphs-container {
                width: 75%;
                display: flex;
                flex-direction: column;
                padding: 20px;
            }
            .graph {
                flex: 1;
                margin-bottom: 20px;
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