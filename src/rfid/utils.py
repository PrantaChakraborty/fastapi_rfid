

def generate_email_subject_body(rfid_obj):
    subject = f"Notice of Traffic Rule Violation: {rfid_obj.id}"
    body = (f"We are writing to inform you that on "
            f"{rfid_obj.created_at.date().strftime('%Y-%m-%d')} at "
            f"approximately"
            f" {rfid_obj.created_at.time().strftime('%H:%M %p')},"
            f" a violation of traffic rules was recorded against"
            f" your vehicle, {rfid_obj.rfid}")
    return subject, body