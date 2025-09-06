// app.js
const s = document.createElement("script");
s.src = chrome.runtime.getURL("injected.js");
(document.head || document.documentElement).appendChild(s);
s.onload = () => s.remove();
