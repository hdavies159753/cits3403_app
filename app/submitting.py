from app import db
from app.models import Drawing

def submit_and_save (data):

    image_data = data.get('image')

    drawing = Drawing(
        image = image_data,
        prompt_id=2,
        user_id=2
    )
    db.session.add(drawing)
    db.session.commit()
    return True, "Subbmited!"
        