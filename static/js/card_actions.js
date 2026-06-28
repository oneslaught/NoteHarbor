async function toggleNoteFavorite(btn, pk, csrfToken) {
  const response = await fetch(
    `/${document.documentElement.lang}/notes/${pk}/favorite/`,
    {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "X-Requested-With": "XMLHttpRequest",
      },
    },
  );
  const data = await response.json();
  if (data.is_saved) {
    btn.classList.remove("primary");
    btn.classList.add("remove");
    btn.textContent = btn.dataset.removeText;
  } else {
    btn.classList.remove("remove");
    btn.classList.add("primary");
    btn.textContent = btn.dataset.saveText;
  }
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
