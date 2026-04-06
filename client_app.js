const apiStatus = document.getElementById("apiStatus");
const recommendationForm = document.getElementById("recommendationForm");
const recommendationButton = document.getElementById("recommendationButton");
const recommendationStatus = document.getElementById("recommendationStatus");
const destinationInput = document.getElementById("destinationInput");
const quickChips = [...document.querySelectorAll(".quick-chip")];
const resultsShell = document.getElementById("resultsShell");
const heroPromptForm = document.getElementById("heroPromptForm");
const heroPromptButton = document.getElementById("heroPromptButton");
const heroPromptStatus = document.getElementById("heroPromptStatus");
const heroPromptDestination = document.getElementById("heroPromptDestination");
const heroPromptInterests = document.getElementById("heroPromptInterests");
const heroPromptBudget = document.getElementById("heroPromptBudget");
const heroPromptCurrency = document.getElementById("heroPromptCurrency");
const heroPromptDuration = document.getElementById("heroPromptDuration");
const heroPromptTravelStyle = document.getElementById("heroPromptTravelStyle");
const heroPromptPace = document.getElementById("heroPromptPace");
const heroSuggestions = [...document.querySelectorAll(".hero-suggestion")];

const resultsEmpty = document.getElementById("resultsEmpty");
const resultsLoading = document.getElementById("resultsLoading");
const resultsError = document.getElementById("resultsError");
const resultsErrorMessage = document.getElementById("resultsErrorMessage");
const resultsSuccess = document.getElementById("resultsSuccess");

const summaryTopDestination = document.getElementById("summaryTopDestination");
const summaryTopPriority = document.getElementById("summaryTopPriority");
const summaryWhyFirst = document.getElementById("summaryWhyFirst");
const summaryTotalAnalyzed = document.getElementById("summaryTotalAnalyzed");
const summaryAverageScore = document.getElementById("summaryAverageScore");
const summaryAverageConfidence = document.getElementById("summaryAverageConfidence");
const summaryTripStyle = document.getElementById("summaryTripStyle");
const resultDestinationName = document.getElementById("resultDestinationName");
const resultHeadline = document.getElementById("resultHeadline");
const resultOverview = document.getElementById("resultOverview");
const resultWhyWorks = document.getElementById("resultWhyWorks");
const resultTravelFit = document.getElementById("resultTravelFit");
const resultBestTime = document.getElementById("resultBestTime");
const decisionPriority = document.getElementById("decisionPriority");
const decisionExplanation = document.getElementById("decisionExplanation");
const decisionScoreValue = document.getElementById("decisionScoreValue");
const decisionConfidence = document.getElementById("decisionConfidence");
const decisionRiskLevel = document.getElementById("decisionRiskLevel");
const decisionHistoryState = document.getElementById("decisionHistoryState");
const scoreDestination = document.getElementById("scoreDestination");
const scoreBudget = document.getElementById("scoreBudget");
const scoreLocal = document.getElementById("scoreLocal");
const scoreSafety = document.getElementById("scoreSafety");
const scoreTripStyle = document.getElementById("scoreTripStyle");
const workflowSteps = document.getElementById("workflowSteps");
const workflowTitle = document.querySelector(".workflow-shell .card-head h4");
const evidenceSignals = document.getElementById("evidenceSignals");
const reasonSignals = document.getElementById("reasonSignals");
const sourcesUsed = document.getElementById("sourcesUsed");
const itineraryHintsList = document.getElementById("itineraryHintsList");
const groundingEvidenceList = document.getElementById("groundingEvidenceList");
const modelFeatureList = document.getElementById("modelFeatureList");
const verificationStatus = document.getElementById("verificationStatus");
const verificationTrustScore = document.getElementById("verificationTrustScore");
const verificationFreshness = document.getElementById("verificationFreshness");
const verificationSummary = document.getElementById("verificationSummary");
const verificationCitations = document.getElementById("verificationCitations");
const verificationLedger = document.getElementById("verificationLedger");
const traceIdValue = document.getElementById("traceIdValue");
const debugDecisionEngineVersion = document.getElementById("debugDecisionEngineVersion");
const debugResponseMode = document.getElementById("debugResponseMode");
const debugRecognized = document.getElementById("debugRecognized");
const attractionsList = document.getElementById("attractionsList");
const foodList = document.getElementById("foodList");
const favoritesList = document.getElementById("favoritesList");
const itineraryList = document.getElementById("itineraryList");
const budgetCard = document.getElementById("budgetCard");
const safetyCard = document.getElementById("safetyCard");
const tipsList = document.getElementById("tipsList");
const aiMissionTitle = document.getElementById("aiMissionTitle");
const aiMissionSummary = document.getElementById("aiMissionSummary");
const aiMissionOperatorNote = document.getElementById("aiMissionOperatorNote");
const aiFocusStage = document.getElementById("aiFocusStage");
const aiBestMoment = document.getElementById("aiBestMoment");
const aiGenerationMode = document.getElementById("aiGenerationMode");
const agentNextActions = document.getElementById("agentNextActions");
const agentVerificationChecklist = document.getElementById("agentVerificationChecklist");
const aiJournalTitle = document.getElementById("aiJournalTitle");
const aiJournalPreview = document.getElementById("aiJournalPreview");
const aiShareableSummary = document.getElementById("aiShareableSummary");
const agentReplanTriggers = document.getElementById("agentReplanTriggers");
const agentFollowUpQuestions = document.getElementById("agentFollowUpQuestions");
const aiMemoryMoments = document.getElementById("aiMemoryMoments");
const aiModelProvider = document.getElementById("aiModelProvider");
const aiModelMode = document.getElementById("aiModelMode");
const aiModelSummary = document.getElementById("aiModelSummary");
const replanForm = document.getElementById("replanForm");
const replanButton = document.getElementById("replanButton");
const replanStatus = document.getElementById("replanStatus");
const replanInstructionInput = document.getElementById("replanInstructionInput");
const replanChips = [...document.querySelectorAll(".replan-chip")];
const feedbackForm = document.getElementById("feedbackForm");
const feedbackButton = document.getElementById("feedbackButton");
const feedbackStatus = document.getElementById("feedbackStatus");
const feedbackRatingInput = document.getElementById("feedbackRatingInput");
const feedbackNotesInput = document.getElementById("feedbackNotesInput");
const feedbackVerdictInput = document.getElementById("feedbackVerdictInput");
const feedbackChips = [...document.querySelectorAll(".feedback-chip")];

const demoForm = document.getElementById("demoForm");
const demoSubmitButton = document.getElementById("demoSubmitButton");
const demoFormStatus = document.getElementById("demoFormStatus");
const demoCount = document.getElementById("demoCount");
const recommendationCount = document.getElementById("recommendationCount");

const comparisonForm = document.getElementById("comparisonForm");
const comparisonButton = document.getElementById("comparisonButton");
const comparisonStatus = document.getElementById("comparisonStatus");
const comparisonDestinationsInput = document.getElementById("comparisonDestinationsInput");
const compareChips = [...document.querySelectorAll(".compare-chip")];
const comparisonShell = document.getElementById("comparisonShell");
const comparisonEmpty = document.getElementById("comparisonEmpty");
const comparisonLoading = document.getElementById("comparisonLoading");
const comparisonError = document.getElementById("comparisonError");
const comparisonErrorMessage = document.getElementById("comparisonErrorMessage");
const comparisonSuccess = document.getElementById("comparisonSuccess");
const comparisonTopDestination = document.getElementById("comparisonTopDestination");
const comparisonTopPriority = document.getElementById("comparisonTopPriority");
const comparisonTopReason = document.getElementById("comparisonTopReason");
const comparisonComparedCount = document.getElementById("comparisonComparedCount");
const comparisonAverageScore = document.getElementById("comparisonAverageScore");
const comparisonAverageConfidence = document.getElementById("comparisonAverageConfidence");
const comparisonTopBestFor = document.getElementById("comparisonTopBestFor");
const comparisonRankings = document.getElementById("comparisonRankings");
const comparisonMatrix = document.getElementById("comparisonMatrix");
const historyList = document.getElementById("historyList");
const historyEmpty = document.getElementById("historyEmpty");
const clearHistoryButton = document.getElementById("clearHistoryButton");
const navLinks = [...document.querySelectorAll(".nav-links a[href^='#']")];
const benchmarkTop1 = document.getElementById("benchmarkTop1");
const benchmarkGrounding = document.getElementById("benchmarkGrounding");
const benchmarkCalibration = document.getElementById("benchmarkCalibration");
const benchmarkCases = document.getElementById("benchmarkCases");
const benchmarkSummary = document.getElementById("benchmarkSummary");

const HISTORY_KEY = "mindgrid-voyager-history-v2";
const HISTORY_LIMIT = 10;
const DEFAULT_CURRENCY = "USD";
let historyEntries = loadHistory();
let heroSubmissionActive = false;
let currentRecommendationRequest = null;

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function normalizeCurrency(value) {
  const normalized = String(value || DEFAULT_CURRENCY).trim().toUpperCase();
  return normalized || DEFAULT_CURRENCY;
}

