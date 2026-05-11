from app import db
from app.models import Drawing


def submit_and_save(data):
    image_data = data.get('image')
    user_id = data.get('user_id')
    prompt_id = data.get('prompt_id')

    if not image_data:
        return False, "No image data provided."

    if not user_id or not prompt_id:
        return False, "Missing user or prompt information."

    try:
        drawing = Drawing(
            image=image_data,
            prompt_id=prompt_id,
            user_id=user_id
        )
        db.session.add(drawing)
        db.session.commit()
        return True, "Submitted!"
    except Exception as e:
        db.session.rollback()
        return False, f"Submission failed: {str(e)}"
