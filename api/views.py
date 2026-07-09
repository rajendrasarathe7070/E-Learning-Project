from __future__ import annotations

from datetime import datetime
from typing import Any

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.http import JsonResponse, HttpRequest, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from core.models import Branch, Note, Book, PYQ, Syllabus, Doubt, Reply, Bookmark

User = get_user_model()


def _json_error(message: str, status: int = 400, **extra: Any) -> JsonResponse:
    payload = {"error": message}
    payload.update(extra)
    return JsonResponse(payload, status=status)


def _require_login(request: HttpRequest):
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    return None


def _parse_int(val: Any, default: int | None = None) -> int | None:
    try:
        if val is None:
            return default
        return int(val)
    except (TypeError, ValueError):
        return default


@require_http_methods(["GET"])
def health_check(request: HttpRequest):
    """Health check endpoint to keep server alive on Render."""
    return JsonResponse(
        {
            "status": "ok",
            "message": "Server is running",
            "timestamp": datetime.now().isoformat(),
            "service": "eLearn-for-study",
        }
    )


# -----------------
# Notes
# -----------------


def _note_to_dict(note: Note, *, is_mine: bool = False) -> dict[str, Any]:
    pdf_url = None
    if note.pdf_file:
        try:
            pdf_url = note.pdf_file.url
        except Exception:
            pdf_url = None
    if note.pdf_link:
        pdf_url = note.pdf_link

    tags = []
    if note.tags:
        tags = [t.strip() for t in note.tags.split(",") if t.strip()]

    return {
        "id": note.id,
        "title": note.title,
        "subject": note.subject,
        "description": note.description,
        "tags": tags,
        "branch": note.branch.code if note.branch_id else None,
        "semester": note.semester,
        "unit": note.unit,
        "pdf_url": pdf_url,
        "uploaded_by": getattr(note.uploaded_by, "username", None) or getattr(note.uploaded_by, "name", None),
        "uploaded_at": note.uploaded_at.isoformat() if hasattr(note.uploaded_at, "isoformat") else str(note.uploaded_at),
        "download_count": note.download_count,
        "is_mine": is_mine,
    }


@require_http_methods(["GET"])
def notes_list(request: HttpRequest):
    q = (request.GET.get("search") or "").strip()
    branch_code = (request.GET.get("branch") or "all").strip()
    semester = (request.GET.get("semester") or "all").strip()

    qs = Note.objects.select_related("branch", "uploaded_by")

    if branch_code and branch_code.lower() != "all":
        qs = qs.filter(branch__code=branch_code)

    if semester and semester.lower() != "all":
        sem_int = _parse_int(semester)
        if sem_int is not None:
            qs = qs.filter(semester=sem_int)

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(subject__icontains=q) | Q(description__icontains=q) | Q(tags__icontains=q))

    notes = []
    is_mine_user = request.user if getattr(request, "user", None) and request.user.is_authenticated else None
    for n in qs.order_by("-uploaded_at", "-id")[:200]:
        notes.append(_note_to_dict(n, is_mine=(is_mine_user is not None and n.uploaded_by_id == is_mine_user.id)))

    return JsonResponse({"notes": notes})


@require_http_methods(["POST"])
def upload_note(request: HttpRequest):
    login_err = _require_login(request)
    if login_err:
        return login_err

    title = (request.POST.get("title") or "").strip()
    subject = (request.POST.get("subject") or "").strip()
    branch_code = (request.POST.get("branch") or "").strip()
    semester = _parse_int(request.POST.get("semester"), None)
    unit = _parse_int(request.POST.get("unit"), None)
    description = (request.POST.get("description") or "").strip()
    tags = (request.POST.get("tags") or "").strip()
    cover_link = (request.POST.get("cover_link") or "").strip()
    pdf_link = (request.POST.get("pdf_link") or "").strip()

    if not title or not subject or not branch_code or semester is None or unit is None or not pdf_link:
        return _json_error("Missing required fields")

    branch = Branch.objects.filter(code=branch_code).first()
    if not branch:
        return _json_error("Invalid branch")

    note = Note.objects.create(
        title=title,
        subject=subject,
        branch=branch,
        semester=semester,
        unit=unit,
        description=description,
        tags=tags,
        pdf_link=pdf_link,
        cover_link=cover_link,
        uploaded_by=request.user,
    )

    return JsonResponse({"ok": True, "id": note.id})


