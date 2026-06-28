"""Contact form and contact messages routes."""

import logging

import httpx
from fastapi import APIRouter, Request, HTTPException

from database import get_db
from auth import check_session
from config import EMAIL_WEBHOOK_URL

logger = logging.getLogger("just4tech.routes.contact")
router = APIRouter(tags=["contact"])


SUBJECT_LABELS = {
    "general": "General Inquiry",
    "tool-suggestion": "Tool Suggestion",
    "blog-topic": "Blog Topic Request",
    "bug": "Bug Report",
    "feedback": "Feedback",
    "other": "Other",
}


@router.post("/api/contact")
async def submit_contact(request: Request):
    data = await request.json()
    name = data.get("name", "")
    email = data.get("email", "")
    subject_key = data.get("subject", "general")
    msg_body = data.get("message", "")

    subject_label = SUBJECT_LABELS.get(subject_key, "General Inquiry")

    conn = get_db()
    conn.execute(
        "INSERT INTO contact_messages (name, email, subject, message) VALUES (?,?,?,?)",
        (name, email, subject_label, msg_body),
    )
    conn.commit()
    conn.close()

    # Fire-and-forget email notification
    try:
        httpx.post(EMAIL_WEBHOOK_URL, json={
            "name": name, "email": email,
            "subject": subject_key, "message": msg_body,
        }, timeout=5)
    except Exception:
        logger.warning("Failed to send email notification for contact form", exc_info=True)

    logger.info("Contact form submitted: %s <%s>", name, email)
    return {"ok": True, "message": "Message received. Thanks!"}


@router.get("/api/admin/contact-messages")
async def list_contact_messages(request: Request):
    user = check_session(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    conn = get_db()
    msgs = conn.execute(
        "SELECT * FROM contact_messages ORDER BY created_at DESC LIMIT 100"
    ).fetchall()
    conn.close()
    return [dict(m) for m in msgs]


@router.delete("/api/admin/contact-messages/{msg_id}")
async def delete_contact_message(msg_id: int, request: Request):
    user = check_session(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    conn = get_db()
    conn.execute("DELETE FROM contact_messages WHERE id = ?", (msg_id,))
    conn.commit()
    conn.close()
    logger.info("Contact message deleted: id=%d", msg_id)
    return {"ok": True}
