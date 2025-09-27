from email.message import EmailMessage

from app.config import settings


def create_confirmation(email_to: str):
    email = EmailMessage()
    email["Subject"] = "Shop confirmation"
    email["From"] = settings.GM_USER
    email["To"] = email_to
    email.set_content(
        f"""
            <h1>Shop confirmation</h1>
            <p>details:</p>
            """,
        subtype="html"
    )
    return email

def access_order(email_to: str, product_data: dict):
    email = EmailMessage()
    email["Subject"] = "Your order"
    email["From"] = settings.GM_USER
    email["To"] = email_to
    email.set_content(
        f"""
                <h1>Your order success 🎉</h1>
                <p>Thank you for your purchase!</p>
                 <p><b>Product:</b> {product_data} </p>
                """,
        subtype="html"
    )

    return email
