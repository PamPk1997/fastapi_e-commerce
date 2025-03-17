from xhtml2pdf import pisa
from jinja2 import Template
from io import BytesIO

async def generate_invoice_pdf(order_details: dict) -> BytesIO:
    # Use Jinja2 to render the HTML with dynamic order details
    template = Template("""
    <html>
        <body>
            <h1>Invoice</h1>
            <p><strong>Order ID:</strong> {{ order_id }}</p>
            <p><strong>Customer Name:</strong> {{ customer_name }}</p>
            <p><strong>Total Amount:</strong> ₹{{ total_amount }}</p>
            <hr>
            <h3>Products</h3>
            <ul>
            {% for item in products %}
                <li>{{ item.name }} - ₹{{ item.price }} x {{ item.quantity }}</li>
            {% endfor %}
            </ul>
        </body>
    </html>
    """)

    # Fill the template with dynamic order data
    html = template.render(order_id=order_details["order_id"], customer_name=order_details["customer_name"],
                           total_amount=order_details["total_amount"], products=order_details["products"])

    # Create PDF from the rendered HTML
    pdf_bytes = BytesIO()
    pisa_status = pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=pdf_bytes)
    
    if pisa_status.err:
        return None
    
    pdf_bytes.seek(0)  # Reset the BytesIO cursor
    return pdf_bytes