function formatCurrency(value, currency = DEFAULT_CURRENCY) {
  const normalizedCurrency = normalizeCurrency(currency);
  const numericValue = Number(value || 0);
  try {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: normalizedCurrency,
      currencyDisplay: "symbol",
      maximumFractionDigits: normalizedCurrency === "JPY" ? 0 : 2
    }).format(numericValue);
  } catch (error) {
    return `${normalizedCurrency} ${numericValue.toLocaleString("en-US")}`;
  }
}

function formatPercent(value) {
  return `${Math.round(Number(value) || 0)}%`;
}

function formatConfidence(value) {
  const numeric = Number(value || 0);
  if (numeric <= 1) {
    return `${Math.round(numeric * 100)}% confidence`;
  }
  return `${Math.round(numeric)}% confidence`;
}

function formatLabel(value) {
  return String(value || "")
    .replaceAll("-", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function ensureArray(value) {
  return Array.isArray(value) ? value.filter(Boolean) : [];
}

function safeText(value, fallback) {
  const normalized = String(value ?? "").trim();
  return normalized || fallback;
}

function compactLabel(value, maxLength = 34) {
  const text = safeText(value, "");
  if (text.length <= maxLength) {
    return text;
  }
  return `${text.slice(0, maxLength - 3).trim()}...`;
}

function average(values) {
  if (!values.length) {
    return 0;
  }
  return values.reduce((sum, value) => sum + Number(value || 0), 0) / values.length;
}

function normalizeDestinationName(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function formatTimestamp(value) {
  try {
    return new Intl.DateTimeFormat("en-US", {
      dateStyle: "medium",
      timeStyle: "short"
    }).format(new Date(value));
  } catch (error) {
    return "Saved recently";
  }
}

function parseDestinationList(value) {
  const seen = new Set();
  return String(value)
    .split(/[\n,]+/)
    .map((item) => normalizeDestinationName(item))
    .filter((item) => {
      if (!item || seen.has(item.toLowerCase())) {
        return false;
      }
      seen.add(item.toLowerCase());
      return true;
    })
    .slice(0, 4);
}

function confidenceToPercent(value) {
  const numeric = Number(value || 0);
  if (numeric <= 1) {
    return Math.round(numeric * 100);
  }
  return Math.round(numeric);
}

function setComparisonState(state, message = "") {
  comparisonShell.dataset.state = state;
  comparisonEmpty.hidden = state !== "empty";
  comparisonLoading.hidden = state !== "loading";
  comparisonError.hidden = state !== "error";
  comparisonSuccess.hidden = state !== "success";

  if (message) {
    comparisonErrorMessage.textContent = message;
  }
}

function setPriorityBadge(element, priority) {
  const normalized = String(priority || "medium").toLowerCase();
  element.textContent = `${formatLabel(priority || "medium")} priority`;
  element.className = `decision-badge priority-${normalized}`;
}

function buildStageContributionFromRecommendation(recommendation) {
  const scores = recommendation.meta?.scores || {};
  const reason = recommendation.reasoningWorkflow?.reason || {};
  const decision = recommendation.decisionEngine || {};
  const verifyScore = Number(scores.safetyConfidence || reason.safetyScore || 0);

  return {
    Discover: Number(
      average([
        scores.destinationIntelligence,
        scores.localSignal,
        reason.popularityScore
      ]).toFixed(2)
    ),
    Verify: Number(verifyScore.toFixed(2)),
    Prioritize: Number(
      average([
        scores.budgetFit,
        reason.relevanceScore
      ]).toFixed(2)
    ),
    Explain: Number(
      average([
        decision.decision_score,
        confidenceToPercent(decision.confidence)
      ]).toFixed(2)
    )
  };
}

function stageReasonFor(label) {
  const reasons = {
    Discover: "Destination fit and local signal created the early advantage.",
    Verify: "Safety confidence and trust signals strengthened the rank.",
    Prioritize: "Budget fit and route relevance improved practicality.",
    Explain: "Confidence and final score made the recommendation easier to defend."
  };
  return reasons[label] || "Balanced performance across the decision workflow.";
}

function pickLeadingStage(stageContribution) {
  return Object.entries(stageContribution).sort((left, right) => right[1] - left[1])[0]?.[0] || "Discover";
}

function loadHistory() {
  try {
    const raw = window.localStorage.getItem(HISTORY_KEY);
    const parsed = JSON.parse(raw || "[]");
    return Array.isArray(parsed) ? parsed : [];
  } catch (error) {
    return [];
  }
}

function persistHistory() {
  try {
    window.localStorage.setItem(HISTORY_KEY, JSON.stringify(historyEntries.slice(0, HISTORY_LIMIT)));
  } catch (error) {
    // Ignore storage failures so the live experience keeps working.
  }
}

function saveHistoryEntry(entry) {
  historyEntries = [entry, ...historyEntries].slice(0, HISTORY_LIMIT);
  persistHistory();
  renderHistoryList();
}

function buildHistoryEntry(config) {
  return {
    id: `run-${Date.now()}-${Math.random().toString(16).slice(2, 8)}`,
    createdAt: new Date().toISOString(),
    ...config
  };
}

function setApiStatus(message, type) {
  apiStatus.textContent = message;
  apiStatus.classList.remove("is-online", "is-offline");
  if (type) {
    apiStatus.classList.add(type);
  }
}

function setActiveNavLink(id) {
  navLinks.forEach((link) => {
    const target = String(link.getAttribute("href") || "").replace("#", "");
    link.classList.toggle("is-active", target === id);
  });
}

function setResultsState(state, message = "") {
  resultsShell.dataset.state = state;
  resultsEmpty.hidden = state !== "empty";
  resultsLoading.hidden = state !== "loading";
  resultsError.hidden = state !== "error";
  resultsSuccess.hidden = state !== "success";

  if (message) {
    resultsErrorMessage.textContent = message;
  }
}

function setButtonState(button, isLoading, loadingLabel, idleLabel) {
  button.disabled = isLoading;
  button.textContent = isLoading ? loadingLabel : idleLabel;
}

function setHeroPromptState(isLoading, message = "") {
  if (!heroPromptButton || !heroPromptStatus) {
    return;
  }

  heroPromptButton.disabled = isLoading;
  heroPromptButton.textContent = isLoading ? "Running..." : "Run Decision Engine";
  if (message) {
    heroPromptStatus.textContent = message;
  }
}

function syncHeroPromptToRecommendationForm() {
  if (!heroPromptForm || !recommendationForm) {
    return;
  }

  recommendationForm.elements.destination.value = String(heroPromptDestination?.value || "").trim();
  recommendationForm.elements.budget.value = Number(heroPromptBudget?.value || 0) || 1800;
  recommendationForm.elements.currency.value = normalizeCurrency(heroPromptCurrency?.value || DEFAULT_CURRENCY);
  recommendationForm.elements.duration.value = Number(heroPromptDuration?.value || 0) || 4;
  recommendationForm.elements.travelStyle.value = String(heroPromptTravelStyle?.value || "Balanced Explorer");
  recommendationForm.elements.pace.value = String(heroPromptPace?.value || "balanced");
  recommendationForm.elements.interests.value = String(heroPromptInterests?.value || "").trim();
}

function parseInterests(value) {
  return String(value)
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function renderStackList(target, items) {
  const normalizedItems = ensureArray(items);
  if (!normalizedItems.length) {
    target.innerHTML = `
      <article class="stack-item">
        <p>No high-signal items were returned for this section yet.</p>
      </article>
    `;
    return;
  }

  target.innerHTML = normalizedItems
    .map(
      (item) => `
        <article class="stack-item">
          <div class="stack-top">
            <strong>${escapeHtml(item.name || item.title || "Untitled")}</strong>
            ${item.bestTime ? `<span>${escapeHtml(item.bestTime)}</span>` : ""}
          </div>
          <p>${escapeHtml(item.why || item.description || "")}</p>
          ${buildReferenceLinksMarkup(item.references)}
          ${item.estimatedCost !== undefined ? `<small>${escapeHtml(item.budgetBand || "mid")} | ${formatCurrency(item.estimatedCost, item.currency || DEFAULT_CURRENCY)}</small>` : ""}
        </article>
      `
    )
    .join("");
}

function buildReferenceLinksMarkup(references) {
  const normalized = ensureArray(references).filter((item) => item && item.url);
  if (!normalized.length) {
    return "";
  }

  return `
    <div class="stack-links">
      ${normalized
        .slice(0, 2)
        .map(
          (item) => `
            <a
              class="stack-link"
              href="${escapeHtml(item.url)}"
              target="_blank"
              rel="noreferrer noopener"
            >
              <span>${escapeHtml(item.platform || "Reference")}</span>
              <strong>${escapeHtml(compactLabel(item.title || item.query || "Open reference", 44))}</strong>
            </a>
          `
        )
        .join("")}
    </div>
  `;
}

function renderSimpleTextList(target, items, fallback) {
  const normalizedItems = ensureArray(items);
  if (!normalizedItems.length) {
    target.innerHTML = `
      <article class="stack-item">
        <p>${escapeHtml(fallback)}</p>
      </article>
    `;
    return;
  }

  target.innerHTML = normalizedItems
    .map((item) => `<article class="stack-item"><p>${escapeHtml(item)}</p></article>`)
    .join("");
}

function renderPillCloud(target, items, tone = "signal") {
  const normalizedItems = ensureArray(items);
  if (!normalizedItems.length) {
    target.innerHTML = `<span class="signal-pill signal-pill-${escapeHtml(tone)}">No signals yet</span>`;
    return;
  }

  target.innerHTML = normalizedItems
    .map((item) => `<span class="signal-pill signal-pill-${escapeHtml(tone)}">${escapeHtml(item)}</span>`)
    .join("");
}

function renderReasonSignals(target, items) {
  const normalizedItems = ensureArray(items);
  if (!normalizedItems.length) {
    target.innerHTML = `
      <article class="stack-item stack-item-compact">
        <p>No ranked evidence is available for this response.</p>
      </article>
    `;
    return;
  }

  target.innerHTML = normalizedItems
    .map(
      (item) => `
        <article class="stack-item stack-item-compact">
          <div class="stack-top">
            <strong>Signal</strong>
            <span>Decision evidence</span>
          </div>
          <p>${escapeHtml(item)}</p>
        </article>
      `
    )
    .join("");
}

function renderBudgetCard(data) {
  if (!data || !data.suggestedAllocation) {
    budgetCard.innerHTML = `
      <article class="stack-item">
        <p>Budget guidance is still being prepared for this destination.</p>
      </article>
    `;
    return;
  }

  const allocation = Object.entries(data.suggestedAllocation)
    .map(
      ([key, value]) => `
        <li><span>${escapeHtml(key)}</span><strong>${escapeHtml(value)}</strong></li>
      `
    )
    .join("");

  budgetCard.innerHTML = `
    <article class="stack-item">
      <div class="stack-top">
        <strong>${escapeHtml(data.tier)}</strong>
        <span>${formatCurrency(data.totalBudget, data.currency || DEFAULT_CURRENCY)} total</span>
      </div>
      <p>${escapeHtml(data.guidance)}</p>
      <small>${escapeHtml(data.destinationNote)}</small>
    </article>
    <article class="stack-item">
      <div class="stack-top">
        <strong>Budget per day</strong>
        <span>${formatCurrency(data.budgetPerDay, data.currency || DEFAULT_CURRENCY)}</span>
      </div>
      <ul class="allocation-list">${allocation}</ul>
    </article>
  `;
}

function renderSafetyCard(data) {
  if (!data) {
    safetyCard.innerHTML = `
      <article class="stack-item">
        <p>Safety guidance is unavailable for this response.</p>
      </article>
    `;
    return;
  }

  const notes = ensureArray(data.notes).map((note) => `<li>${escapeHtml(note)}</li>`).join("");
  safetyCard.innerHTML = `
    <article class="stack-item">
      <div class="stack-top">
        <strong>${escapeHtml(data.riskLevel)}</strong>
        <span>${escapeHtml(`${data.confidence}% confidence`)}</span>
      </div>
      <p>${escapeHtml(data.transportNote)}</p>
      <ul class="simple-list">${notes}</ul>
    </article>
  `;
}

function renderTips(items) {
  renderSimpleTextList(tipsList, items, "No travel tips were returned for this request.");
}

function renderItinerary(days) {
  const normalizedDays = ensureArray(days);
  if (!normalizedDays.length) {
    itineraryList.innerHTML = `
      <article class="stack-item">
        <p>No itinerary blocks were generated yet.</p>
      </article>
    `;
    return;
  }

  itineraryList.innerHTML = normalizedDays
    .map(
      (day) => `
        <article class="itinerary-day">
          <div class="card-head">
            <div>
              <p class="eyebrow">Day ${escapeHtml(day.day)}</p>
              <h5>${escapeHtml(day.theme)}</h5>
            </div>
            <span>${escapeHtml(day.summary)}</span>
          </div>
          <div class="itinerary-blocks">
            ${day.blocks
              .map(
                (block) => `
                  <div class="itinerary-block">
                    <strong>${escapeHtml(block.time)}</strong>
                    <h6>${escapeHtml(block.title)}</h6>
                    <p>${escapeHtml(block.description)}</p>
                  </div>
                `
              )
              .join("")}
          </div>
          ${buildReferenceLinksMarkup(day.references)}
        </article>
      `
    )
    .join("");
}

function renderWorkflow(recommendation) {
  const workflow = recommendation.reasoningWorkflow || {};
  const stageMap = ensureArray(recommendation.agenticPositioning?.stageMap);
  const perceive = workflow.perceive || {};
  const reason = workflow.reason || {};
  const plan = workflow.plan || {};
  const act = workflow.act || {};
  const decision = recommendation.decisionEngine || {};

  const steps = stageMap.length
    ? stageMap.map((step) => ({
      label: step.label,
      summary: step.summary,
      detail: step.detail
    }))
    : [
      {
        label: "Discover",
        summary: perceive.recognizedDestination ? "Seeded destination profile matched" : "Adaptive fallback profile engaged",
        detail: `${formatCurrency(perceive.budgetPerDay || 0, perceive.currency || recommendation.request?.currency || DEFAULT_CURRENCY)} per day | ${perceive.riskLevel || "Risk unknown"}`
      },
      {
        label: "Verify",
        summary: `Safety ${formatPercent(reason.safetyScore)} | Popularity ${formatPercent(reason.popularityScore)}`,
        detail: `Relevance ${formatPercent(reason.relevanceScore)} from interests, travel style, and budget fit`
      },
      {
        label: "Prioritize",
        summary: `${plan.itineraryDays || 0} itinerary days assembled`,
        detail: `${ensureArray(plan.topAttractions).length} attractions | ${ensureArray(plan.foodAndCafes).length} food picks`
      },
      {
        label: "Explain",
        summary: `${decision.priority_level || "Medium"} priority at ${Number(decision.decision_score || 0).toFixed(2)}`,
        detail: `${formatConfidence(decision.confidence || 0)} | ${act.responseMode || "decision-engine"}`
      }
    ];

  if (workflowTitle) {
    workflowTitle.textContent = "Discover -> Verify -> Prioritize -> Explain";
  }

  workflowSteps.innerHTML = steps
    .map(
      (step, index) => `
        <article class="workflow-step">
          <span class="workflow-index">0${index + 1}</span>
          <strong>${escapeHtml(step.label)}</strong>
          <p>${escapeHtml(step.summary)}</p>
          <small>${escapeHtml(step.detail)}</small>
        </article>
      `
    )
    .join("");
}

function applyPriorityBadge(priority) {
  setPriorityBadge(decisionPriority, priority);
}

function applySummaryPriority(priority) {
  setPriorityBadge(summaryTopPriority, priority);
}

function renderDebug(recommendation) {
  const { meta = {}, reasoningWorkflow = {}, decisionEngine = {} } = recommendation;
  traceIdValue.textContent = meta.traceId || reasoningWorkflow.traceId || decisionEngine.traceId || "n/a";
  debugDecisionEngineVersion.textContent = meta.decisionEngineVersion || "n/a";
  debugResponseMode.textContent = meta.mode || reasoningWorkflow.act?.responseMode || "n/a";
  debugRecognized.textContent = meta.recognizedDestination ? "Seeded destination" : "Fallback intelligence";
}

function renderResultsSummary(recommendation) {
  const summary = recommendation.resultsSummary || {};
  summaryTopDestination.textContent = safeText(summary.topRankedDestination, recommendation.request.destination);
  summaryWhyFirst.textContent = safeText(
    summary.whyRankedFirst,
    recommendation.destinationSummary.explanationSummary || recommendation.destinationSummary.whyThisWorks
  );
  summaryTotalAnalyzed.textContent = safeText(summary.totalDestinationsAnalyzed, "1");
  summaryAverageScore.textContent = Number(summary.averageScore || recommendation.decisionEngine?.decision_score || 0).toFixed(2);
  summaryAverageConfidence.textContent = formatConfidence(
    summary.averageConfidence || recommendation.decisionEngine?.confidence || 0
  );
  summaryTripStyle.textContent = safeText(recommendation.request.travelStyle, "Balanced Explorer");
  applySummaryPriority(summary.topPriorityLevel || recommendation.decisionEngine?.priority_level);
}

function renderVerification(recommendation) {
  if (!verificationStatus) {
    return;
  }

  const verification = recommendation.sourceVerification || {};
  const summary = verification.verificationSummary || {};
  const citations = ensureArray(verification.citations);
  const ledger = ensureArray(verification.signalLedger).map(
    (item) => `${safeText(item.label, "Signal")}: ${formatPercent(item.score || 0)} | ${safeText(item.reason, "No explanation")}`
  );

  verificationStatus.textContent = safeText(summary.status, "Pending");
  verificationTrustScore.textContent = formatPercent(summary.trustScore || 0);
  verificationFreshness.textContent = safeText(summary.freshness, "Seeded intelligence + local runtime");
  verificationSummary.textContent = safeText(
    summary.reason,
    "Verification details will appear here once the decision engine finishes."
  );
  renderReferenceCitationList(verificationCitations, citations);
  renderSimpleTextList(
    verificationLedger,
    ledger,
    "No verification ledger entries were returned for this recommendation."
  );
}

function renderReferenceCitationList(target, citations) {
  const normalized = ensureArray(citations);
  if (!normalized.length) {
    target.innerHTML = `
      <article class="stack-item">
        <p>No verification citations were returned for this recommendation.</p>
      </article>
    `;
    return;
  }

  target.innerHTML = normalized
    .map((item) => {
      const title = safeText(item.label, "Source");
      const meta = `${safeText(item.type, "engine")} | ${formatPercent(item.confidence || 0)}`;
      const reason = safeText(item.reason, "");
      if (item.url) {
        return `
          <article class="stack-item stack-item-compact">
            <div class="stack-top">
              <strong>${escapeHtml(title)}</strong>
              <span>${escapeHtml(meta)}</span>
            </div>
            ${reason ? `<p>${escapeHtml(reason)}</p>` : ""}
            <a
              class="stack-link stack-link-inline"
              href="${escapeHtml(item.url)}"
              target="_blank"
              rel="noreferrer noopener"
            >
              <span>${escapeHtml(item.type || "reference")}</span>
              <strong>Open source</strong>
            </a>
          </article>
        `;
      }

      return `
        <article class="stack-item stack-item-compact">
          <div class="stack-top">
            <strong>${escapeHtml(title)}</strong>
            <span>${escapeHtml(meta)}</span>
          </div>
          ${reason ? `<p>${escapeHtml(reason)}</p>` : ""}
        </article>
      `;
    })
    .join("");
}

function renderGroundingEvidence(recommendation) {
  const grounding = recommendation.grounding || {};
  const metrics = grounding.metrics || {};
  const evidence = ensureArray(grounding.destinationEvidence);
  if (!evidence.length) {
    groundingEvidenceList.innerHTML = `
      <article class="stack-item">
        <p>No grounded evidence snippets were returned for this recommendation.</p>
      </article>
    `;
    return;
  }

  const metricCard = `
    <article class="stack-item stack-item-compact">
      <div class="stack-top">
        <strong>Retrieval summary</strong>
        <span>${escapeHtml(formatLabel(grounding.method || "seeded evidence retrieval"))}</span>
      </div>
      <p>${escapeHtml(`Coverage ${Math.round(Number(metrics.coverageScore || 0))}% | Trust ${Math.round(Number(metrics.trustScore || 0))}% | Recency ${Math.round(Number(metrics.recencyScore || 0))}%`)}</p>
      <p>${escapeHtml(`${Number(metrics.contentGroundedDocuments || 0)} passage-grounded | ${Number(metrics.metadataOnlyDocuments || 0)} metadata-only | ${safeText(grounding.contentGroundingMode, "seeded-passages")}`)}</p>
    </article>
  `;

  groundingEvidenceList.innerHTML = [
    metricCard,
    ...evidence.slice(0, 3).map(
      (item) => `
        <article class="stack-item stack-item-compact">
          <div class="stack-top">
            <strong>${escapeHtml(item.title || "Evidence source")}</strong>
            <span>${escapeHtml(item.contentGrounded ? "Passage grounded" : "Metadata only")}</span>
          </div>
          <p>${escapeHtml(item.groundedClaim || item.excerpt || "Evidence excerpt unavailable.")}</p>
          <small>${escapeHtml(`Trust ${Math.round(Number(item.trust || 0) * 100)}% | ${safeText(item.attribution, item.sourceType || "source")} | ${safeText(item.contentMode, "seeded-passage")}`)}</small>
          ${item.url ? `
            <a class="stack-link stack-link-inline" href="${escapeHtml(item.url)}" target="_blank" rel="noreferrer noopener">
              <span>${escapeHtml(item.legalBasis || item.sourceType || "source")}</span>
              <strong>Open evidence</strong>
            </a>
          ` : ""}
        </article>
      `
    ),
  ].join("");
}

function renderModelDiagnostics(recommendation) {
  const diagnostics = recommendation.modelDiagnostics || {};
  const intentDiagnostics = recommendation.intentDiagnostics || {};
  const calibration = diagnostics.calibrationDiagnostics || {};
  const scoringPipeline = diagnostics.scoringPipeline || {};
  const priorLayer = scoringPipeline.prior || {};
  const learnedLayer = scoringPipeline.learned || {};
  const breakdown = ensureArray(diagnostics.featureBreakdown);
  if (!breakdown.length) {
    modelFeatureList.innerHTML = `
      <article class="stack-item">
        <p>Model diagnostics were not available for this result.</p>
      </article>
    `;
    return;
  }

  const intentSummary = `
    <article class="stack-item stack-item-compact">
      <div class="stack-top">
        <strong>Intent fit</strong>
        <span>${escapeHtml(safeText(diagnostics.calibrationBand, "Medium"))} calibration</span>
      </div>
      <p>${escapeHtml(`Matched: ${ensureArray(intentDiagnostics.matchedInterestTokens).slice(0, 4).join(", ") || "none"}`)}</p>
      <p>${escapeHtml(`Missing: ${ensureArray(intentDiagnostics.missingInterestTokens).slice(0, 4).join(", ") || "none"}`)}</p>
      <p>${escapeHtml(`Confidence ${formatConfidence(diagnostics.confidence || 0)} | mode ${safeText(calibration.mode, "raw-model")}`)}</p>
    </article>
  `;

  const scorePipelineSummary = `
    <article class="stack-item stack-item-compact">
      <div class="stack-top">
        <strong>Score pipeline</strong>
        <span>${escapeHtml(safeText(scoringPipeline.mode, "blended-model"))}</span>
      </div>
      <p>${escapeHtml(`Final score ${Number(diagnostics.score || 0).toFixed(2)} from prior ${Math.round(Number(priorLayer.weight || 0) * 100)}% + learned ${Math.round(Number(learnedLayer.weight || 0) * 100)}% layers.`)}</p>
      <p>${escapeHtml(`Prior ${formatPercent(Number(priorLayer.probability || 0) * 100)} | learned ${formatPercent(Number(learnedLayer.probability || 0) * 100)} | blended ${formatPercent(Number(scoringPipeline.blendedProbability || 0) * 100)}`)}</p>
    </article>
  `;

  modelFeatureList.innerHTML = [
    intentSummary,
    scorePipelineSummary,
    ...breakdown.slice(0, 5).map(
      (item) => `
        <article class="stack-item stack-item-compact">
          <div class="stack-top">
            <strong>${escapeHtml(formatLabel(String(item.feature || "").replaceAll("_", "-")))}</strong>
            <span>${escapeHtml(`${formatLabel(item.dominantLayer || "learned")} led`)}</span>
          </div>
          <p>${escapeHtml(`Value ${Number(item.value || 0).toFixed(2)} | blended contribution ${Number(item.contribution || 0).toFixed(2)}`)}</p>
          <p>${escapeHtml(`Prior ${Number(item.priorContribution || 0).toFixed(2)} (w ${Number(item.priorWeight || 0).toFixed(3)}) | learned ${Number(item.learnedContribution || 0).toFixed(2)} (w ${Number(item.learnedWeight || 0).toFixed(3)})`)}</p>
        </article>
      `
    ),
  ].join("");
}

function renderAgenticExperience(recommendation) {
  if (!aiMissionTitle) {
    return;
  }

  const agentic = recommendation.agenticExperience || {};
  const mission = agentic.missionBrief || {};
  const narrative = agentic.decisionNarrative || {};
  const playbook = agentic.agentPlaybook || {};
  const memory = agentic.memoryDraft || {};
  const modelLayer = agentic.modelLayer || {};

  aiMissionTitle.textContent = safeText(
    mission.title,
    `${recommendation.request.destination} mission brief`
  );
  aiMissionSummary.textContent = safeText(
    mission.summary,
    modelLayer.executiveBrief
      || narrative.shortSummary
      || recommendation.destinationSummary?.whyThisWorks
      || "Generated mission summary unavailable."
  );
  aiMissionOperatorNote.textContent = safeText(
    mission.operatorNote,
    modelLayer.decisionMemo
      || narrative.confidenceNarrative
      || "No operator note was generated for this response."
  );
  aiFocusStage.textContent = safeText(mission.focusLabel, "Discover");
  aiBestMoment.textContent = safeText(
    mission.bestMoment,
    recommendation.bestTimeToVisit?.window || "Flexible timing"
  );
  aiGenerationMode.textContent = safeText(
    formatLabel(String(agentic.mode || "").replaceAll("_", "-")),
    "Local template generation"
  );
  if (aiModelProvider) {
    aiModelProvider.textContent = safeText(
      `${formatLabel(String(modelLayer.provider || "mindgrid-local").replaceAll("_", "-"))} | ${safeText(modelLayer.model, "template")}`,
      "Mindgrid local"
    );
  }
  if (aiModelMode) {
    aiModelMode.textContent = safeText(
      formatLabel(String(modelLayer.mode || "local-simulated-llm").replaceAll("_", "-")),
      "Local simulated llm"
    );
  }
  if (aiModelSummary) {
    aiModelSummary.textContent = safeText(
      modelLayer.assistantReply,
      "Use a follow-up instruction to make the decision engine replan this trip."
    );
  }

  renderSimpleTextList(
    agentNextActions,
    playbook.nextActions,
    "No next-step actions were generated for this recommendation."
  );
  renderSimpleTextList(
    agentVerificationChecklist,
    playbook.verificationChecklist,
    "No verification checklist was generated for this recommendation."
  );
  aiJournalTitle.textContent = safeText(memory.journalTitle, "Generated memory draft");
  aiJournalPreview.textContent = safeText(
    memory.journalPreview,
    "The generative trip journal preview will appear here."
  );
  aiShareableSummary.textContent = safeText(
    memory.shareableSummary,
    "A concise shareable trip summary will appear here."
  );
  renderSimpleTextList(
    agentReplanTriggers,
    playbook.replanTriggers,
    "No replan triggers were generated for this destination."
  );
  renderSimpleTextList(
    agentFollowUpQuestions,
    playbook.followUpQuestions?.length ? playbook.followUpQuestions : modelLayer.nextPromptSuggestions,
    "No follow-up prompts were generated for this destination."
  );
  renderPillCloud(
    aiMemoryMoments,
    memory.memoryMoments || mission.bestFor || [],
    "signal"
  );
}

async function refreshEvaluationSnapshot() {
  if (!benchmarkTop1 || window.location.protocol === "file:") {
    return;
  }

  try {
    const payload = await fetchJson("/api/evaluation", { headers: { Accept: "application/json" } });
    const summary = payload.evaluation?.summary || {};
    const benchmarkCaseCount = Number(summary.benchmarkCaseCount || summary.caseCount || 0);
    const headlineMode = safeText(summary.mode, "out-of-sample temporal backtest");
    benchmarkTop1.textContent = `${Math.round(Number(summary.top1Accuracy || 0))}%`;
    benchmarkGrounding.textContent = `${Math.round(Number(summary.averageGroundingCoverage || 0))}%`;
    benchmarkCalibration.textContent = `${Math.round(Number(summary.calibrationGap || 0))}%`;
    benchmarkCases.textContent = benchmarkCaseCount
      ? `${safeText(summary.caseCount, "--")}/${benchmarkCaseCount}`
      : safeText(summary.caseCount, "--");
    benchmarkSummary.textContent = `Current ${headlineMode.replaceAll("-", " ")} reports ${Math.round(Number(summary.top1Accuracy || 0))}% top-1 accuracy and ${Math.round(Number(summary.top3Coverage || 0))}% top-3 coverage across ${safeText(summary.caseCount, 0)} held-out scenarios from ${benchmarkCaseCount || safeText(summary.caseCount, 0)} total benchmark cases, with ${Math.round(Number(summary.averageGroundingCoverage || 0))}% average grounding coverage and a ${Math.round(Number(summary.calibrationGap || 0))}% calibration gap.`;
  } catch (error) {
    benchmarkTop1.textContent = "n/a";
    benchmarkGrounding.textContent = "n/a";
    benchmarkCalibration.textContent = "n/a";
    benchmarkCases.textContent = "n/a";
    if (benchmarkSummary) {
      benchmarkSummary.textContent = "Local benchmark metrics are unavailable until the backend evaluation layer responds.";
    }
  }
}

function renderRecommendation(payload, options = {}) {
  const recommendation = payload.recommendation;
  const { meta = {}, decisionEngine = {}, reasoningWorkflow = {} } = recommendation;
  const scores = meta.scores || {};
  const supportingSignals = recommendation.supportingSignals || {};
  const combinedSignals = [
    ...ensureArray(supportingSignals.core),
    ...ensureArray(supportingSignals.styleIndicators),
    ...ensureArray(supportingSignals.social).map((item) => compactLabel(item))
  ].slice(0, 8);
  const tripStyleIndicator = safeText(recommendation.request.travelStyle, "Balanced Explorer");
  currentRecommendationRequest = {
    destination: recommendation.request.destination,
    budget: recommendation.request.budget,
    currency: normalizeCurrency(recommendation.request.currency || DEFAULT_CURRENCY),
    duration: recommendation.request.duration,
    interests: ensureArray(recommendation.request.interests),
    travelStyle: recommendation.request.travelStyle,
    pace: recommendation.request.pace,
    traceId: safeText(meta.traceId, "")
  };

  renderResultsSummary(recommendation);
  resultDestinationName.textContent = recommendation.request.destination;
  applyPriorityBadge(decisionEngine.priority_level);
  decisionExplanation.textContent = safeText(
    decisionEngine.reason_summary,
    recommendation.destinationSummary.explanationSummary || recommendation.destinationSummary.whyThisWorks
  );
  resultHeadline.textContent = safeText(recommendation.destinationSummary.headline, "Destination intelligence summary");
  resultOverview.textContent = safeText(recommendation.destinationSummary.overview, "Overview unavailable.");
  resultWhyWorks.textContent = safeText(recommendation.destinationSummary.whyThisWorks, "No explanation was returned.");
  resultTravelFit.textContent = safeText(recommendation.destinationSummary.travelStyleFit, "Travel style fit is still being prepared.");
  resultBestTime.textContent = safeText(recommendation.bestTimeToVisit?.window, "Flexible");
  decisionScoreValue.textContent = Number(decisionEngine.decision_score || 0).toFixed(2);
  decisionConfidence.textContent = formatConfidence(decisionEngine.confidence || 0);
  decisionRiskLevel.textContent = safeText(decisionEngine.risk_level, recommendation.safetyAndRisk?.riskLevel || "Medium");
  decisionHistoryState.textContent = options.restored ? "Restored locally" : "Stored locally";
  scoreDestination.textContent = formatPercent(scores.destinationIntelligence);
  scoreBudget.textContent = formatPercent(scores.budgetFit);
  scoreLocal.textContent = formatPercent(scores.localSignal);
  scoreSafety.textContent = formatPercent(scores.safetyConfidence);
  scoreTripStyle.textContent = tripStyleIndicator;

  renderWorkflow(recommendation);
  renderPillCloud(evidenceSignals, combinedSignals.length ? combinedSignals : meta.signals || [], "signal");
  renderReasonSignals(reasonSignals, reasoningWorkflow.reason?.topSignals || []);
  renderPillCloud(
    sourcesUsed,
    decisionEngine.sources_used || reasoningWorkflow.perceive?.sourcesUsed || [],
    "source"
  );
  renderSimpleTextList(
    itineraryHintsList,
    supportingSignals.itineraryHints,
    "No itinerary hints were returned for this destination."
  );
  renderGroundingEvidence(recommendation);
  renderModelDiagnostics(recommendation);
  renderVerification(recommendation);
  renderDebug(recommendation);
  renderStackList(attractionsList, recommendation.topAttractions);
  renderStackList(foodList, recommendation.foodAndCafes);
  renderStackList(favoritesList, recommendation.localFavorites);
  renderItinerary(recommendation.dayWiseItinerary);
  renderBudgetCard(recommendation.budgetGuidance);
  renderSafetyCard(recommendation.safetyAndRisk);
  renderTips(recommendation.travelTips);
  renderAgenticExperience(recommendation);
  if (feedbackStatus) {
    feedbackStatus.textContent = "Save whether this recommendation felt right, needed replanning, or missed the brief.";
  }
  setResultsState("success");
  if (!options.skipScroll) {
    resultsShell.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

function buildComparisonEntry(payloadResponse) {
  const recommendation = payloadResponse.recommendation;
  const decision = recommendation.decisionEngine || {};
  const supportingSignals = recommendation.supportingSignals || {};
  const scores = recommendation.meta?.scores || {};
  const rankings = ensureArray(recommendation.resultsSummary?.rankings);
  const rankedMatch = rankings.find(
    (item) => String(item.destination || "").toLowerCase() === String(recommendation.request.destination || "").toLowerCase()
  ) || {};
  const stageContribution = rankedMatch.stageContribution || buildStageContributionFromRecommendation(recommendation);
  const leadingStage = rankedMatch.leadingStage || pickLeadingStage(stageContribution);
  const bestForList = ensureArray(supportingSignals.bestFor).length
    ? ensureArray(supportingSignals.bestFor)
    : ensureArray(rankedMatch.bestFor);

  return {
    destination: recommendation.request.destination,
    score: Number(decision.decision_score || 0),
    confidencePercent: confidenceToPercent(decision.confidence || rankedMatch.confidence || 0),
    priority: safeText(decision.priority_level, rankedMatch.priorityLevel || "Medium"),
    explanation: safeText(
      recommendation.agenticExperience?.decisionNarrative?.shortSummary
        || decision.reason_summary
        || recommendation.destinationSummary?.explanationSummary
        || recommendation.destinationSummary?.whyThisWorks,
      "No generated explanation is available."
    ),
    whyRanked: safeText(
      recommendation.agenticExperience?.decisionNarrative?.whyThisWon
        || rankedMatch.why
        || recommendation.destinationSummary?.explanationSummary
        || recommendation.destinationSummary?.whyThisWorks,
      "No ranking explanation is available."
    ),
    budgetFit: Number(scores.budgetFit || rankedMatch.budgetFit || 0),
    safety: Number(scores.safetyConfidence || rankedMatch.safety || recommendation.safetyAndRisk?.confidence || 0),
    localSignal: Number(scores.localSignal || rankedMatch.localSignal || 0),
    tripStyle: safeText(
      recommendation.request.travelStyle,
      ensureArray(rankedMatch.tripStyle)[0] || "Balanced Explorer"
    ),
    bestFor: safeText(bestForList[0], "Balanced trip"),
    evidence: [
      ...ensureArray(supportingSignals.core),
      ...ensureArray(supportingSignals.styleIndicators),
      ...ensureArray(rankedMatch.signals)
    ].slice(0, 4),
    traceId: safeText(recommendation.meta?.traceId, decision.traceId || "n/a"),
    leadingStage,
    leadingStageReason: safeText(rankedMatch.stageReason, stageReasonFor(leadingStage)),
    stageContribution,
    raw: payloadResponse
  };
}

function renderComparisonCards(entries) {
  comparisonRankings.innerHTML = entries
    .map(
      (entry, index) => `
        <article class="comparison-card ${index === 0 ? "comparison-card-top" : ""}">
          <div class="comparison-card-head">
            <div class="comparison-card-destination">
              <span class="comparison-rank">#${index + 1}</span>
              <h4>${escapeHtml(entry.destination)}</h4>
            </div>
            <span class="decision-badge priority-${escapeHtml(String(entry.priority).toLowerCase())}">
              ${escapeHtml(formatLabel(entry.priority))} priority
            </span>
          </div>

          <div class="comparison-card-score">
            <span>Decision score</span>
            <strong>${Number(entry.score).toFixed(2)}</strong>
            <small>${escapeHtml(`${entry.confidencePercent}% confidence`)}</small>
          </div>

          <p class="comparison-card-why">${escapeHtml(compactLabel(entry.explanation, 170))}</p>

          <div class="comparison-tag-row">
            <span class="comparison-tag">Best for ${escapeHtml(entry.bestFor)}</span>
            <span class="comparison-tag">Lead stage ${escapeHtml(entry.leadingStage)}</span>
          </div>

          <div class="comparison-card-metrics">
            <article class="comparison-mini-metric">
              <span>Budget fit</span>
              <strong>${escapeHtml(formatPercent(entry.budgetFit))}</strong>
            </article>
            <article class="comparison-mini-metric">
              <span>Safety</span>
              <strong>${escapeHtml(formatPercent(entry.safety))}</strong>
            </article>
            <article class="comparison-mini-metric">
              <span>Local signal</span>
              <strong>${escapeHtml(formatPercent(entry.localSignal))}</strong>
            </article>
            <article class="comparison-mini-metric">
              <span>Trip style</span>
              <strong>${escapeHtml(entry.tripStyle)}</strong>
            </article>
          </div>

          <div class="comparison-card-foot">
            <span class="comparison-foot-note">${escapeHtml(entry.leadingStageReason)}</span>
          </div>
        </article>
      `
    )
    .join("");
}

function renderComparisonTable(entries) {
  const rows = [
    ["Decision score", (entry) => Number(entry.score).toFixed(2)],
    ["Confidence", (entry) => `${entry.confidencePercent}%`],
    ["Priority", (entry) => formatLabel(entry.priority)],
    ["Best for", (entry) => entry.bestFor],
    ["Budget fit", (entry) => formatPercent(entry.budgetFit)],
    ["Safety", (entry) => formatPercent(entry.safety)],
    ["Local signal", (entry) => formatPercent(entry.localSignal)],
    ["Trip style", (entry) => entry.tripStyle],
    ["Lead stage", (entry) => `${entry.leadingStage} | ${entry.leadingStageReason}`],
    ["Why this ranks here", (entry) => compactLabel(entry.whyRanked, 140)]
  ];

  comparisonMatrix.innerHTML = `
    <div class="comparison-matrix-grid">
      ${rows
        .map(
          ([label, formatter]) => `
            <article class="comparison-matrix-row">
              <div class="comparison-matrix-label">${escapeHtml(label)}</div>
              <div class="comparison-matrix-values">
                ${entries
                  .map(
                    (entry) => `
                      <div class="comparison-matrix-value">
                        <span class="comparison-matrix-destination">${escapeHtml(entry.destination)}</span>
                        <span class="comparison-matrix-signal">${escapeHtml(formatter(entry))}</span>
                      </div>
                    `
                  )
                  .join("")}
              </div>
            </article>
          `
        )
        .join("")}
    </div>
  `;
}

function renderComparisonSession(payloadResponses, options = {}) {
  const entries = ensureArray(payloadResponses).map(buildComparisonEntry).sort((left, right) => right.score - left.score);
  if (!entries.length) {
    setComparisonState("empty");
    return null;
  }

  const topEntry = entries[0];
  comparisonTopDestination.textContent = topEntry.destination;
  comparisonTopReason.textContent = topEntry.whyRanked;
  comparisonComparedCount.textContent = String(entries.length);
  comparisonAverageScore.textContent = average(entries.map((entry) => entry.score)).toFixed(2);
  comparisonAverageConfidence.textContent = `${Math.round(average(entries.map((entry) => entry.confidencePercent)))}% confidence`;
  comparisonTopBestFor.textContent = topEntry.bestFor;
  setPriorityBadge(comparisonTopPriority, topEntry.priority);

  renderComparisonCards(entries);
  renderComparisonTable(entries);
  setComparisonState("success");

  if (!options.skipScroll) {
    comparisonShell.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  return {
    entries,
    topEntry
  };
}

function renderHistoryList() {
  if (!historyEntries.length) {
    historyEmpty.hidden = false;
    historyList.innerHTML = "";
    return;
  }

  historyEmpty.hidden = true;
  historyList.innerHTML = historyEntries
    .map(
      (entry) => `
        <button class="history-button" type="button" data-history-id="${escapeHtml(entry.id)}">
          <div class="history-header">
            <div class="history-title">
              <strong>${escapeHtml(entry.mode === "comparison" ? "Comparison run" : "Recommendation run")}</strong>
              <small>${escapeHtml(formatTimestamp(entry.createdAt))}</small>
            </div>
            <span class="history-mode-pill">
              ${escapeHtml(entry.mode === "comparison" ? `${entry.destinations.length} destinations` : "Single destination")}
            </span>
          </div>
          <p class="history-destinations">${escapeHtml(entry.destinations.join(", "))}</p>
          <div class="history-meta">
            <article>
              <span>Top result</span>
              <strong>${escapeHtml(entry.topRankedDestination)}</strong>
            </article>
            <article>
              <span>Avg score</span>
              <strong>${escapeHtml(Number(entry.averageScore || 0).toFixed(2))}</strong>
            </article>
          </div>
        </button>
      `
    )
    .join("");

  historyList.querySelectorAll("[data-history-id]").forEach((button) => {
    button.addEventListener("click", () => restoreHistoryEntry(button.dataset.historyId));
  });
}

function populateSingleForm(entry) {
  recommendationForm.elements.destination.value = entry.form.destination;
  recommendationForm.elements.budget.value = entry.form.budget;
  recommendationForm.elements.currency.value = normalizeCurrency(entry.form.currency || DEFAULT_CURRENCY);
  recommendationForm.elements.duration.value = entry.form.duration;
  recommendationForm.elements.travelStyle.value = entry.form.travelStyle;
  recommendationForm.elements.pace.value = entry.form.pace;
  recommendationForm.elements.interests.value = entry.form.interests;

  if (heroPromptDestination) {
    heroPromptDestination.value = entry.form.destination;
  }
  if (heroPromptBudget) {
    heroPromptBudget.value = entry.form.budget;
  }
  if (heroPromptCurrency) {
    heroPromptCurrency.value = normalizeCurrency(entry.form.currency || DEFAULT_CURRENCY);
  }
  if (heroPromptDuration) {
    heroPromptDuration.value = entry.form.duration;
  }
  if (heroPromptTravelStyle) {
    heroPromptTravelStyle.value = entry.form.travelStyle;
  }
  if (heroPromptPace) {
    heroPromptPace.value = entry.form.pace;
  }
  if (heroPromptInterests) {
    heroPromptInterests.value = entry.form.interests;
  }
}

function populateComparisonForm(entry) {
  comparisonDestinationsInput.value = entry.form.destinations.join(", ");
  comparisonForm.elements.budget.value = entry.form.budget;
  comparisonForm.elements.currency.value = normalizeCurrency(entry.form.currency || DEFAULT_CURRENCY);
  comparisonForm.elements.duration.value = entry.form.duration;
  comparisonForm.elements.travelStyle.value = entry.form.travelStyle;
  comparisonForm.elements.pace.value = entry.form.pace;
  comparisonForm.elements.interests.value = entry.form.interests;
  syncCompareChips();
}

function restoreHistoryEntry(id) {
  const entry = historyEntries.find((item) => item.id === id);
  if (!entry) {
    return;
  }

  if (entry.mode === "comparison") {
    populateComparisonForm(entry);
    renderComparisonSession(entry.payloads, { restored: true, skipScroll: false });
    comparisonStatus.textContent = `Restored comparison run from ${formatTimestamp(entry.createdAt)}.`;
    return;
  }

  populateSingleForm(entry);
  renderRecommendation(entry.payload, { restored: true, skipScroll: false });
  recommendationStatus.textContent = `Restored recommendation for ${entry.topRankedDestination}.`;
}

function syncCompareChips() {
  const activeDestinations = parseDestinationList(comparisonDestinationsInput.value).map((item) => item.toLowerCase());
  compareChips.forEach((chip) => {
    chip.classList.toggle(
      "is-active",
      activeDestinations.includes(String(chip.dataset.compareDestination || "").toLowerCase())
    );
  });
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.details || payload.error || payload.message || "Request failed.");
  }
  return payload;
}

async function checkBackendHealth() {
  if (window.location.protocol === "file:") {
    setApiStatus("Static preview mode. Run python app.py for live API support.", "is-offline");
    demoCount.textContent = "-";
    recommendationCount.textContent = "-";
    return;
  }

  try {
    const payload = await fetchJson("/health", { headers: { Accept: "application/json" } });
    const healthLabel = payload.version ? `v${payload.version}` : "local";
    setApiStatus(`API online | ${healthLabel}`, "is-online");
  } catch (error) {
    setApiStatus("Backend offline. Start python app.py to enable live requests.", "is-offline");
  }
}

async function refreshCounts() {
  if (window.location.protocol === "file:") {
    return;
  }

  try {
    const [demoSummary, recommendationSummary] = await Promise.all([
      fetchJson("/api/demo-request", { headers: { Accept: "application/json" } }),
      fetchJson("/api/recommendations", { headers: { Accept: "application/json" } })
    ]);
    demoCount.textContent = demoSummary.count;
    recommendationCount.textContent = recommendationSummary.count;
  } catch (error) {
    demoCount.textContent = "n/a";
    recommendationCount.textContent = "n/a";
  }
}

function handleHeroPromptSubmit(event) {
  event.preventDefault();

  if (!heroPromptForm || !recommendationForm) {
    return;
  }

  syncHeroPromptToRecommendationForm();
  heroSubmissionActive = true;
  setHeroPromptState(true, "Passing the brief into the live decision engine...");
  recommendationForm.scrollIntoView({ behavior: "smooth", block: "start" });
  if (typeof recommendationForm.requestSubmit === "function") {
    recommendationForm.requestSubmit();
    return;
  }

  recommendationForm.dispatchEvent(new Event("submit", { bubbles: true, cancelable: true }));
}

async function handleRecommendationSubmit(event) {
  event.preventDefault();

  if (window.location.protocol === "file:") {
    recommendationStatus.textContent = "Start the Python server first so recommendations can call the local API.";
    setHeroPromptState(false, "Start the Python server first so the hero prompt can reach the local API.");
    return;
  }

  const formData = new FormData(recommendationForm);
  const payload = {
    destination: String(formData.get("destination") || "").trim(),
    budget: Number(formData.get("budget") || 0),
    currency: normalizeCurrency(formData.get("currency") || DEFAULT_CURRENCY),
    duration: Number(formData.get("duration") || 0),
    interests: parseInterests(formData.get("interests") || ""),
    travelStyle: String(formData.get("travelStyle") || "").trim(),
    pace: String(formData.get("pace") || "balanced").trim()
  };

  setResultsState("loading");
  setButtonState(recommendationButton, true, "Generating...", "Generate AI Exploration Plan");
  recommendationStatus.textContent = "Running the decision engine across discovery, verification, prioritization, and explanation...";

  try {
    const payloadResponse = await fetchJson("/api/recommendations", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json"
      },
      body: JSON.stringify(payload)
    });
    renderRecommendation(payloadResponse);
    recommendationStatus.textContent = `Decision output ready for ${payloadResponse.recommendation.request.destination}.`;
    if (heroSubmissionActive) {
      heroPromptStatus.textContent = `Decision output ready for ${payloadResponse.recommendation.request.destination}.`;
      if (heroPromptDestination) {
        heroPromptDestination.value = payloadResponse.recommendation.request.destination;
      }
    }
    saveHistoryEntry(
      buildHistoryEntry({
        mode: "single",
        destinations: [payloadResponse.recommendation.request.destination],
        topRankedDestination: payloadResponse.recommendation.request.destination,
        averageScore: payloadResponse.recommendation.decisionEngine?.decision_score || 0,
        form: {
          destination: payload.destination,
          budget: payload.budget,
          currency: payload.currency,
          duration: payload.duration,
          travelStyle: payload.travelStyle,
          pace: payload.pace,
          interests: ensureArray(payload.interests).join(", ")
        },
        payload: payloadResponse
      })
    );
    await refreshCounts();
  } catch (error) {
    const fallbackMessage =
      error.message || "Unable to generate a recommendation. Try Bangkok, Tokyo, Bali, Dubai, Singapore, Paris, or Goa.";
    setResultsState("error", fallbackMessage);
    recommendationStatus.textContent = fallbackMessage;
    if (heroSubmissionActive) {
      heroPromptStatus.textContent = fallbackMessage;
    }
  } finally {
    setButtonState(recommendationButton, false, "Generating...", "Generate AI Exploration Plan");
    if (heroSubmissionActive) {
      heroSubmissionActive = false;
      setHeroPromptState(false, heroPromptStatus.textContent);
    }
  }
}

async function handleComparisonSubmit(event) {
  event.preventDefault();

  if (window.location.protocol === "file:") {
    comparisonStatus.textContent = "Start the Python server first so comparison mode can call the local API.";
    return;
  }

  const formData = new FormData(comparisonForm);
  const destinations = parseDestinationList(formData.get("destinations") || "");
  if (destinations.length < 2 || destinations.length > 4) {
    const message = "Enter 2 to 4 destinations separated by commas or line breaks.";
    setComparisonState("error", message);
    comparisonStatus.textContent = message;
    return;
  }

  const sharedPayload = {
    budget: Number(formData.get("budget") || 0),
    currency: normalizeCurrency(formData.get("currency") || DEFAULT_CURRENCY),
    duration: Number(formData.get("duration") || 0),
    interests: parseInterests(formData.get("interests") || ""),
    travelStyle: String(formData.get("travelStyle") || "").trim(),
    pace: String(formData.get("pace") || "balanced").trim()
  };

  setComparisonState("loading");
  setButtonState(comparisonButton, true, "Comparing...", "Compare Destinations");
  comparisonStatus.textContent = "Running the same trip brief across all selected destinations...";

  try {
    const results = await Promise.allSettled(
      destinations.map((destination) =>
        fetchJson("/api/recommendations", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json"
          },
          body: JSON.stringify({
            destination,
            ...sharedPayload
          })
        })
      )
    );

    const successfulResponses = results
      .filter((result) => result.status === "fulfilled")
      .map((result) => result.value);

    if (successfulResponses.length < 2) {
      throw new Error("Comparison needs at least 2 successful recommendation results.");
    }

    const rendered = renderComparisonSession(successfulResponses);
    if (!rendered) {
      throw new Error("Comparison results could not be rendered.");
    }

    const partialFailures = results.length - successfulResponses.length;
    comparisonStatus.textContent = partialFailures
      ? `Comparison ready with ${successfulResponses.length} destinations. ${partialFailures} request(s) failed.`
      : `Comparison ready. ${rendered.topEntry.destination} ranked first for this brief.`;

    saveHistoryEntry(
      buildHistoryEntry({
        mode: "comparison",
        destinations,
        topRankedDestination: rendered.topEntry.destination,
        averageScore: average(rendered.entries.map((entry) => entry.score)),
        form: {
          destinations,
          budget: sharedPayload.budget,
          currency: sharedPayload.currency,
          duration: sharedPayload.duration,
          travelStyle: sharedPayload.travelStyle,
          pace: sharedPayload.pace,
          interests: ensureArray(sharedPayload.interests).join(", ")
        },
        payloads: successfulResponses
      })
    );
    await refreshCounts();
  } catch (error) {
    const message = error.message || "Unable to compare the selected destinations.";
    setComparisonState("error", message);
    comparisonStatus.textContent = message;
  } finally {
    setButtonState(comparisonButton, false, "Comparing...", "Compare Destinations");
  }
}

async function handleReplanSubmit(event) {
  event.preventDefault();

  if (window.location.protocol === "file:") {
    replanStatus.textContent = "Start the Python server first so the AI copilot can replan through the local API.";
    return;
  }

  if (!currentRecommendationRequest) {
    replanStatus.textContent = "Generate a recommendation first so the AI copilot has a decision context to refine.";
    return;
  }

  const instruction = safeText(replanInstructionInput?.value, "");
  if (!instruction) {
    replanStatus.textContent = "Add a short follow-up instruction like 'make it cheaper' or 'make it safer'.";
    return;
  }

  setButtonState(replanButton, true, "Replanning...", "Run AI Replan");
  replanStatus.textContent = "The AI copilot is updating the trip brief and rerunning the decision engine...";

  try {
    const payloadResponse = await fetchJson("/api/replan", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json"
      },
      body: JSON.stringify({
        baseRequest: currentRecommendationRequest,
        instruction
      })
    });

    renderRecommendation({ recommendation: payloadResponse.replan.recommendation });
    replanStatus.textContent = payloadResponse.replan.assistantReply || "Replan ready.";
    recommendationStatus.textContent = `AI copilot updated the recommendation for ${payloadResponse.replan.updatedRequest.destination}.`;
    saveHistoryEntry(
      buildHistoryEntry({
        mode: "single",
        destinations: [payloadResponse.replan.updatedRequest.destination],
        topRankedDestination: payloadResponse.replan.updatedRequest.destination,
        averageScore: payloadResponse.replan.recommendation.decisionEngine?.decision_score || 0,
        form: {
          destination: payloadResponse.replan.updatedRequest.destination,
          budget: payloadResponse.replan.updatedRequest.budget,
          currency: normalizeCurrency(payloadResponse.replan.updatedRequest.currency || DEFAULT_CURRENCY),
          duration: payloadResponse.replan.updatedRequest.duration,
          travelStyle: payloadResponse.replan.updatedRequest.travelStyle,
          pace: payloadResponse.replan.updatedRequest.pace,
          interests: ensureArray(payloadResponse.replan.updatedRequest.interests).join(", ")
        },
        payload: { recommendation: payloadResponse.replan.recommendation }
      })
    );
    await refreshCounts();
  } catch (error) {
    replanStatus.textContent = error.message || "The AI copilot could not replan this request.";
  } finally {
    setButtonState(replanButton, false, "Replanning...", "Run AI Replan");
  }
}