@require_http_methods(["POST", "PUT"])
def download_note(request: HttpRequest, note_id: int):
    # No strict auth required for download (based on frontend)
    note = Note.objects.filter(id=note_id).first()
    if not note:
        return _json_error("Note not found", status=404)

    # increment
    Note.objects.filter(id=note_id).update(download_count=models.F("download_count") + 1)  # type: ignore[name-defined]

    # return pdf_url
    pdf_url = note.pdf_link
    if note.pdf_file:
        try:
            pdf_url = note.pdf_file.url
        except Exception:
            pass

    return JsonResponse({"ok": True, "pdf_url": pdf_url})


@require_http_methods(["POST"])
def toggle_bookmark(request: HttpRequest, note_id: int):
    login_err = _require_login(request)
    if login_err:
        return login_err

    note = Note.objects.filter(id=note_id).first()
    if not note:
        return _json_error("Note not found", status=404)

    bookmarked = Bookmark.objects.filter(user=request.user, note=note).exists()
    if bookmarked:
        Bookmark.objects.filter(user=request.user, note=note).delete()
        return JsonResponse({"bookmarked": False})

    Bookmark.objects.create(user=request.user, note=note)
    return JsonResponse({"bookmarked": True})


@require_http_methods(["DELETE"])
def delete_note(request: HttpRequest, note_id: int):
    login_err = _require_login(request)
    if login_err:
        return login_err

    note = Note.objects.filter(id=note_id).first()
    if not note:
        return _json_error("Note not found", status=404)

    if note.uploaded_by_id != request.user.id and getattr(request.user, "role", None) != "super_student":
        return HttpResponseForbidden("Not permitted")

    note.delete()
    return JsonResponse({"ok": True})


# -----------------
# Books
# -----------------


def _book_to_dict(b: Book) -> dict[str, Any]:
    pdf_url = b.pdf_link
    if b.pdf_file:
        try:
            pdf_url = b.pdf_file.url
        except Exception:
            pass

    return {
        "id": b.id,
        "title": b.title,
        "author": b.author,
        "subject": b.subject,
        "branch": b.branch.code if b.branch_id else None,
        "semester": b.semester,
        "rating": b.rating,
        "cover_gradient": b.cover_gradient,
        "cover_link": b.cover_link,
        "description": b.description,
        "pdf_url": pdf_url,
    }


@require_http_methods(["GET"])
def books_list(request: HttpRequest):
    branch_code = (request.GET.get("branch") or "all").strip()
    qs = Book.objects.select_related("branch")
    if branch_code and branch_code.lower() != "all":
        qs = qs.filter(branch__code=branch_code)
    books = [_book_to_dict(b) for b in qs.order_by("-id")[:200]]
    return JsonResponse({"books": books})


