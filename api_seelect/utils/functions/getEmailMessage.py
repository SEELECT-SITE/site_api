# Function used to get the email message, send with the link to validate the email.
def get_email_message(link):
    
    message = """
        Olá,

        Bem-vindo a SEELECT! Estamos muito felizes em tê-lo conosco.

        Para confirmar o seu cadastro, clique no link abaixo:

        {link}

        Se você não se cadastrou na SEELECT, por favor, ignore este e-mail.

        Estamos empolgados para tê-lo como participante do nosso evento e esperamos que você aproveite ao máximo a sua experiência na SEELECT.

        Atenciosamente,
        A Equipe da SEELECT
    """.format(link=link)
    
    return message

# Function used to get the forget password email message, send with the new password.
def get_forget_password_message(password):
    
    message = """
        Olá,

        Recebemos uma solicitação para redefinir a senha da sua conta. Abaixo está a sua nova senha:

        Nova Senha: {password}

        Por favor, faça login com essa nova senha e lembre-se de alterá-la para uma de sua escolha assim que entrar na sua conta.

        Se você não solicitou uma redefinição de senha, por favor, entre em contato conosco imediatamente.

        Atenciosamente,
        A Equipe da SEELECT
    """.format(password=password)
    
    return message