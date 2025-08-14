/* multilingual.js — toggles language cookie and dispatches reload to Streamlit */
function setClauseWiseLang(lang) {
  document.cookie = "cw_lang=" + lang + ";path=/;max-age=31536000";
  // Let Streamlit reload so server-side i18n picks it up
  location.reload();
}