@require_http_methods(["POST"])
def upload_book(request: HttpRequest):
    login_err = _require_login(request)
    if login_err:
        return login_err

    if getattr(request.user, "role", None) != "super_student":
        return HttpResponseForbidden("Only super students can upload")

    title = (request.POST.get("title") or "").strip()
    author = (request.POST.get("author") or "").strip()
    subject = (request.POST.get("subject") or "").strip()
    branch_code = (request.POST.get("branch") or "").strip()
    semester = _parse_int(request.POST.get("semester"), None)
    rating = _parse_int(request.POST.get("rating"), None)
    description = (request.POST.get("description") or "").strip()
    cover_gradient = (request.POST.get("cover_gradient") or "").strip() or "linear-gradient(135deg,#6c63ff,#00d4ff)"
    cover_link = (request.POST.get("cover_link") or "").strip()
    pdf_link = (request.POST.get("pdf_link") or "").strip()

    if not title or not author or not subject or not branch_code or semester is None or rating is None or not pdf_link:
        return _json_error("Missing required fields")

    branch = Branch.objects.filter(code=branch_code).first()
    if not branch:
        return _json_error("Invalid branch")

    Book.objects.create(
        title=title,
        author=author,
        subject=subject,
        branch=branch,
        semester=semester,
        rating=rating,
        cover_gradient=cover_gradient,
        description=description,
        cover_link=cover_link,
        pdf_link=pdf_link,
    )

    return JsonResponse({"ok": True})


# -----------------
# PYQ
# -----------------


def _pyq_to_dict(p: PYQ) -> dict[str, Any]:
    pdf_url = p.pdf_link
    if p.pdf_file:
        try:
            pdf_url = p.pdf_file.url
        except Exception:
            pass

    return {
        "id": p.id,
        "subject": p.subject,
        "branch": p.branch.code if p.branch_id else None,
        "semester": p.semester,
        "year": p.year,
        "exam_type": p.exam_type,
        "pdf_url": pdf_url,
    }


@require_http_methods(["GET"])
def pyqs_list(request: HttpRequest):
    branch_code = (request.GET.get("branch") or "all").strip()
    exam_type = (request.GET.get("exam_type") or "all").strip()
    year = request.GET.get("year")

    qs = PYQ.objects.select_related("branch")
    if branch_code and branch_code.lower() != "all":
        qs = qs.filter(branch__code=branch_code)
    if exam_type and exam_type.lower() != "all":
        qs = qs.filter(exam_type=exam_type)
    if year and year.lower() != "all":
        y = _parse_int(year)
        if y is not None:
            qs = qs.filter(year=y)

    pyqs = [_pyq_to_dict(p) for p in qs.order_by("-year", "-id")[:500]]
    return JsonResponse({"pyqs": pyqs})


@require_http_methods(["POST"])
def upload_pyq(request: HttpRequest):
    login_err = _require_login(request)
    if login_err:
        return login_err

    if getattr(request.user, "role", None) != "super_student":
        return HttpResponseForbidden("Only super students can upload")

    subject = (request.POST.get("subject") or "").strip()
    branch_code = (request.POST.get("branch") or "").strip()
    semester = _parse_int(request.POST.get("semester"), None)
    year = _parse_int(request.POST.get("year"), None)
    exam_type = (request.POST.get("exam_type") or "").strip()
    pdf_link = (request.POST.get("pdf_link") or "").strip()

    if not subject or not branch_code or semester is None or year is None or not exam_type or not pdf_link:
        return _json_error("Missing required fields")

    branch = Branch.objects.filter(code=branch_code).first()
    if not branch:
        return _json_error("Invalid branch")

    PYQ.objects.create(
        subject=subject,
        branch=branch,
        semester=semester,
        year=year,
        exam_type=exam_type,
        pdf_link=pdf_link,
    )

    return JsonResponse({"ok": True})


# -----------------
# Syllabus
# -----------------


def _syllabus_to_dict(s: Syllabus) -> dict[str, Any]:
    pdf_url = s.pdf_link
    if s.pdf_file:
        try:
            pdf_url = s.pdf_file.url
        except Exception:
            pass

    return {
        "id": s.id,
        "subject_name": s.subject_name,
        "subject_code": s.subject_code,
        "branch": s.branch.code if s.branch_id else None,
        "semester": s.semester,
        "units": s.units,
        "pdf_url": pdf_url,
    }


@require_http_methods(["GET"])
def syllabus_list(request: HttpRequest):
    branch_code = (request.GET.get("branch") or "all").strip()
    qs = Syllabus.objects.select_related("branch")
    if branch_code and branch_code.lower() != "all":
        qs = qs.filter(branch__code=branch_code)
    syllabi = [_syllabus_to_dict(s) for s in qs.order_by("-id")[:500]]
    return JsonResponse({"syllabi": syllabi})


