async function toggleFavorite(btn, pk, csrfToken) {
    event.preventDefault();
    event.stopPropagation();
    const response = await fetch(`/${document.documentElement.lang}/notes/${pk}/favorite/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
        }
    });
    const data = await response.json();
    btn.classList.add('pop');
    setTimeout(() => {
        btn.classList.remove('pop');
        window.location.reload();
    }, 300);
}

async function deleteNote(btn, pk, csrfToken) {
  event.preventDefault();
  event.stopPropagation();
  const response = await fetch(
    `/${document.documentElement.lang}/notes/${pk}/delete/`,
    {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "X-Requested-With": "XMLHttpRequest",
      },
    },
  );
  const data = await response.json();
  if (data.deleted) {
    const card = btn.closest(".note-card");
    card.style.transition = "opacity 0.3s, transform 0.3s";
    card.style.opacity = "0";
    card.style.transform = "scale(0.95)";
    setTimeout(() => card.remove(), 300);
  }
}
