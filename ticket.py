from PIL import Image, ImageDraw, ImageFont, ImageFilter
import qrcode
import os
import uuid

def generate_ticket(name, event_name, date, time, venue, unique_id):
    # Ticket dimensions
    ticket_width = 1000
    ticket_height = 600
    background_color = "white"

    # Create a blank image with a gradient background
    ticket = Image.new("RGB", (ticket_width, ticket_height), background_color)
    gradient = Image.new("RGB", (ticket_width, ticket_height), "#8697c4")
    for y in range(ticket_height):
        color = (255, 127 + y // 10, 80 + y // 15)  # Create gradient effect
        for x in range(ticket_width):
            gradient.putpixel((x, y), color)
    ticket = Image.blend(ticket, gradient, alpha=0.3)

    draw = ImageDraw.Draw(ticket)

    # Fonts (use modern fonts from Google Fonts)
    font_path = "arial.ttf"
    try:
        title_font = ImageFont.truetype(font_path, 50)
        text_font = ImageFont.truetype(font_path, 30)
        small_font = ImageFont.truetype(font_path, 20)
    except IOError:
        print("Default font not found. Using system fonts.")
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Add branding or a logo
    logo_size = (150, 150)
    try:
        logo = Image.open("image.png").resize(logo_size)
        ticket.paste(logo, (20, 20), logo)
    except FileNotFoundError:
        print("Logo not found. Skipping logo addition.")

    # Add text with modern fonts and layout
    draw.text((200, 30), event_name, fill="black", font=title_font)
    draw.text((200, 100), f"Name: {name}", fill="black", font=text_font)
    draw.text((200, 150), f"Date: {date}", fill="black", font=text_font)
    draw.text((200, 200), f"Time: {time}", fill="black", font=text_font)
    draw.text((200, 250), f"Venue: {venue}", fill="black", font=text_font)
    draw.text((200, 300), f"Ticket ID: {unique_id}", fill="black", font=text_font)

    # Generate a stylized QR code
    qr_data = f"Name: {name}\nEvent: {event_name}\nDate: {date}\nTime: {time}\nVenue: {venue}\nTicket ID: {unique_id}"
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    qr_size = 200
    qr_img = qr_img.resize((qr_size, qr_size))
    ticket.paste(qr_img, (ticket_width - qr_size - 50, ticket_height - qr_size - 50))

    # Save the ticket
    output_dir = "modern_tickets"
    os.makedirs(output_dir, exist_ok=True)
    ticket_path = os.path.join(output_dir, f"{unique_id}_ticket.png")
    ticket.save(ticket_path)

    print(f"Modern ticket generated: {ticket_path}")

# Generate tickets
attendees_list = ["ANANYA SINGH"]
for attendee in attendees_list:
    unique_id = str(uuid.uuid4())[:8]  # Generate a short unique ID
    generate_ticket(
        name=attendee,
        event_name="TechBuzz 2.0",
        date="2025-01-15",
        time="10:00 AM",
        venue="Auditorium,Raman Block",
        unique_id=unique_id
    )
