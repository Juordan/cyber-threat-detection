
import re
import quopri
import html

from email.header import decode_header


def clean_email_text(text):
    """
    Membersihkan teks email menggunakan tahapan
    preprocessing yang digunakan pada training.
    """

    if text is None:
        return ""

    try:
        import pandas as pd
        if pd.isna(text):
            return ""
    except (ImportError, TypeError, ValueError):
        pass

    text = str(text)

    # 1. Decode MIME encoded words
    try:
        decoded_parts = decode_header(text)
        decoded_text = []

        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                try:
                    decoded_text.append(
                        part.decode(encoding or "utf-8", errors="replace")
                    )
                except (LookupError, UnicodeError):
                    decoded_text.append(
                        part.decode("utf-8", errors="replace")
                    )
            else:
                decoded_text.append(part)

        text = "".join(decoded_text)

    except Exception:
        pass

    # 2. Decode quoted-printable
    try:
        text = quopri.decodestring(
            text.encode("utf-8", errors="replace")
        ).decode("utf-8", errors="replace")
    except Exception:
        pass

    # 3. Decode HTML entities
    text = html.unescape(text)

    # 4. Remove HTML comments
    text = re.sub(
        r"<!--.*?-->",
        " ",
        text,
        flags=re.DOTALL
    )

    # 5. Remove script and style blocks
    text = re.sub(
        r"<(script|style)\b[^>]*>.*?</\1\s*>",
        " ",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    # 6. Remove remaining HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # 7. Convert to lowercase
    text = text.lower()

    # 8. Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text