@require_http_methods(["POST"])
def upload_syllabus(request: HttpRequest):
    login_err = _require_login(request)
    if login_err:
        return login_err

    if getattr(request.user, "role", None) != "super_student":
        return HttpResponseForbidden("Only super students can upload")

    subject_name = (request.POST.get("subject_name") or "").strip()
    subject_code = (request.POST.get("subject_code") or "").strip()
    branch_code = (request.POST.get("branch") or "").strip()
    semester = _parse_int(request.POST.get("semester"), None)
    units_raw = (request.POST.get("units") or "[]").strip()
    pdf_link = (request.POST.get("pdf_link") or "").strip()

    if not subject_name or not subject_code or not branch_code or semester is None or not pdf_link:
        return _json_error("Missing required fields")

    import json

    try:
        units = json.loads(units_raw) if units_raw else []
    except Exception:
        units = []

    branch = Branch.objects.filter(code=branch_code).first()
    if not branch:
        return _json_error("Invalid branch")

    Syllabus.objects.create(
        subject_name=subject_name,
        subject_code=subject_code,
        branch=branch,
        semester=semester,
        units=units,
        pdf_link=pdf_link,
    )

    return JsonResponse({"ok": True})


# -----------------
# Doubts & Replies
# -----------------


def _doubt_to_dict(d: Doubt, *, replies_data: list[dict[str, Any]], current_username: str) -> dict[str, Any]:
    return {
        "id": d.id,
        "title": d.title,
        "description": d.description,
        "subject": d.subject,
        "branch": d.branch.code if d.branch_id else None,
        "semester": d.semester,
        "asked_by": getattr(d.asked_by, "username", ""),
        "asked_at": d.asked_at.isoformat() if hasattr(d.asked_at, "isoformat") else str(d.asked_at),
        "views": d.views,
        "is_solved": d.is_solved,
        "replies": replies_data,
    }


@require_http_methods(["GET"])
def doubts_list(request: HttpRequest):
    status = (request.GET.get("status") or "all").strip().lower()

    qs = Doubt.objects.select_related("branch", "asked_by").prefetch_related("replies")

    if status in {"open", "solved"}:
        qs = qs.filter(is_solved=(status == "solved"))

    # newest first
    doubts = qs.order_by("-asked_at")[:200]

    current_username = getattr(request.user, "username", "") if request.user.is_authenticated else ""

    output: list[dict[str, Any]] = []
    for d in doubts:
        replies_qs = Reply.objects.filter(doubt_id=d.id).order_by("is_best", "created_at")
        replies = []
        for r in replies_qs:
            replies.append(
                {
                    "id": r.id,
                    "by": getattr(r.user, "username", ""),
                    "answer": r.answer,
                    "is_best": r.is_best,
                }
            )

        output.append(_doubt_to_dict(d, replies_data=replies, current_username=current_username))

    return JsonResponse({"doubts": output})


@require_http_methods(["POST"])
def ask_doubt(request: HttpRequest):
    login_err = _require_login(request)
    if login_err:
        return login_err

    title = (request.POST.get("title") or "").strip()
    subject = (request.POST.get("subject") or "").strip()
    description = (request.POST.get("description") or "").strip()
    branch_code = (request.POST.get("branch") or "").strip()
    semester = _parse_int(request.POST.get("semester"), None)

    if not title or not subject or not description or not branch_code or semester is None:
        return _json_error("Missing required fields")

    branch = Branch.objects.filter(code=branch_code).first()
    if not branch:
        return _json_error("Invalid branch")

    Doubt.objects.create(
        title=title,
        description=description,
        subject=subject,
        branch=branch,
        semester=semester,
        asked_by=request.user,
    )

    return JsonResponse({"ok": True})


