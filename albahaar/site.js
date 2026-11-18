/* Shared layout + behaviour for the Al-Bahaar site */
const CDN = "https://cdn.prod.website-files.com/660ee881750650ca2d4c4b7c/";
const SITE = {
  phone: "+1 (708) 653-0009",
  tel: "+17086530009",
  email: "info@albahaar.com",
  address: "39 Orland Square Dr, Orland Park, IL 60462",
  maps: "https://maps.app.goo.gl/CxqishMk19Qv5mo36",
  order: "https://albahaar.smartonlineorder.com/",
  instagram: "https://www.instagram.com/albahaarusa",
  tiktok: "https://www.tiktok.com/@al.bahaar",
  logo: CDN + "660eee78d19de12a44f60fed_AlBahaarTransp..png",
  hours: [
    ["Monday – Thursday", "12:00 PM – 9:00 PM"],
    ["Friday", "12:00 PM – 10:30 PM"],
    ["Saturday", "11:00 AM – 10:30 PM"],
    ["Sunday", "11:00 AM – 10:00 PM"],
  ],
};

const ICONS = {
  pin: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
  phone: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
  mail: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
  clock: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
  insta: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
  tiktok: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M16.6 5.8A4.3 4.3 0 0 1 15.5 3h-3.1v12.4a2.6 2.6 0 1 1-2.6-2.6c.3 0 .5 0 .8.1V9.7a5.7 5.7 0 1 0 4.9 5.7V9.1a7.3 7.3 0 0 0 4.3 1.4V7.4a4.3 4.3 0 0 1-3.2-1.6Z"/></svg>',
  menu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
};

const REVIEWS = [
  ["Al Bahaar is hands down one of the best restaurants I have ever eaten at. From start to finish, everything about our evening was exceptional. Each dish was not only beautifully presented but also bursting with flavor—fresh, vibrant, and cooked to absolute perfection.", "Patricia Nulis", "694c7e15848dd5e81b5970c3_Patrica.png"],
  ["Coming all the way from Indiana to try their food and we didn’t regret it! Totally worth the drive — the food, the atmosphere, and the vibes were amazingly good. I can’t talk enough about the friendly staff and the excellent service. Thank you 👌", "Wafa Trigui", "694c7c135e67595b054d14fc_Waffa.png"],
  ["Amazing food, fantastic service! We had a large group and they handled it gracefully! Tariq was so fun, gave us great insight on the menu. We will be back!!", "Kenzi Fischer", "694c7c6583ddfda845ad7e2c_Kenzi.png"],
  ["If you’re looking for authentic Mediterranean flavors, top-notch service, and a warm, welcoming atmosphere, Al Bahaar is a must-visit! My husband and I will definitely be back!", "Ashley Pride", "694c7d515263b89fb2cfe592_unnamed.png"],
  ["Everything was delicious! Service was top tier! And we were seated by the cozy fireplace. Can’t wait to go back!", "Abel Muhammed", "694c7d5408fc86fde9c138a7_Abel.png"],
];

function dishHTML(it) {
  const price = Number.isInteger(+it.p) ? it.p : (+it.p).toFixed(2);
  return `
  <div class="dish">
    <div class="dish-head"><h4>${it.n.toLowerCase()}</h4>${it.x ? `<span class="note">${it.x}</span>` : ""}<span class="dots"></span><span class="price">$${price}</span></div>
    <p>${it.d}</p>
  </div>`;
}

const page = document.body.dataset.page || "";
const navItem = (href, label, key) =>
  `<li><a href="${href}"${page === key ? ' aria-current="page"' : ""}>${label}</a></li>`;

function renderHeader() {
  const el = document.getElementById("site-header");
  if (!el) return;
  el.outerHTML = `
  <div class="announce">🌟 Every Weekend Buffet Special — All-you-can-eat for just $25, 12–3 PM 🍽️</div>
  <header class="site-header">
    <nav class="container nav" aria-label="Main">
      <a href="index.html" class="logo" aria-label="Al-Bahaar home"><img src="${SITE.logo}" alt="Al-Bahaar" width="140" height="52"></a>
      <button class="nav-toggle" aria-label="Open menu" aria-expanded="false">${ICONS.menu}</button>
      <ul class="nav-links">
        ${navItem("index.html", "Home", "home")}
        ${navItem("menu.html", "Menu", "menu")}
        ${navItem("about.html", "About", "about")}
        ${navItem("contact.html", "Contact", "contact")}
        <li><a class="btn btn-gold" href="${SITE.order}" target="_blank" rel="noopener">Order Online</a></li>
      </ul>
    </nav>
  </header>`;
  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  toggle.addEventListener("click", () => {
    const open = links.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open);
  });
}

