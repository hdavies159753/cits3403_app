"""
Seed script — populates the database with dummy data for development.
Idempotent: skips seeding if data already exists.
Uses only the Python standard library (no Pillow).
"""

import base64
import io
import random
import struct
import zlib
from datetime import date, datetime, timedelta, timezone

from app import create_app, db
from app.models import Drawing, Prompt, User, Vote


# ---------------------------------------------------------------------------
# Pure-Python minimal PNG generator (256x256, solid-colour rectangles)
# ---------------------------------------------------------------------------

def _make_png(width, height, pixels):
    """Create a PNG file from raw RGB pixel rows.

    *pixels* is a list of *height* rows, each row a list of *width*
    ``(r, g, b)`` tuples.
    """

    def chunk(chunk_type, data):
        c = chunk_type + data
        crc = struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
        return struct.pack(">I", len(data)) + c + crc

    header = b"\x89PNG\r\n\x1a\n"
    ihdr = chunk(
        b"IHDR",
        struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0),
    )

    raw = b""
    for row in pixels:
        raw += b"\x00"  # filter byte (None)
        for r, g, b_ in row:
            raw += struct.pack("BBB", r, g, b_)

    idat = chunk(b"IDAT", zlib.compress(raw))
    iend = chunk(b"IEND", b"")
    return header + ihdr + idat + iend


def generate_drawing_image(seed_value):
    """Return a ``data:image/png;base64,...`` string of a 256x256 image with
    random coloured rectangles, deterministic for the given *seed_value*."""

    rng = random.Random(seed_value)
    w, h = 256, 256

    # start with a white canvas
    pixels = [[(255, 255, 255)] * w for _ in range(h)]

    # draw 3-6 random solid-colour rectangles
    for _ in range(rng.randint(3, 6)):
        colour = (rng.randint(30, 230), rng.randint(30, 230), rng.randint(30, 230))
        x1 = rng.randint(0, w - 40)
        y1 = rng.randint(0, h - 40)
        x2 = rng.randint(x1 + 20, min(x1 + 120, w))
        y2 = rng.randint(y1 + 20, min(y1 + 120, h))
        for y in range(y1, y2):
            for x in range(x1, x2):
                pixels[y][x] = colour

    png_bytes = _make_png(w, h, pixels)
    b64 = base64.b64encode(png_bytes).decode("ascii")
    return f"data:image/png;base64,{b64}"


# ---------------------------------------------------------------------------
# Seed data definitions
# ---------------------------------------------------------------------------

USERS = [
    ("ArtistOne", "password123"),
    ("SketchMaster", "password123"),
    ("DoodleFan", "password123"),
    ("PixelArtist", "password123"),
    ("CreativeGenius", "password123"),
]

PROMPTS = [
    "A cat wearing a top hat",
    "Dragon working at McDonald's",
    "Cat flying a plane",
    "Robot on holiday",
    "Penguin playing guitar",
    "Alien visiting a coffee shop",
    "Dinosaur riding a skateboard",
]


def seed():
    """Wipe all data and insert fresh dummy users, prompts, drawings and votes."""

    print("Wiping database …")
    Vote.query.delete()
    Drawing.query.delete()
    Prompt.query.delete()
    User.query.delete()
    db.session.commit()

    print("Seeding database …")

    # --- Admin user ---
    admin = User(username="adminuser")
    admin.set_password("adminuserpass")
    db.session.add(admin)

    # --- Users ---
    users = []
    for username, password in USERS:
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        users.append(user)
    db.session.flush()  # assigns ids

    all_users = [admin] + users

    # --- Prompts (today through 6 days ago) ---
    today = date.today()
    prompts = []
    for i, text in enumerate(PROMPTS):
        prompt = Prompt(text=text, date=today - timedelta(days=i))
        db.session.add(prompt)
        prompts.append(prompt)
    db.session.flush()

    # --- Drawings (2-4 per prompt, each from a different user) ---
    # Skip today's prompt so users can submit fresh drawings.
    # Exclude admin from the artist pool entirely.
    artist_pool = [u for u in all_users if u.username != "adminuser"]
    drawings = []
    image_seed = 1
    for prompt in prompts[1:]:  # skip index 0 (today's prompt)
        num_artists = min(random.randint(2, 4), len(artist_pool))
        artists = random.sample(artist_pool, num_artists)
        for user in artists:
            image_data = generate_drawing_image(image_seed)
            drawing = Drawing(
                image=image_data,
                user_id=user.id,
                prompt_id=prompt.id,
                date=datetime.combine(
                    prompt.date, datetime.min.time()
                ).replace(tzinfo=timezone.utc),
            )
            db.session.add(drawing)
            drawings.append(drawing)
            image_seed += 1
    db.session.flush()

    # --- Votes (random, respecting constraints) ---
    vote_count = 0
    for drawing in drawings:
        # each drawing gets 0-4 votes from random users (not the artist)
        eligible_voters = [u for u in all_users if u.id != drawing.user_id]
        num_votes = random.randint(0, min(4, len(eligible_voters)))
        voters = random.sample(eligible_voters, num_votes)
        for voter in voters:
            v = Vote(voter_id=voter.id, drawing_id=drawing.id)
            db.session.add(v)
            vote_count += 1

    db.session.commit()

    print(
        f"Seeded: {len(all_users)} users, {len(prompts)} prompts, "
        f"{len(drawings)} drawings, {vote_count} votes."
    )


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed()
