import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import email

class EmailService:

    @staticmethod
    def send_welcome_email(to_email: str, user_name: str):
        subject = "Bienvenido a nuestra plataforma"
        body = f"""
        <html>
            <body>
                <h2>Hola {user_name},</h2>
                <p>Tu cuenta ha sido creada exitosamente 🎉</p>
                <p>Gracias por registrarte en nuestra plataforma.</p>
                <br/>
                <p>Saludos,<br>El equipo de INFILE</p>
            </body>
        </html>
        """

        msg = MIMEMultipart()
        msg["From"] = email.EMAIL_USER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        try:
            with smtplib.SMTP(email.EMAIL_HOST, email.EMAIL_PORT) as server:
                server.starttls()
                server.login(email.EMAIL_USER, email.EMAIL_PASSWORD)
                server.sendmail(email.EMAIL_USER, to_email, msg.as_string())
            print(f"[EmailService] Correo enviado exitosamente a {to_email}")
            return True
        except Exception as e:
            print(f"[EmailService] Error al enviar correo: {e}")
            return False