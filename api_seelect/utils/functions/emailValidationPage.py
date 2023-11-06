# Function which returns the html of email validation page.
def email_validation_page():
    
    html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Confirmation</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin: 50px;
                }
            </style>
        </head>
        <body>
            <h1>Email Confirmed</h1>
            <p>Your email address has been successfully confirmed. You can now login to your account.</p>
        </body>
        </html>
    """
    
    return html