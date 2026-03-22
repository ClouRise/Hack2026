# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
# from app.core.config import settings
# from pydantic import SecretStr, EmailStr


# # Конфигурация
# conf = ConnectionConfig(
#     MAIL_USERNAME=settings.MAIL_USERNAME,      # Email от которого отправляем
#     MAIL_PASSWORD=settings.MAIL_PASSWORD,      # Пароль (App Password для Gmail)
#     MAIL_FROM=settings.MAIL_FROM,              # Email "От кого" (показывается получателю)
#     MAIL_PORT=settings.MAIL_PORT,              # Порт SMTP сервера
#     MAIL_SERVER=settings.MAIL_SERVER,          # Адрес SMTP сервера
#     MAIL_FROM_NAME="ПрофДНК",                  # Имя отправителя (показывается получателю)
#     MAIL_STARTTLS=True,                        # Шифрование TLS
#     MAIL_SSL_TLS=False,                        # SSL шифрование (не используем, т.к. STARTTLS)
#     USE_CREDENTIALS=True,                      # Использовать логин/пароль
#     VALIDATE_CERTS=True                        # Проверять SSL сертификаты
# )

# fm = FastMail(conf)


# async def send_new_psychologist_email(email: str, name: str, password: str):
#     """Отправка пароля новому психологу"""
    
#     html = f"""
#     <h2>Добро пожаловать в ПрофДНК!</h2>
#     <p>Здравствуйте, {name}!</p>
#     <p>Для вас создан аккаунт психолога.</p>
#     <p><strong>Email:</strong> {email}<br>
#     <strong>Пароль для входа:</strong> {password}</p>
#     """
    
#     message = MessageSchema(
#         subject="Ваш аккаунт в ПрофДНК",
#         recipients=[email], # type: ignore
#         body=html,
#         subtype=MessageType.html
#     )
    
#     await fm.send_message(message)