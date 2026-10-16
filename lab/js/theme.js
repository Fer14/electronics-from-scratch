(function () {
  var button = document.getElementById("theme-toggle");
  if (!button) return;
  function label() { button.textContent = document.documentElement.dataset.theme === "dark" ? "light" : "dark"; }
  label();
  button.addEventListener("click", function () {
    var next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem("efs-lab:theme", next); } catch (e) {}
    label();
  });
})();