function renderReviews() {
  document.querySelectorAll("[data-reviews]").forEach((el) => {
    el.innerHTML = REVIEWS.slice(0, 3).concat(el.dataset.reviews === "all" ? REVIEWS.slice(3) : [])
      .map(([q, name, img]) => `
      <article class="review reveal">
        <div class="stars" aria-label="5 stars">★★★★★</div>
        <blockquote>“${q}”</blockquote>
        <div class="who"><img src="${CDN + img}" alt="" loading="lazy"><div><b>${name}</b><span>Valued customer</span></div></div>
      </article>`).join("");
  });
}

function renderReserve() {
  document.querySelectorAll("[data-reserve]").forEach((el) => {
    el.innerHTML = `
    <div class="container">
      <div class="reserve reveal">
        <div class="media" role="img" aria-label="Al-Bahaar dining room"></div>
        <div class="body">
          <span class="eyebrow">Reserve Now</span>
          <h2>Secure Your Table of Indulgence</h2>
          <p class="lead">To reserve, call us and speak with our host or hostess — see you soon!</p>
          <ul class="info-list">
            <li>${ICONS.phone}<div><b>Booking</b><a href="tel:${SITE.tel}">${SITE.phone}</a></div></li>
            <li>${ICONS.pin}<div><b>Location</b><a href="${SITE.maps}" target="_blank" rel="noopener">${SITE.address}</a></div></li>
          </ul>
          <table class="hours-table">${SITE.hours.map(([d, h]) => `<tr><td>${d}</td><td>${h}</td></tr>`).join("")}</table>
          <div class="btn-row" style="margin-top:28px">
            <a class="btn btn-gold" href="tel:${SITE.tel}">Call to Reserve</a>
            <a class="btn btn-ghost" href="contact.html">Contact Us</a>
          </div>
        </div>
      </div>
    </div>`;
  });
}

function renderFooter() {
  const el = document.getElementById("site-footer");
  if (!el) return;
  el.outerHTML = `
  <footer class="site-footer">
    <div class="container footer-grid">
      <div>
        <img src="${SITE.logo}" alt="Al-Bahaar" style="height:60px;width:auto;margin-bottom:16px">
        <p><strong style="color:var(--cream)">A Taste of the Mediterranean, A Taste of Experience.</strong><br>
        At Al-Bahaar, we believe that dining is a form of art. From our family to yours, we welcome you to an unforgettable experience.</p>
        <div class="socials">
          <a href="${SITE.instagram}" target="_blank" rel="noopener" aria-label="Instagram">${ICONS.insta}</a>
          <a href="${SITE.tiktok}" target="_blank" rel="noopener" aria-label="TikTok">${ICONS.tiktok}</a>
        </div>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="menu.html">Menu</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="${SITE.order}" target="_blank" rel="noopener">Order Online</a></li>
        </ul>
      </div>
      <div>
        <h4>Visit</h4>
        <ul>
          <li><a href="${SITE.maps}" target="_blank" rel="noopener">${SITE.address}</a></li>
          <li><a href="tel:${SITE.tel}">${SITE.phone}</a></li>
          <li><a href="mailto:${SITE.email}">${SITE.email}</a></li>
        </ul>
      </div>
      <div>
        <h4>Hours</h4>
        <ul>${SITE.hours.map(([d, h]) => `<li>${d}<br><span style="color:var(--gold)">${h}</span></li>`).join("")}</ul>
      </div>
    </div>
    <div class="container footer-bottom">
      <span>© ${new Date().getFullYear()} Al-Bahaar. Made with ❤️ in Chicago.</span>
      <span><a href="privacy.html">Privacy Policy</a></span>
    </div>
  </footer>`;
}

function initReveal() {
  const els = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window)) { els.forEach((e) => e.classList.add("in")); return; }
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { threshold: 0.12 });
  els.forEach((e) => io.observe(e));
}

function initForms() {
  document.querySelectorAll("form.contact-form").forEach((form) => {
    form.addEventListener("submit", (ev) => {
      ev.preventDefault();
      const d = new FormData(form);
      const subject = encodeURIComponent(`${d.get("topic") || "Inquiry"} — ${d.get("name")}`);
      const body = encodeURIComponent(
        [...d.entries()].filter(([k]) => k !== "topic").map(([k, v]) => `${k[0].toUpperCase() + k.slice(1)}: ${v}`).join("\n")
      );
      window.location.href = `mailto:${SITE.email}?subject=${subject}&body=${body}`;
      const msg = form.querySelector(".form-msg");
      if (msg) msg.classList.add("show");
    });
  });
}

renderHeader();
renderReviews();
renderReserve();
renderFooter();
initReveal();
initForms();
