from sqlalchemy.exc import IntegrityError
from app import db
from app.models import Drawing


def submit_and_save(user_id, data):
    image_data = data.get('image')
    prompt_id = data.get('prompt_id')

    if not image_data:
        return False, "No image data provided.", None

    if not prompt_id:
        return False, "Missing prompt information.", None

    try:
        drawing = Drawing(
            image=image_data,
            prompt_id=prompt_id,
            user_id=user_id
        )
        db.session.add(drawing)
        db.session.commit()
        return True, "Submitted!", drawing.id
    except IntegrityError:
        db.session.rollback()
        return False, "You have already submitted a drawing for this prompt.", None
    except Exception as e:
        db.session.rollback()
        return False, f"Submission failed: {str(e)}", None
