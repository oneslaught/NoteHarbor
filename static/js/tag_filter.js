function tagFilter(selected, tags) {
  return {
    open: false,
    search: "",
    selected: selected,
    tags: tags,
    get filtered() {
      return this.tags.filter(
        (t) =>
          t.name.toLowerCase().includes(this.search.toLowerCase()) &&
          !this.selected.find((s) => s.id === t.id),
      );
    },
    toggle(tag) {
      this.selected.push(tag);
      this.search = "";
      this.open = false;
      this.apply();
    },
    remove(tag) {
      this.selected = this.selected.filter((s) => s.id !== tag.id);
      this.apply();
    },
    apply() {
      const url = new URL(window.location.href);
      url.searchParams.delete("tag");
      this.selected.forEach((t) => url.searchParams.append("tag", t.id));
      window.location.href = url.toString();
    },
  };
}
