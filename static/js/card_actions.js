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
    btn.classList.add("saved");
    if (btn.dataset.removeText) {
      btn.classList.remove("primary");
      btn.textContent = btn.dataset.removeText;
    }
  } else {
    btn.classList.remove("saved");
    if (btn.dataset.saveText) {
      btn.classList.add("primary");
      btn.textContent = btn.dataset.saveText;
    }
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

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".favorite-btn").forEach((btn) => {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      const pk = this.dataset.pk;
      const csrf = this.dataset.csrf;
      toggleNoteFavorite(this, pk, csrf);
    });
  });

  document.querySelectorAll(".delete-btn").forEach((btn) => {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      const pk = this.dataset.pk;
      const csrf = this.dataset.csrf;
      deleteNote(this, pk, csrf);
    });
  });
});
