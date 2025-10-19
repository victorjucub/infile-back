import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import email

class EmailService:

    def __init__(self):
        self.INFILE_NEWS_URL = 'http://localhost/infile-front/vistas'

    def sendWelcomeEmail(self, to_email: str, user_name: str, token_activate: str):
        print("[EmailService][sendWelcomeEmail] -> Ejecutando proceso ")
        subject = "[IFILE NEWS]: Bienvenido a nuestra plataforma !"
        body = f"""
            <html>
                <body>
                    <h2>Hola {user_name},</h2>
                    <p>Tu cuenta ha sido creada exitosamente 🎉</p>
                    <p>Gracias por registrarte en nuestra plataforma.</p>
                    <br/>
                    <p>Para confirmar tu cuenta, debes acceder a este link: {self.INFILE_NEWS_URL}/login.php?process={token_activate}</p>
                    <br/>
                    <p>Saludos,<br>El equipo de INFILE</p>
                </body>
            </html>
        """

        msg = MIMEMultipart()
        msg["From"] = "[INFILE NEWS] Victor Jucub"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        try:
            with smtplib.SMTP(email.EMAIL_HOST, email.EMAIL_PORT) as server:
                server.starttls()
                server.login(email.EMAIL_USER, email.EMAIL_PASSWORD)
                server.sendmail(email.EMAIL_USER, to_email, msg.as_string())
            print(f"[EmailService][sendWelcomeEmail] Correo enviado exitosamente a {to_email}")
            return True
        except Exception as e:
            print(f"[EmailService][sendWelcomeEmail] Error al enviar correo: {e}")
            return False
        
    def sendWelcomeGoogleEmail(self, to_email: str, user_name: str):
        print("[EmailService][sendWelcomeGoogleEmail] -> Ejecutando proceso ")
        subject = "[IFILE NEWS]: Bienvenido a nuestra plataforma !"
        body = f"""
            <html>
                <body>
                    <h2>Hola {user_name},</h2>
                    <p>Tu cuenta ha sido creada exitosamente 🎉</p>
                    <p>Gracias por registrarte en nuestra plataforma.</p>
                    <br/>
                    <p>Tu cuenta ha sido creada mediante un inicio de sesión con Google</p>
                    <br/>
                    <p>Saludos,<br>El equipo de INFILE</p>
                </body>
            </html>
        """

        msg = MIMEMultipart()
        msg["From"] = "[INFILE NEWS] Victor Jucub"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        try:
            with smtplib.SMTP(email.EMAIL_HOST, email.EMAIL_PORT) as server:
                server.starttls()
                server.login(email.EMAIL_USER, email.EMAIL_PASSWORD)
                server.sendmail(email.EMAIL_USER, to_email, msg.as_string())
            print(f"[EmailService][sendWelcomeGoogleEmail] Correo enviado exitosamente a {to_email}")
            return True
        except Exception as e:
            print(f"[EmailService][sendWelcomeGoogleEmail] Error al enviar correo: {e}")
            return False
        
    def sendRestorePasswordEmail(self, to_email: str, user_name: str, token_password: str):
        print("[EmailService][sendRestorePasswordEmail] -> Ejecutando proceso ")
        subject = "[IFILE NEWS]: Solicitud para restablecer contraseña !"
        body = f"""
            <html>
                <body>
                    <h2>Hola {user_name},</h2>
                    <p>Has hecho una solicitud para restablecer tu contraseña 🎉</p>
                    <p>Para continuar con el proceso debes hacer click en el siguiente enlace:</p>
                    <br/>
                    <p>{self.INFILE_NEWS_URL}/restablecer-clave.php?process={token_password}</p>
                    <br/>
                    <p>Saludos,<br>El equipo de INFILE</p>
                </body>
            </html>
        """

        msg = MIMEMultipart()
        msg["From"] = "[INFILE NEWS] Victor Jucub"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        try:
            with smtplib.SMTP(email.EMAIL_HOST, email.EMAIL_PORT) as server:
                server.starttls()
                server.login(email.EMAIL_USER, email.EMAIL_PASSWORD)
                server.sendmail(email.EMAIL_USER, to_email, msg.as_string())
            print(f"[EmailService][sendRestorePasswordEmail] Correo enviado exitosamente a {to_email}")
            return True
        except Exception as e:
            print(f"[EmailService][sendRestorePasswordEmail] Error al enviar correo: {e}")
            return False