@require_http_methods(["POST"])
def reply_to_doubt(request: HttpRequest, doubt_id: int):
    login_err = _require_login(request)
    if login_err:
        return login_err

    answer = (request.POST.get("answer") or "").strip()
    if not answer:
        return _json_error("Answer required")

    doubt = Doubt.objects.filter(id=doubt_id).first()
    if not doubt:
        return _json_error("Doubt not found", status=404)

    Reply.objects.create(doubt=doubt, user=request.user, answer=answer)
    return JsonResponse({"ok": True})


@require_http_methods(["POST"])
def mark_best_reply(request: HttpRequest, reply_id: int):
    login_err = _require_login(request)
    if login_err:
        return login_err

    reply = Reply.objects.select_related("doubt", "user").filter(id=reply_id).first()
    if not reply:
        return _json_error("Reply not found", status=404)

    doubt = reply.doubt
    if doubt.asked_by_id != request.user.id and getattr(request.user, "role", None) != "super_student":
        return HttpResponseForbidden("Not permitted")

    # unset others
    Reply.objects.filter(doubt_id=doubt.id).update(is_best=False)
    reply.is_best = True
    reply.save(update_fields=["is_best"])

    # mark doubt solved if best reply exists
    Doubt.objects.filter(id=doubt.id).update(is_solved=True)

    return JsonResponse({"ok": True})


# -----------------
# Profile
# -----------------


def _user_to_profile_dict(u: User) -> dict[str, Any]:
    branch_code = u.branch.code if u.branch_id else None
    return {
        "id": u.id,
        "username": u.username,
        "name": u.get_full_name() or u.username,
        "role": getattr(u, "role", None),
        "college": getattr(u, "college", ""),
        "bio": getattr(u, "bio", ""),
        "avatar": getattr(u, "avatar", ""),
        "branch": branch_code,
        "semester": getattr(u, "semester", None),
    }


@require_http_methods(["GET"])
def profile_data(request: HttpRequest):
    login_err = _require_login(request)
    if login_err:
        return login_err
    return JsonResponse(_user_to_profile_dict(request.user))


@require_http_methods(["POST"])
def update_profile(request: HttpRequest):
    login_err = _require_login(request)
    if login_err:
        return login_err

    name = (request.POST.get("name") or "").strip()
    college = (request.POST.get("college") or "").strip()
    branch_code = (request.POST.get("branch") or "").strip()
    semester = _parse_int(request.POST.get("semester"), None)
    bio = (request.POST.get("bio") or "").strip()

    u: User = request.user
    if name:
        # map to full_name: set first_name blank, username unchanged
        # templates read `user.name` from API
        u.first_name = name
        u.save(update_fields=["first_name"])

    u.college = college
    u.bio = bio

    if branch_code:
        branch = Branch.objects.filter(code=branch_code).first()
        u.branch = branch

    if semester is not None:
        u.semester = semester

    u.save(update_fields=["college", "bio", "branch", "semester", "first_name"])
    return JsonResponse({"ok": True})


@require_http_methods(["GET"])
def my_uploads(request: HttpRequest):
    login_err = _require_login(request)
    if login_err:
        return login_err

    qs = Note.objects.filter(uploaded_by_id=request.user.id).select_related("branch", "uploaded_by").order_by("-uploaded_at", "-id")
    notes = [_note_to_dict(n, is_mine=True) for n in qs]
    return JsonResponse({"notes": notes})


@require_http_methods(["GET"])
def saved_notes(request: HttpRequest):
    login_err = _require_login(request)
    if login_err:
        return login_err

    bookmarks = Bookmark.objects.filter(user_id=request.user.id).select_related("note", "note__branch", "note__uploaded_by")
    notes: list[dict[str, Any]] = []
    for bm in bookmarks.order_by("-saved_at"):
        notes.append(_note_to_dict(bm.note, is_mine=(bm.note.uploaded_by_id == request.user.id)))

    return JsonResponse({"notes": notes})

