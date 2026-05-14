from datetime import datetime, timedelta
from app.models import Prompt, Drawing


def get_browsepage_data(selected_prompt="all", selected_date="all"):
    prompts = Prompt.query.order_by(Prompt.date.desc()).all()

    query = Drawing.query.order_by(Drawing.date.desc())

    if selected_prompt != "all":
        query = query.join(Prompt).filter(Prompt.text == selected_prompt)

    # Build the dates list before applying date filter, so the dropdown
    # always shows all available dates for the current prompt filter.
    all_for_dates = query.all()
    dates = sorted(
        {drawing.date.date() for drawing in all_for_dates if drawing.date},
        reverse=True
    )

    if selected_date != "all":
        try:
            parsed_date = datetime.strptime(selected_date, "%Y-%m-%d")
            next_day = parsed_date + timedelta(days=1)
            query = query.filter(Drawing.date >= parsed_date, Drawing.date < next_day)
        except (ValueError, TypeError):
            pass  # invalid date string — skip filter

    drawings = query.all()

    return {
        "prompts": prompts,
        "drawings": drawings,
        "dates": dates,
        "selected_prompt": selected_prompt,
        "selected_date": selected_date,
    }