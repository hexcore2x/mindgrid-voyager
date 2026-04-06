from __future__ import annotations

from copy import deepcopy
from typing import Any


BALI_SEED: dict[str, Any] = {
    "destination": "Bali",
    "summary": "Bali blends wellness escapes, design-forward cafes, surf energy, beach clubs, temple landscapes, and slower lifestyle travel into one high-memory destination.",
    "whyNow": "Bali performs especially well for travelers who want a high emotional payoff, strong cafe culture, and a mix of calm and social energy without overcomplicated routing.",
    "bestTime": "April to October",
    "seasonNote": "Dry-season months make coastal movement, waterfall routes, and sunset plans much more reliable.",
    "riskLevel": "Low risk with scooter and late-night awareness",
    "safetyConfidence": 87,
    "transportNote": "Private drivers work best for multi-stop days; avoid overloading the itinerary with long cross-island transfers.",
    "safetyNotes": [
        "Scooter-heavy zones demand extra road awareness, especially after sunset.",
        "Plan beach club or cliffside evenings with a known return route.",
        "Rain can materially slow inland travel during wetter months.",
    ],
    "signals": ["cafe density", "wellness travel", "sunset coastline", "creative hotspots"],
    "tips": [
        "Keep one district focus per day because transfers add up quickly.",
        "Use sunrise or sunset moments as the emotional anchors of the trip.",
        "Mix one polished cafe block with one nature or temple block for stronger pacing.",
    ],
    "scoreInputs": {
        "destinationIntelligence": 90,
        "budgetFit": 88,
        "localSignal": 91,
        "safetyConfidence": 87,
    },
    "budgetIndicators": {
        "valueWindow": "$95-$180/day",
        "saverMove": "Base around one zone and use curated cafe + warung mixes.",
        "splurgeMoment": "Use premium spend on one sunset dinner or private driver day.",
    },
    "socialSignals": [
        "Sunset cliff clubs keep Bali highly visible in social discovery loops.",
        "Canggu and Ubud cafes show strong repeat-creator and digital-nomad signal.",
        "Villa and wellness content keeps premium travel demand unusually resilient.",
    ],
    "bestFor": ["Wellness reset", "Cafe exploration", "Scenic escape"],
    "styleIndicators": ["Wellness-led", "Cafe-first", "Scenic pace", "Lifestyle travel"],
    "explanationSummary": "Bali ranks highly when the traveler wants scenic pace, cafe discovery, and premium-feeling memories without a fully luxury-only budget.",
    "itineraryHints": [
        "Pair Ubud culture with a relaxed afternoon cafe block.",
        "Keep one sunset coastline evening for the emotional peak.",
        "Use a dedicated driver day for waterfalls, rice terraces, or temple clusters.",
    ],
    "attractions": [
        {
            "name": "Ubud terraces and temple circuit",
            "why": "Best for cultural texture, slower pacing, and classic Bali visual identity.",
            "tags": ["culture", "nature", "relaxed", "scenic"],
            "bestTime": "Morning",
            "estimatedCost": 16,
            "budgetBand": "budget",
            "theme": "Temple calm and inland texture",
        },
        {
            "name": "Uluwatu cliffs and sunset route",
            "why": "A high-memory evening arc with strong scenic payoff.",
            "tags": ["scenic", "high-energy", "iconic", "mid"],
            "bestTime": "Sunset",
            "estimatedCost": 24,
            "budgetBand": "mid",
        },
        {
            "name": "Seminyak design and beach corridor",
            "why": "Combines polished shopping, cafes, and easy beach-adjacent movement.",
            "tags": ["design", "shopping", "balanced", "mid"],
            "bestTime": "Afternoon",
            "estimatedCost": 20,
            "budgetBand": "mid",
        },
    ],
    "food": [
        {
            "name": "Canggu specialty cafe run",
            "why": "High-density cafe discovery with strong design and social signal.",
            "tags": ["coffee", "design", "local", "mid"],
            "bestTime": "Breakfast",
            "estimatedCost": 16,
            "budgetBand": "mid",
        },
        {
            "name": "Warung lunch with local seafood or nasi campur",
            "why": "Strong local value and better everyday food signal than polished resort dining.",
            "tags": ["food", "local", "budget"],
            "bestTime": "Lunch",
            "estimatedCost": 14,
            "budgetBand": "budget",
        },
        {
            "name": "Cliffside or beach-view dinner",
            "why": "One premium sunset dinner can define the emotional memory of the trip.",
            "tags": ["food", "premium", "scenic"],
            "bestTime": "Dinner",
            "estimatedCost": 68,
            "budgetBand": "premium",
        },
    ],
    "favorites": [
        {
            "name": "Pererenan village cafe pocket",
            "why": "A softer alternative to busier Bali zones with strong coffee and local texture.",
            "tags": ["coffee", "relaxed", "local"],
            "bestTime": "Late morning",
            "estimatedCost": 12,
            "budgetBand": "budget",
        },
        {
            "name": "Ubud artisan and design stores",
            "why": "Adds locally rooted design browsing without hard scheduling.",
            "tags": ["design", "shopping", "balanced"],
            "bestTime": "Afternoon",
            "estimatedCost": 18,
            "budgetBand": "mid",
        },
        {
            "name": "Quiet beach sunrise window",
            "why": "A slower, reflective moment that makes the trip feel more personal.",
            "tags": ["nature", "scenic", "relaxed"],
            "bestTime": "Sunrise",
            "estimatedCost": 8,
            "budgetBand": "budget",
        },
    ],
}


