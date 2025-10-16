import puppeteer from "puppeteer";

const SESSION_ID = "4007b723c55c6dd3afa6276dea11445";

const browser = await puppeteer.launch({ headless: false });
const page = await browser.newPage();
await page.setCookie({
  name: "POESESSID",
  value: SESSION_ID,
  domain: ".udemy.com",
  path: "/",
  httpOnly: true,
  secure: true,
});

await page.goto("https://www.udemy.com");

// (async () => {
//   try {
//     // Load URLs from file
//     if (!fs.existsSync(URLS_FILE)) {
//       console.error(`❌ Missing ${URLS_FILE}. Please create it with an array of URLs.`);
//       process.exit(1);
//     }

//     const urls = JSON.parse(fs.readFileSync(URLS_FILE, "utf-8"));
//     if (!Array.isArray(urls) || urls.length === 0) {
//       console.error("❌ urls.json must contain a non-empty array of URLs.");
//       process.exit(1);
//     }

//     console.log(`🚀 Launching browser with session: ${SESSION_ID}`);

//     const browser = await puppeteer.launch({
//       headless: false, // headful mode
//       defaultViewport: null,
//       args: [
//         `--user-data-dir=./puppeteer_profile_${SESSION_ID}`, // persist session
//         "--disable-background-timer-throttling",
//         "--disable-features=IntensiveWakeUpThrottling",
//         "--disable-renderer-backgrounding",
//         "--disable-backgrounding-occluded-windows",
//       ],
//     });

//     // Open each URL in a new tab with a 1s delay
//     for (const [i, url] of urls.entries()) {
//       const page = await browser.newPage();
//       await page.goto(url, { waitUntil: "domcontentloaded" });
//       console.log(`✅ Opened Tab ${i + 1}: ${url}`);
//       await sleep(1000); // wait 1 second before next tab
//     }

//     console.log("🌐 All tabs loaded. Browser is running...");

//     // Keep browser alive until manual exit
//     process.on("SIGINT", async () => {
//       console.log("\n👋 Closing browser...");
//       await browser.close();
//       process.exit(0);
//     });

//   } catch (err) {
//     console.error("🔥 Error:", err);
//     process.exit(1);
//   }
// })();