function setActiveFeedbackVerdict(verdict) {
  if (!feedbackVerdictInput) {
    return;
  }

  feedbackVerdictInput.value = verdict;
  feedbackChips.forEach((chip) => {
    chip.classList.toggle("is-active", String(chip.dataset.feedbackVerdict || "") === verdict);
  });
}

async function handleFeedbackSubmit(event) {
  event.preventDefault();

  if (window.location.protocol === "file:") {
    feedbackStatus.textContent = "Start the Python server first so local calibration feedback can be saved.";
    return;
  }

  if (!currentRecommendationRequest) {
    feedbackStatus.textContent = "Generate a recommendation first so feedback can be attached to a real decision trace.";
    return;
  }

  const verdict = safeText(feedbackVerdictInput?.value, "accepted").toLowerCase();
  const rating = Number(feedbackRatingInput?.value || 3);
  const notes = safeText(feedbackNotesInput?.value, "");

  setButtonState(feedbackButton, true, "Saving...", "Save feedback");
  feedbackStatus.textContent = "Saving local calibration feedback...";

  try {
    const payloadResponse = await fetchJson("/api/feedback", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json"
      },
      body: JSON.stringify({
        destination: currentRecommendationRequest.destination,
        traceId: currentRecommendationRequest.traceId,
        verdict,
        rating,
        notes,
        requestPayload: {
          destination: currentRecommendationRequest.destination,
          budget: currentRecommendationRequest.budget,
          currency: currentRecommendationRequest.currency,
          duration: currentRecommendationRequest.duration,
          interests: ensureArray(currentRecommendationRequest.interests),
          travelStyle: currentRecommendationRequest.travelStyle,
          pace: currentRecommendationRequest.pace
        }
      })
    });
    const summary = payloadResponse.feedbackSummary || {};
    const learningRefresh = payloadResponse.learningRefresh || {};
    const refreshNote = learningRefresh.feedbackTrainable
      ? ` Live model refreshed with ${learningRefresh.feedbackSamples || 0} feedback sample(s).`
      : " Feedback saved, but this event was not trainable yet.";
    feedbackStatus.textContent = `Feedback saved. ${summary.sampleCount || 0} local sample(s) for ${currentRecommendationRequest.destination}; acceptance prior ${Math.round(Number(summary.acceptanceRate || 0) * 100)}%.${refreshNote}`;
  } catch (error) {
    feedbackStatus.textContent = error.message || "Unable to save feedback right now.";
  } finally {
    setButtonState(feedbackButton, false, "Saving...", "Save feedback");
  }
}