DESTINATION_DEMO_INTELLIGENCE: dict[str, dict[str, Any]] = {
    "bangkok": {
        "scoreInputs": {
            "destinationIntelligence": 92,
            "budgetFit": 91,
            "localSignal": 93,
            "safetyConfidence": 83,
        },
        "signals": ["street food density", "local neighborhoods", "night markets", "budget efficiency"],
        "budgetIndicators": {
            "valueWindow": "$85-$165/day",
            "saverMove": "Use BTS and market-led meals for the strongest value density.",
            "splurgeMoment": "One riverside dinner or rooftop close creates premium contrast.",
        },
        "socialSignals": [
            "Night markets and Chinatown dining keep Bangkok highly visible in food-first travel feeds.",
            "Ari and Talad Noi show strong creator interest beyond the classic icon circuit.",
            "Rooftop and river content consistently boosts premium-experience demand.",
        ],
        "bestFor": ["Food exploration", "Nightlife", "Budget trip"],
        "styleIndicators": ["Food-first", "High-energy", "Local texture", "Urban contrast"],
        "explanationSummary": "Bangkok ranks well for travelers who want variety, food density, and strong value without losing premium memory moments.",
        "itineraryHints": [
            "Keep temple blocks early before the heat curve rises.",
            "Use one market or creative district in the afternoon.",
            "Anchor evenings around riverside, Chinatown, or rooftop arcs.",
        ],
    },
    "tokyo": {
        "scoreInputs": {
            "destinationIntelligence": 94,
            "budgetFit": 87,
            "localSignal": 92,
            "safetyConfidence": 95,
        },
        "budgetIndicators": {
            "valueWindow": "$150-$290/day",
            "saverMove": "Cluster neighborhoods and use depachika or cafe-led lunches.",
            "splurgeMoment": "Reserve one omakase or immersive art experience early.",
        },
        "socialSignals": [
            "Design-led neighborhoods keep Tokyo strong across premium lifestyle content.",
            "Cafe, retail, and omakase culture create consistent repeat-visitor signal.",
            "Tokyo benefits from very high trust in logistics and everyday quality.",
        ],
        "bestFor": ["Safety-first", "Solo travel", "Design-aware trip"],
        "styleIndicators": ["Precision logistics", "Design-aware", "Food depth"],
        "explanationSummary": "Tokyo ranks highest for travelers seeking world-class food, reliable logistics, and layered neighborhood discovery with low friction.",
        "itineraryHints": [
            "Use neighborhoods as day themes instead of crossing the city repeatedly.",
            "Combine shrine, retail, and cafe blocks to keep transitions light.",
            "Leave evenings for atmosphere-heavy districts like Nakameguro or Shinjuku.",
        ],
    },
    "dubai": {
        "scoreInputs": {
            "destinationIntelligence": 89,
            "budgetFit": 85,
            "localSignal": 84,
            "safetyConfidence": 91,
        },
        "budgetIndicators": {
            "valueWindow": "$170-$340/day",
            "saverMove": "Base around metro-linked districts and limit long taxi-heavy routing.",
            "splurgeMoment": "Use premium spend on skyline, desert, or dinner-view experiences.",
        },
        "socialSignals": [
            "Skyline and hospitality visuals give Dubai unusually strong premium social pull.",
            "Desert content and architecture keep the destination highly memorable online.",
            "Luxury food and hotel ecosystems raise expectation for polished execution.",
        ],
        "bestFor": ["Premium stay", "Iconic city break", "Luxury comfort"],
        "styleIndicators": ["Premium comfort", "Icon-first", "Climate-aware"],
        "explanationSummary": "Dubai ranks strongly when the traveler values comfort, visual polish, and premium infrastructure more than deep walkable city texture.",
        "itineraryHints": [
            "Use indoor or observation anchors during the hottest part of the day.",
            "Pair heritage zones with evening skyline districts.",
            "Keep one planned desert or waterfront moment for memory value.",
        ],
    },
    "singapore": {
        "scoreInputs": {
            "destinationIntelligence": 93,
            "budgetFit": 84,
            "localSignal": 90,
            "safetyConfidence": 96,
        },
        "budgetIndicators": {
            "valueWindow": "$160-$280/day",
            "saverMove": "Use hawker meals and MRT routing to balance a premium city with smart spend.",
            "splurgeMoment": "One skyline or bayfront dinner is usually enough for the premium hit.",
        },
        "socialSignals": [
            "Food-led content and clean urban visuals keep Singapore highly trusted in recommendation loops.",
            "Neighborhoods like Tiong Bahru and Joo Chiat show stronger local-lifestyle signal than the icon layer alone.",
            "High safety and efficiency reinforce premium product-fit for planners.",
        ],
        "bestFor": ["Safety-first", "Food exploration", "Short city break"],
        "styleIndicators": ["High-trust", "Food-led", "Efficient city break"],
        "explanationSummary": "Singapore ranks especially well for travelers who want strong food discovery, clean logistics, and a polished city experience with very low risk.",
        "itineraryHints": [
            "Use hawker centers as strategic food anchors instead of just snack stops.",
            "Pair one icon district with one neighborhood district each day.",
            "Keep evenings for waterfront, gardens, or softer quay-side walks.",
        ],
    },
    "paris": {
        "scoreInputs": {
            "destinationIntelligence": 91,
            "budgetFit": 82,
            "localSignal": 89,
            "safetyConfidence": 84,
        },
        "budgetIndicators": {
            "valueWindow": "$180-$320/day",
            "saverMove": "Cluster districts and use boulangerie or market-led lunch stops.",
            "splurgeMoment": "Choose one standout museum or bistro night rather than overspending daily.",
        },
        "socialSignals": [
            "Cafe culture, river walks, and district identity keep Paris emotionally sticky in travel content.",
            "Le Marais and Canal Saint-Martin show stronger local repeat-visitor signal than only icon chasing.",
            "Paris performs best when paced intentionally, not aggressively.",
        ],
        "bestFor": ["Culture-led escape", "Cafe ritual trip", "Walkable districts"],
        "styleIndicators": ["Atmosphere-first", "Culture-led", "Walkable districts"],
        "explanationSummary": "Paris ranks highly when the traveler cares about atmosphere, culture, cafe rituals, and the emotional texture of a city rather than pure efficiency.",
        "itineraryHints": [
            "Assign each day to one district family to preserve rhythm.",
            "Use river walks to connect major icons without overpacking.",
            "Balance museums with quieter neighborhood routes for a stronger trip memory.",
        ],
    },
    "bali": {
        "scoreInputs": {
            "destinationIntelligence": 90,
            "budgetFit": 88,
            "localSignal": 91,
            "safetyConfidence": 87,
        },
        "budgetIndicators": {
            "valueWindow": "$95-$180/day",
            "saverMove": "Stay district-focused and mix premium cafes with strong local warungs.",
            "splurgeMoment": "One sunset cliff dinner or private-driver day creates high payoff.",
        },
        "socialSignals": [
            "Canggu and Ubud lifestyle content keeps Bali highly visible in social travel feeds.",
            "Sunset clubs, villas, and wellness trips create strong premium aspiration signal.",
            "Bali works best when routed by zone instead of trying to cover everything at once.",
        ],
        "bestFor": ["Wellness reset", "Scenic escape", "Lifestyle travel"],
        "styleIndicators": ["Wellness-led", "Scenic pace", "Lifestyle travel"],
        "explanationSummary": "Bali scores especially well for cafe discovery, scenic pacing, and travelers who want a softer, memory-driven trip with strong social proof.",
        "itineraryHints": [
            "Pair one inland culture block with one coastline or sunset block.",
            "Avoid cross-island hops inside the same day when possible.",
            "Use sunrise or sunset as the emotional center of the itinerary.",
        ],
    },
    "goa": {
        "bestFor": ["Beach reset", "Nightlife", "Lifestyle trip"],
        "budgetIndicators": {
            "valueWindow": "$80-$170/day",
            "saverMove": "Commit to one north or south cluster per day and let the route breathe.",
            "splurgeMoment": "Use premium spend on one sunset dinner or standout beach stay.",
        },
        "socialSignals": [
            "Goa stays strong in beach-and-cafe travel feeds because it blends relaxed days with social evenings.",
            "Assagao and Mandrem create stronger lifestyle and cafe signal than generic party-only framing.",
            "North-versus-south tradeoffs make Goa comparison-friendly inside the decision engine.",
        ],
        "styleIndicators": ["Beach pace", "Lifestyle-led", "Social evenings"],
        "explanationSummary": "Goa ranks well when the traveler wants a relaxed coastal trip with nightlife optionality, cafe culture, and strong memory moments at lower overall complexity.",
        "itineraryHints": [
            "Protect sunset windows because they drive the strongest emotional payoff.",
            "Do not mix far north and far south blocks inside the same day.",
            "Use one beach block and one food-or-night block per day for balance.",
        ],
    },
}


def merge_destination_demo_intelligence(seed_data: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    enriched = deepcopy(seed_data)
    enriched.setdefault("bali", deepcopy(BALI_SEED))

    for slug, extras in DESTINATION_DEMO_INTELLIGENCE.items():
        if slug not in enriched:
            continue
        enriched[slug] = {
            **deepcopy(enriched[slug]),
            **deepcopy(extras),
        }

    return enriched
