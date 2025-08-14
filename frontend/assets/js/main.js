/* main.js — small DOM helpers used via streamlit.components.v1.html injection */
/* NOTE: Streamlit isolates DOM; use carefully via components.html */

window.clausewise = {
  // animate element fade-in
  fadeIn: function (selector, delay = 0) {
    const el = document.querySelector(selector);
    if (!el) return;
    el.style.opacity = 0;
    el.style.transition = "opacity 600ms ease, transform 600ms ease";
    setTimeout(() => {
      el.style.opacity = 1;
      el.style.transform = "translateY(0)";
    }, delay);
  },

  // toggle language cookie (simple)
  setLang: function(lang) {
    document.cookie = "cw_lang=" + lang + ";path=/;max-age=31536000";
    // Optionally trigger a reload to let Streamlit re-read cookies
    location.reload();
  }
}
