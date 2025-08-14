/* animations.js — simple intersection observer for scroll animations */
(function () {
  if (typeof window === "undefined") return;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.style.opacity = 1;
        e.target.style.transform = "translateY(0)";
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.card, .lottie, .fade-in').forEach(el => {
    el.style.opacity = 0;
    el.style.transform = "translateY(14px)";
    observer.observe(el);
  });
})();
