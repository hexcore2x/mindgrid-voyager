/*
const profiles = {
  explorer: {
    title: "Urban Explorer profile",
    summary:
      "Designed for travelers who want cultural density, easy movement, and local texture in the same day.",
    dayTone: "Walkable with flexible detours",
    optimalBudget: 170,
    destination: 92,
    local: 88,
    safety: 82,
    budgetBase: 94,
    budgetMessage:
      "The engine keeps core cultural stops and one atmospheric dinner while trimming low-signal transit hops.",
    sources: [
      "Neighborhood activity maps and seasonal crowd shifts",
      "Transit friction, queue timing, and walkability intelligence",
      "Review depth mixed with recency-weighted social chatter"
    ],
    itinerary: [
      {
        time: "08:15",
        title: "Breakfast in a design-forward local cafe cluster",
        text: "Starts where resident footfall is strong but tourist inflation is still low.",
        cost: 18
      },
      {
        time: "12:30",
        title: "Museum and old-quarter loop",
        text: "Scheduled into the quietest queue window with weather-friendly indoor coverage.",
        cost: 34
      },
      {
        time: "19:15",
        title: "Chef-driven dinner near a live music lane",
        text: "Pairs standout food quality with a short, comfortable evening route back.",
        cost: 46
      }
    ],
    favorites: [
      {
        title: "Stone Alley Coffee Room",
        text: "High repeat-local signal, known for morning calm and neighborhood regulars."
      },
      {
        title: "Riverside Book Arcade",
        text: "Low-friction cultural stop with strong dwell time and excellent midday energy."
      },
      {
        title: "Market Hall Listening Bar",
        text: "Late-evening social pick chosen for atmosphere quality over trend noise."
      }
    ],
    alerts: [
      {
        title: "Route advisory",
        text: "Use the riverside path before 21:00 for the best lighting and lowest congestion."
      },
      {
        title: "Timing adjustment",
        text: "Shift museum entry by 20 minutes if rain starts early to preserve queue advantage."
      },
      {
        title: "Transit fallback",
        text: "Micro-mobility lane is faster than metro for the afternoon segment today."
      }
    ],
    journalTitle: "The city unfolded in layers.",
    journalLead:
      "This profile leans into curiosity, rhythm, and the feeling of moving through a place at exactly the right pace.",
    journalSnippet:
      "By noon, the route no longer felt like a plan I was following. It felt like the city was quietly opening one good decision after another, each one verified by the energy of the streets around me.",
    tags: ["culture-dense", "walkable", "adaptive route", "high local texture"],
    journalMood: "Curated for a curiosity-led traveler"
  },
  budget: {
    title: "Budget Hunter profile",
    summary:
      "Built for maximum experience density at a controlled daily cost, without defaulting to the cheapest options.",
    dayTone: "Lean spend, high value, low friction",
    optimalBudget: 120,
    destination: 84,
    local: 81,
    safety: 79,
    budgetBase: 98,
    budgetMessage:
      "The engine protects your daily cap by prioritizing transit efficiency, bundled activity zones, and high-value food windows.",
    sources: [
      "Price elasticity across meal periods and neighborhood zones",
      "Transit cost comparison against walking and ride-share friction",
      "Value-per-hour scoring for attractions and community spaces"
    ],
    itinerary: [
      {
        time: "08:00",
        title: "Breakfast corridor with local pastry and coffee pair",
        text: "Selected for strong quality-to-cost ratio and proximity to the first activity cluster.",
        cost: 9
      },
      {
        time: "13:00",
        title: "Free gallery circuit with market lunch",
        text: "Combines high cultural yield with low transit drag and flexible timing.",
        cost: 18
      },
      {
        time: "18:45",
        title: "Sunset viewpoint and neighborhood dinner",
        text: "Balances a signature city moment with a local meal that stays under target.",
        cost: 24
      }
    ],
    favorites: [
      {
        title: "Corner Oven Collective",
        text: "Resident-loved, generous portions, and consistently above-value breakfast scores."
      },
      {
        title: "Canal Market Hall",
        text: "Best midday flexibility for sampling multiple stalls without overspending."
      },
      {
        title: "Garden Terrace Viewpoint",
        text: "Zero-ticket scenic win that offsets paid attraction pressure."
      }
    ],
    alerts: [
      {
        title: "Spend control",
        text: "Avoid dining in the central monument ring after 19:30 due to surge pricing."
      },
      {
        title: "Mobility note",
        text: "Two walkable clusters reduce transport cost more than an all-day transit pass."
      },
      {
        title: "Queue strategy",
        text: "Go to the market before 12:15 to avoid buying from higher-priced fast lines."
      }
    ],
    journalTitle: "A city that rewarded restraint with surprise.",
    journalLead:
      "The strongest moments came from smart tradeoffs, not from chasing expensive highlights.",
    journalSnippet:
      "The trip felt light, almost tactical, but never deprived. Every saved ride or skipped hype stop seemed to create room for something more memorable and more local.",
    tags: ["value-first", "high efficiency", "market finds", "smart tradeoffs"],
    journalMood: "Curated for a cost-aware explorer"
  },
  foodie: {
    title: "Food Scout profile",
    summary:
      "Tailored for travelers who want the city's character to be discovered through kitchens, cafes, and neighborhood rituals.",
    dayTone: "Flavor-led with social energy",
    optimalBudget: 210,
    destination: 89,
    local: 95,
    safety: 80,
    budgetBase: 88,
    budgetMessage:
      "The engine allows one premium meal anchor and surrounds it with local-value cafe and snack discoveries.",
    sources: [
      "Recency-weighted dish reviews and venue consistency markers",
      "Chef credibility, repeat mentions, and neighborhood loyalty patterns",
      "Social media buzz filtered through authenticity and overhype checks"
    ],
    itinerary: [
      {
        time: "08:30",
        title: "Specialty coffee and bakery opening run",
        text: "Timed for peak pastry quality and lower wait, with strong resident repeat behavior.",
        cost: 22
      },
      {
        time: "13:15",
        title: "Market tasting route across three signature counters",
        text: "A multi-stop midday block designed to sample variety without duplicating cuisines.",
        cost: 36
      },
      {
        time: "20:00",
        title: "Flagship dinner with night dessert walk",
        text: "Selected for depth of praise, chef signal, and a strong after-dinner district flow.",
        cost: 72
      }
    ],
    favorites: [
      {
        title: "Roast & Rind Atelier",
        text: "Small-batch breakfast favorite with unusually high return-customer language."
      },
      {
        title: "Lantern Market Kitchen Row",
        text: "Best zone for comparative tasting across local specialties in one walkable loop."
      },
      {
        title: "Velvet Cup Night Cafe",
        text: "High social warmth and late-evening dessert energy without tourist fatigue."
      }
    ],
    alerts: [
      {
        title: "Reservation risk",
        text: "Book the flagship dinner before 16:00 or the engine will downgrade to a secondary option."
      },
      {
        title: "Crowd pattern",
        text: "The market is most photogenic after 14:00 but best for sampling before 13:30."
      },
      {
        title: "Movement note",
        text: "Take the tram uphill and walk back down to preserve appetite and route comfort."
      }
    ],
    journalTitle: "I learned the city through what it fed me.",
    journalLead:
      "This profile treats food as both navigation system and emotional memory layer.",
    journalSnippet:
      "The places I remember most were not the loudest. They were the ones where the room went still for a second after the first bite, as if the city had explained itself in flavor.",
    tags: ["food-led", "chef signal", "cafe rituals", "night dessert route"],
    journalMood: "Curated for a flavor-seeking traveler"
  },
  secure: {
    title: "Safety First profile",
    summary:
      "Optimized for confidence, comfort, and clarity, with steady routes and lower situational uncertainty.",
    dayTone: "Predictable movement with strong safeguards",
    optimalBudget: 180,
    destination: 86,
    local: 77,
    safety: 96,
    budgetBase: 90,
    budgetMessage:
      "The engine preserves trusted routes, daylight-heavy movement, and highly consistent venues while keeping spend reasonable.",
    sources: [
      "Route lighting, crowd density, and neighborhood timing intelligence",
      "Weather exposure and fallback transport reliability",
      "Venue consistency, support access, and low-friction return paths"
    ],
    itinerary: [
      {
        time: "08:45",
        title: "Morning cafe near a major transit node",
        text: "Easy orientation, dependable quality, and simple onward movement for the day.",
        cost: 16
      },
      {
        time: "12:00",
        title: "High-confidence attraction cluster",
        text: "Keeps transitions short and avoids isolated movement during low-activity windows.",
        cost: 28
      },
      {
        time: "18:15",
        title: "Early dinner with direct return route",
        text: "Ends the day before heavy crowd spikes while preserving a strong local experience.",
        cost: 38
      }
    ],
    favorites: [
      {
        title: "Station Garden Cafe",
        text: "Reliable service, good visibility, and consistent positive mentions from solo travelers."
      },
      {
        title: "Civic Square Museum Ring",
        text: "Dense cluster of trusted venues with low route ambiguity."
      },
      {
        title: "Oak Street Supper House",
        text: "Highly rated for calm atmosphere, early dining, and easy return logistics."
      }
    ],
    alerts: [
      {
        title: "Route advisory",
        text: "Avoid the river underpass after dusk and stay on the main boulevard return route."
      },
      {
        title: "Weather fallback",
        text: "Heavy rain window may begin at 17:40, so indoor activity options are front-loaded."
      },
      {
        title: "Support note",
        text: "All recommended stops keep you within short access to staffed transit and clear signage."
      }
    ],
    journalTitle: "The city felt clear, calm, and open to me.",
    journalLead:
      "Confidence shaped the experience, and that confidence created more room for presence and enjoyment.",
    journalSnippet:
      "Nothing dramatic happened, and that was the quiet luxury of the day. Every turn felt legible, every return felt easy, and the city met me without tension.",
    tags: ["confidence-led", "predictable routes", "trusted venues", "low ambiguity"],
    journalMood: "Curated for a confidence-first traveler"
  }
};

const state = {
  profile: "explorer",
  budget: 160
};

const profileButtons = [...document.querySelectorAll("[data-profile]")];
const budgetRange = document.getElementById("budgetRange");
const budgetValue = document.getElementById("budgetValue");
const profileTitle = document.getElementById("profileTitle");
const profileSummary = document.getElementById("profileSummary");
const budgetInsight = document.getElementById("budgetInsight");
const sourceList = document.getElementById("sourceList");
const itineraryList = document.getElementById("itineraryList");
const favoritesList = document.getElementById("favoritesList");
const alertsList = document.getElementById("alertsList");
const dayTone = document.getElementById("dayTone");
const journalTitle = document.getElementById("journalTitle");
const journalLead = document.getElementById("journalLead");
const journalSnippet = document.getElementById("journalSnippet");
const journalTags = document.getElementById("journalTags");
const journalMood = document.getElementById("journalMood");
const year = document.getElementById("year");
const apiStatus = document.getElementById("apiStatus");
const demoForm = document.getElementById("demoForm");
const formStatus = document.getElementById("formStatus");
const submitButton = document.getElementById("submitButton");

const scoreDestination = document.getElementById("scoreDestination");
const scoreBudget = document.getElementById("scoreBudget");
const scoreLocal = document.getElementById("scoreLocal");
const scoreSafety = document.getElementById("scoreSafety");
const meterDestination = document.getElementById("meterDestination");
const meterBudget = document.getElementById("meterBudget");
const meterLocal = document.getElementById("meterLocal");
const meterSafety = document.getElementById("meterSafety");

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function computeBudgetFit(profile, budget) {
  const distance = Math.abs(budget - profile.optimalBudget);
  return clamp(profile.budgetBase - Math.round(distance * 0.22), 61, 99);
}

function formatCurrency(value) {
  return `$${value}`;
}

function buildBudgetMessage(profile, budget) {
  const delta = budget - profile.optimalBudget;
  let adjustment = "";

  if (delta >= 30) {
    adjustment = " With extra room in the budget, the engine unlocks a more premium signature moment.";
  } else if (delta <= -30) {
    adjustment = " Because the budget is tighter, the engine protects the strongest signals and trims weaker extras.";
  } else {
    adjustment = " The current budget stays close to the profile's ideal balance of value and experience.";
  }

  return `${profile.budgetMessage}${adjustment}`;
}

function scaledCost(baseCost, budget) {
  const multiplier = clamp(0.82 + (budget - 70) / 300, 0.72, 1.28);
  return Math.round(baseCost * multiplier);
}

function renderList(target, items) {
  target.innerHTML = "";

  items.forEach((item) => {
    const li = document.createElement("li");
    const title = document.createElement("strong");
    const text = document.createElement("span");

    title.textContent = item.title;
    text.textContent = item.text;

    li.append(title, text);
    target.appendChild(li);
  });
}

function renderSources(items) {
  sourceList.innerHTML = "";
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    sourceList.appendChild(li);
  });
}

function renderItinerary(items, budget) {
  itineraryList.innerHTML = "";

  items.forEach((item) => {
    const row = document.createElement("article");
    row.className = "timeline-item";

    const time = document.createElement("div");
    time.className = "timeline-time";
    time.textContent = item.time;

    const copy = document.createElement("div");
    copy.className = "timeline-copy";
    const heading = document.createElement("h4");
    heading.textContent = item.title;
    const paragraph = document.createElement("p");
    paragraph.textContent = item.text;
    copy.append(heading, paragraph);

    const price = document.createElement("div");
    price.className = "timeline-price";
    price.textContent = formatCurrency(scaledCost(item.cost, budget));

    row.append(time, copy, price);
    itineraryList.appendChild(row);
  });
}

function renderTags(tags) {
  journalTags.innerHTML = "";
  tags.forEach((tag) => {
    const chip = document.createElement("span");
    chip.textContent = tag;
    journalTags.appendChild(chip);
  });
}

function setScore(target, meter, value) {
  target.textContent = `${value}%`;
  meter.style.width = `${value}%`;
}

function setApiStatus(message, type) {
  apiStatus.textContent = message;
  apiStatus.classList.remove("is-online", "is-offline");

  if (type) {
    apiStatus.classList.add(type);
  }
}

function renderProfile() {
  const profile = profiles[state.profile];
  const budgetFit = computeBudgetFit(profile, state.budget);

  budgetValue.textContent = formatCurrency(state.budget);
  profileTitle.textContent = profile.title;
  profileSummary.textContent = profile.summary;
  budgetInsight.textContent = buildBudgetMessage(profile, state.budget);
  dayTone.textContent = profile.dayTone;

  setScore(scoreDestination, meterDestination, profile.destination);
  setScore(scoreBudget, meterBudget, budgetFit);
  setScore(scoreLocal, meterLocal, profile.local);
  setScore(scoreSafety, meterSafety, profile.safety);

  renderSources(profile.sources);
  renderItinerary(profile.itinerary, state.budget);
  renderList(favoritesList, profile.favorites);
  renderList(alertsList, profile.alerts);

  journalTitle.textContent = profile.journalTitle;
  journalLead.textContent = profile.journalLead;
  journalSnippet.textContent = profile.journalSnippet;
  renderTags(profile.tags);
  journalMood.textContent = profile.journalMood;

  profileButtons.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.profile === state.profile);
  });
}

profileButtons.forEach((button) => {
  button.addEventListener("click", () => {
    state.profile = button.dataset.profile;
    renderProfile();
  });
});

budgetRange.addEventListener("input", (event) => {
  state.budget = Number(event.target.value);
  renderProfile();
});

async function checkBackendHealth() {
  if (window.location.protocol === "file:") {
    setApiStatus("Static preview mode. Run python app.py for live API and form support.", "is-offline");
    return;
  }

  try {
    const response = await fetch("/health", {
      headers: {
        Accept: "application/json"
      }
    });

    if (!response.ok) {
      throw new Error("Health endpoint unavailable");
    }

    const payload = await response.json();
    setApiStatus(`Backend live: ${payload.service} ready`, "is-online");
  } catch (error) {
    setApiStatus("Backend offline. Start python app.py to enable live submissions.", "is-offline");
  }
}

async function handleFormSubmit(event) {
  event.preventDefault();

  if (window.location.protocol === "file:") {
    formStatus.textContent = "Start the Python server first so the form can submit to the local API.";
    return;
  }

  const formData = new FormData(demoForm);
  const payload = {
    name: String(formData.get("name") || "").trim(),
    email: String(formData.get("email") || "").trim(),
    destination: String(formData.get("destination") || "").trim(),
    travelStyle: String(formData.get("travelStyle") || "").trim(),
    notes: String(formData.get("notes") || "").trim()
  };

  submitButton.disabled = true;
  submitButton.textContent = "Submitting...";
  formStatus.textContent = "Sending your request to the local MindGrid Voyager API...";

  try {
    const response = await fetch("/api/demo-request", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json"
      },
      body: JSON.stringify(payload)
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || "Unable to submit the request.");
    }

    demoForm.reset();
    formStatus.textContent = `Request saved successfully with id ${result.requestId}.`;
    setApiStatus("Backend live: request pipeline active", "is-online");
  } catch (error) {
    formStatus.textContent = error.message || "Something went wrong while submitting the form.";
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Submit Demo Request";
  }
}

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  },
  {
    threshold: 0.14
  }
);

document.querySelectorAll(".reveal").forEach((element) => observer.observe(element));

year.textContent = new Date().getFullYear();
renderProfile();
checkBackendHealth();
demoForm.addEventListener("submit", handleFormSubmit);
*/

// Safe bootstrap: keep the original file path working while loading the upgraded client.
const existingClientApp = document.querySelector('script[data-client-app="true"], script[src$="client_app.js"]');
if (!existingClientApp) {
  const bootstrap = document.createElement("script");
  bootstrap.src = "client_app.js";
  bootstrap.defer = true;
  bootstrap.dataset.clientApp = "true";
  document.body.appendChild(bootstrap);
}
