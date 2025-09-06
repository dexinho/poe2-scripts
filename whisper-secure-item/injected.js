// injected.js
(function () {
  console.log("PoE Trade Auto-Whisper (XHR Hook)");
  localStorage.poe_trade_run_script = "true";

  const whisperCooldown = 10;
  const travelToHideoutCooldown = 1000;
  const whisperLimits = {
    perMinute: 15,
    per10Minutes: 75,
    perHour: 150,
    per12Hours: 600,
  };

  function getWhisperLog() {
    try {
      const log = JSON.parse(
        localStorage.getItem("poe_trade_whisper_log") || "[]"
      );
      const now = Date.now();
      return log.filter((ts) => now - ts < 12 * 60 * 60 * 1000);
    } catch (e) {
      return [];
    }
  }

  function canWhisper(log) {
    const now = Date.now();
    const countLastMinute = log.filter((ts) => now - ts < 60 * 1000).length;
    const countLast10Min = log.filter((ts) => now - ts < 10 * 60 * 1000).length;
    const countLastHour = log.filter((ts) => now - ts < 60 * 60 * 1000).length;
    const countLast12Hours = log.length;

    return (
      countLastMinute < whisperLimits.perMinute &&
      countLast10Min < whisperLimits.per10Minutes &&
      countLastHour < whisperLimits.perHour &&
      countLast12Hours < whisperLimits.per12Hours
    );
  }

  function logWhisperTime(log) {
    log.push(Date.now());
    localStorage.setItem("poe_trade_whisper_log", JSON.stringify(log));
  }

  function getLastWhisperTime() {
    return parseInt(
      localStorage.getItem("poe_trade_last_whisper_click") || "0",
      10
    );
  }
  function updateLastWhisperTime() {
    localStorage.setItem("poe_trade_last_whisper_click", Date.now().toString());
  }

  function getLastTravelTime() {
    return parseInt(
      localStorage.getItem("poe_trade_last_travel_click") || "0",
      10
    );
  }
  function updateLastTravelTime() {
    localStorage.setItem("poe_trade_last_travel_click", Date.now().toString());
  }

  function normalizeText(s) {
    return (s || "").replace(/\s+/g, " ").trim().toLowerCase();
  }

  function handleButtons() {
    const log = getWhisperLog();
    if (!canWhisper(log)) return;

    const toRunScript = localStorage.poe_trade_run_script === "true";
    const toCopyWhisper = localStorage.poe_trade_copy_whisper === "true";

    // If live search not active, bail
    const plusSpan = document.querySelector("span.plus");
    if (plusSpan) {
      const textSpan = plusSpan.nextElementSibling;
      if (
        textSpan &&
        normalizeText(textSpan.textContent) === "activate live search"
      )
        return;
    }

    const now = Date.now();
    const lastWhisperTime = getLastWhisperTime();
    const lastTravelTime = getLastTravelTime();

    const btns = document.querySelectorAll("button.direct-btn");
    for (const btn of btns) {
      if (!(btn instanceof HTMLElement)) continue;

      const label = normalizeText(btn.innerText || btn.textContent);
      const isTravelToHideout = label.includes("travel to hideout");

      if (isTravelToHideout && now - lastTravelTime < travelToHideoutCooldown)
        continue;
      if (!isTravelToHideout && now - lastWhisperTime < whisperCooldown)
        continue;

      // --- Copy Whisper flow ---
      if (toCopyWhisper && !isTravelToHideout) {
        const copyWhisperButton = document.querySelector(
          "button.dropdown-item.btn.btn-xs.btn-default.whisper-btn"
        );
        if (copyWhisperButton) {
          copyWhisperButton.click();
          updateLastWhisperTime();
          logWhisperTime(log);
          console.log("[ext] Clicked copy whisper:", copyWhisperButton);
          return;
        }
      }

      if (!toRunScript) continue;

      // --- Direct Whisper / Travel ---
      btn.click();

      if (isTravelToHideout) {
        updateLastTravelTime();
        logWhisperTime(log);
        console.log("[ext] Clicked 'Travel to Hideout'");
      } else {
        updateLastWhisperTime();
        btn.parentElement?.remove();
        logWhisperTime(log);
        console.log("[ext] Clicked 'Direct Whisper'");
      }

      // --- Expired button handler ---
      setTimeout(() => {
        const expiredBtn = document.querySelector(
          "button.btn.btn-xs.btn-default.direct-btn.expired"
        );
        if (expiredBtn) {
          expiredBtn.click();
          expiredBtn.parentElement?.();
          console.log("[ext] Clicked 'Expired – Teleport anyway?'");
        }
      }, 1000);

      return; // stop after first valid click
    }
  }

  const origOpen = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (...args) {
    this.addEventListener("load", function () {
      if (this.responseURL.includes("/api/trade2/fetch/")) {
        console.log("[ext] Trade fetch detected:", this.responseURL);
        handleButtons();
      }
    });
    return origOpen.apply(this, args);
  };
})();