async function handleDemoSubmit(event) {
  event.preventDefault();

  if (window.location.protocol === "file:") {
    demoFormStatus.textContent = "Start the Python server first so demo requests can be submitted.";
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

  setButtonState(demoSubmitButton, true, "Submitting...", "Submit Demo Request");
  demoFormStatus.textContent = "Submitting demo request...";

  try {
    const result = await fetchJson("/api/demo-request", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json"
      },
      body: JSON.stringify(payload)
    });
    demoForm.reset();
    demoFormStatus.textContent = `Demo request saved with id ${result.requestId}.`;
    await refreshCounts();
  } catch (error) {
    demoFormStatus.textContent = error.message || "Unable to submit demo request.";
  } finally {
    setButtonState(demoSubmitButton, false, "Submitting...", "Submit Demo Request");
  }
}

quickChips.forEach((chip) => {
  chip.addEventListener("click", () => {
    destinationInput.value = chip.dataset.destination || "";
    destinationInput.focus();
  });
});

heroSuggestions.forEach((chip) => {
  chip.addEventListener("click", () => {
    if (!heroPromptDestination) {
      return;
    }

    heroPromptDestination.value = chip.dataset.heroDestination || "";
    heroPromptDestination.focus();
  });
});

compareChips.forEach((chip) => {
  chip.addEventListener("click", () => {
    const destination = normalizeDestinationName(chip.dataset.compareDestination || "");
    const current = parseDestinationList(comparisonDestinationsInput.value);
    const exists = current.some((item) => item.toLowerCase() === destination.toLowerCase());
    const nextDestinations = exists
      ? current.filter((item) => item.toLowerCase() !== destination.toLowerCase())
      : [...current, destination].slice(0, 4);

    comparisonDestinationsInput.value = nextDestinations.join(", ");
    syncCompareChips();
    comparisonDestinationsInput.focus();
  });
});

