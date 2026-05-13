from app.models import Prompt, Drawing


def get_browsepage_data(selected_prompt="all", selected_date="all"):
    prompts = Prompt.query.order_by(Prompt.date.desc()).all()

    query = Drawing.query.order_by(Drawing.date.desc())

    if selected_prompt != "all":
        query = query.join(Prompt).filter(Prompt.text == selected_prompt)

    if selected_date != "all":
        query = query.filter(Drawing.date >= selected_date)

    drawings = query.all()
    dates = sorted(
        {drawing.date.date() for drawing in drawings if drawing.date},
        reverse=True
    )

    return {
        "prompts": prompts,
        "drawings": drawings,
        "dates": dates,
        "selected_prompt": selected_prompt,
        "selected_date": selected_date,
    }