replanChips.forEach((chip) => {
  chip.addEventListener("click", () => {
    if (!replanInstructionInput) {
      return;
    }

    replanInstructionInput.value = chip.dataset.replanInstruction || "";
    replanInstructionInput.focus();
  });
});

feedbackChips.forEach((chip) => {
  chip.addEventListener("click", () => {
    setActiveFeedbackVerdict(String(chip.dataset.feedbackVerdict || "accepted"));
  });
});

comparisonDestinationsInput.addEventListener("input", syncCompareChips);
clearHistoryButton.addEventListener("click", () => {
  historyEntries = [];
  persistHistory();
  renderHistoryList();
});

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.14 }
);

const navObserver = new IntersectionObserver(
  (entries) => {
    const activeEntry = entries
      .filter((entry) => entry.isIntersecting)
      .sort((left, right) => right.intersectionRatio - left.intersectionRatio)[0];

    if (activeEntry?.target?.id) {
      setActiveNavLink(activeEntry.target.id);
    }
  },
  {
    rootMargin: "-30% 0px -55% 0px",
    threshold: [0.12, 0.3, 0.55]
  }
);

function initializeClientApp() {
  if (resultsShell) {
    setResultsState("empty");
  }
  if (comparisonShell) {
    setComparisonState("empty");
  }

  document.querySelectorAll(".reveal").forEach((element) => observer.observe(element));
  navLinks.forEach((link) => {
    const id = String(link.getAttribute("href") || "").replace("#", "");
    const section = document.getElementById(id);
    if (section) {
      navObserver.observe(section);
    }
  });
  if (heroPromptForm) {
    heroPromptForm.addEventListener("submit", handleHeroPromptSubmit);
  }
  if (recommendationForm) {
    recommendationForm.addEventListener("submit", handleRecommendationSubmit);
  }
  if (comparisonForm) {
    comparisonForm.addEventListener("submit", handleComparisonSubmit);
  }
  if (replanForm) {
    replanForm.addEventListener("submit", handleReplanSubmit);
  }
  if (feedbackForm) {
    feedbackForm.addEventListener("submit", handleFeedbackSubmit);
  }
  if (demoForm) {
    demoForm.addEventListener("submit", handleDemoSubmit);
  }

  renderHistoryList();
  syncCompareChips();
  setActiveNavLink("how-it-works");
  checkBackendHealth();
  refreshCounts();
  refreshEvaluationSnapshot();
  setActiveFeedbackVerdict("accepted");
}

try {
  initializeClientApp();
} catch (error) {
  console.error("MindGrid Voyager client initialization failed.", error);
  if (resultsShell) {
    setResultsState("empty");
  }
  if (recommendationStatus) {
    recommendationStatus.textContent = "Live results are available, but part of the interface initialization failed. Refresh once to retry.";
  }
}
