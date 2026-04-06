from __future__ import annotations

from dataclasses import dataclass
from math import floor
from typing import Any

from .demo_intelligence import merge_destination_demo_intelligence
from .itinerary_planner import ItineraryPlanner
from .prioritization_engine import PrioritizationEngine
from .risk_analyzer import RiskAnalyzer
from .source_discovery import SourceDiscovery
from .social_signal_engine import SocialSignalEngine


@dataclass(slots=True)
class RecommendationInput:
    destination: str
    budget: int
    currency: str
    duration: int
    interests: list[str]
    travel_style: str
    pace: str


FALLBACK_PROFILE: dict[str, Any] = {
    "destination": "Custom Journey",
    "summary": "A flexible city-break profile generated from global travel heuristics.",
    "whyNow": "This destination is handled by the fallback intelligence path, so the plan leans on universal city-exploration patterns.",
    "bestTime": "Aim for shoulder season if possible",
    "seasonNote": "Shoulder months usually balance better weather, lighter crowds, and stronger value.",
    "riskLevel": "Moderate awareness",
    "safetyConfidence": 76,
    "transportNote": "Save one anchor route offline and keep an easy return option after dark.",
    "safetyNotes": [
        "Choose busy, well-lit corridors for late-evening movement.",
        "Keep one cached map and one known return point each day.",
        "Use reservation-backed dining if the area is unfamiliar.",
    ],
    "signals": ["maps", "budget heuristics", "urban walkability", "local pattern fallback"],
    "tips": [
        "Start with one high-signal district instead of spreading the day too thin.",
        "Anchor lunch near the main attraction cluster to reduce transit churn.",
        "Keep one flexible slot for weather or queue changes.",
    ],
    "scoreInputs": {
        "destinationIntelligence": 74,
        "budgetFit": 78,
        "localSignal": 72,
        "safetyConfidence": 76,
    },
    "budgetIndicators": {
        "valueWindow": "$90-$180/day",
        "saverMove": "Stay district-focused and protect walkability.",
        "splurgeMoment": "Use premium spend on one standout dinner or viewpoint.",
    },
    "socialSignals": [
        "Fallback mode relies on general city-break heuristics instead of destination-specific social proof.",
    ],
    "styleIndicators": ["Flexible", "Budget-aware", "Walkable clusters"],
    "explanationSummary": "Fallback intelligence favors practical routing, adaptable neighborhoods, and lower-risk planning patterns.",
    "itineraryHints": [
        "Open with one orientation block.",
        "Keep one weather-flexible slot each day.",
        "End near a known return route.",
    ],
    "attractions": [
        {
            "name": "Historic core walk",
            "why": "Good first-day orientation with low planning risk.",
            "tags": ["culture", "walkable", "budget"],
            "bestTime": "Morning",
            "estimatedCost": 0,
            "budgetBand": "budget",
            "theme": "Orientation and city rhythm",
        },
        {
            "name": "Flagship museum or gallery",
            "why": "Reliable cultural depth and weather-proof planning anchor.",
            "tags": ["culture", "art", "rainy-day", "mid"],
            "bestTime": "Afternoon",
            "estimatedCost": 22,
            "budgetBand": "mid",
        },
        {
            "name": "Signature viewpoint",
            "why": "Creates a memorable sense of place without overcomplicating the route.",
            "tags": ["scenic", "relaxed", "budget"],
            "bestTime": "Sunset",
            "estimatedCost": 12,
            "budgetBand": "budget",
        },
    ],
    "food": [
        {
            "name": "Neighborhood cafe",
            "why": "Useful for local rhythm, easy observation, and low-friction starts.",
            "tags": ["coffee", "relaxed", "budget"],
            "bestTime": "Breakfast",
            "estimatedCost": 10,
            "budgetBand": "budget",
        },
        {
            "name": "Market lunch hall",
            "why": "Great for variety and strong local signal without committing to a long meal.",
            "tags": ["food", "market", "budget"],
            "bestTime": "Lunch",
            "estimatedCost": 18,
            "budgetBand": "budget",
        },
        {
            "name": "Chef-led dinner room",
            "why": "Adds one premium memory point if budget allows.",
            "tags": ["food", "premium", "high-energy"],
            "bestTime": "Dinner",
            "estimatedCost": 48,
            "budgetBand": "premium",
        },
    ],
    "favorites": [
        {
            "name": "Local bookshop cafe",
            "why": "Quiet but culturally rich stop that works for most travel styles.",
            "tags": ["culture", "coffee", "relaxed"],
            "bestTime": "Late morning",
            "estimatedCost": 12,
            "budgetBand": "budget",
        },
        {
            "name": "Independent design street",
            "why": "A good local-texture block for spontaneous wandering.",
            "tags": ["shopping", "walkable", "balanced"],
            "bestTime": "Afternoon",
            "estimatedCost": 16,
            "budgetBand": "mid",
        },
        {
            "name": "Evening food lane",
            "why": "Clusters energy, food discovery, and low-effort movement into one zone.",
            "tags": ["food", "high-energy", "mid"],
            "bestTime": "Evening",
            "estimatedCost": 28,
            "budgetBand": "mid",
        },
    ],
}


DESTINATION_SEEDS: dict[str, dict[str, Any]] = {
    "bangkok": {
        "destination": "Bangkok",
        "summary": "Bangkok blends temple heritage, hyper-local food culture, luxury pockets, and late-night energy in a city that rewards confident, neighborhood-first planning.",
        "whyNow": "Bangkok works especially well for travelers seeking strong food discovery, high variety, and a favorable value curve across every budget tier.",
        "bestTime": "November to February",
        "seasonNote": "Cooler months make daytime movement easier and keep riverside and market exploration more comfortable.",
        "riskLevel": "Urban vigilance recommended",
        "safetyConfidence": 83,
        "transportNote": "Use BTS or river transit for predictable daytime movement and ride-share for late-night returns.",
        "safetyNotes": [
            "Watch traffic intensity when crossing major roads.",
            "Use metered or app-booked transport after late dinners.",
            "Hydrate aggressively during hotter months.",
        ],
        "signals": ["street food density", "night markets", "temple access", "budget efficiency"],
        "tips": [
            "Keep temples earlier in the day to avoid heat spikes.",
            "Cluster rooftop or river moments in the evening.",
            "Budget travelers get excellent value by mixing markets with one signature dinner.",
        ],
        "attractions": [
            {
                "name": "Grand Palace and Wat Phra Kaew",
                "why": "High-impact cultural anchor with dense historical storytelling.",
                "tags": ["culture", "history", "iconic", "mid"],
                "bestTime": "Early morning",
                "estimatedCost": 18,
                "budgetBand": "mid",
                "theme": "Royal heritage and temple architecture",
            },
            {
                "name": "Wat Arun riverside circuit",
                "why": "One of the most photogenic and spatially rewarding river experiences in the city.",
                "tags": ["culture", "scenic", "walkable", "budget"],
                "bestTime": "Late afternoon",
                "estimatedCost": 10,
                "budgetBand": "budget",
            },
            {
                "name": "Talad Noi creative quarter",
                "why": "Blends old Bangkok texture with galleries, murals, and cafe pockets.",
                "tags": ["art", "local", "walkable", "relaxed"],
                "bestTime": "Afternoon",
                "estimatedCost": 8,
                "budgetBand": "budget",
            },
        ],
        "food": [
            {
                "name": "Chinatown late-night street food crawl",
                "why": "Top-tier density for serious flavor discovery with strong social energy.",
                "tags": ["food", "high-energy", "market", "budget"],
                "bestTime": "Dinner",
                "estimatedCost": 24,
                "budgetBand": "budget",
            },
            {
                "name": "Ari specialty cafe run",
                "why": "Strong coffee scene with calmer pacing and polished local taste.",
                "tags": ["coffee", "relaxed", "design", "mid"],
                "bestTime": "Morning",
                "estimatedCost": 14,
                "budgetBand": "mid",
            },
            {
                "name": "Riverside Thai tasting menu",
                "why": "A premium way to experience polished local cuisine with atmosphere.",
                "tags": ["food", "premium", "scenic"],
                "bestTime": "Dinner",
                "estimatedCost": 76,
                "budgetBand": "premium",
            },
        ],
        "favorites": [
            {
                "name": "Bang Rak side-street eateries",
                "why": "Excellent local value and repeat-resident food signal.",
                "tags": ["food", "local", "budget"],
                "bestTime": "Lunch",
                "estimatedCost": 16,
                "budgetBand": "budget",
            },
            {
                "name": "Warehouse 30 creative cluster",
                "why": "Useful for design-minded travelers who want slower neighborhood texture.",
                "tags": ["art", "design", "relaxed"],
                "bestTime": "Afternoon",
                "estimatedCost": 12,
                "budgetBand": "mid",
            },
            {
                "name": "Suan Luang weekend community market",
                "why": "A less tourist-heavy option for browsing, snacks, and local atmosphere.",
                "tags": ["market", "local", "budget"],
                "bestTime": "Weekend afternoon",
                "estimatedCost": 10,
                "budgetBand": "budget",
            },
        ],
    },
    "tokyo": {
        "destination": "Tokyo",
        "summary": "Tokyo offers extraordinary precision: world-class food, hyper-efficient mobility, layered neighborhoods, and enough variety to reward both structure and serendipity.",
        "whyNow": "Tokyo is ideal for travelers who want clean logistics, deep local discovery, and a premium-feeling experience at many spending levels.",
        "bestTime": "March to May and October to November",
        "seasonNote": "Spring and autumn balance comfortable weather, walkability, and strong neighborhood energy.",
        "riskLevel": "Low risk with urban awareness",
        "safetyConfidence": 95,
        "transportNote": "Rail is the planning backbone; keep one IC card and one backup route for busy hubs.",
        "safetyNotes": [
            "Expect rush-hour density around major interchange stations.",
            "Cashless payment is common, but carry a small backup cash reserve.",
            "Late-night trains taper, so plan the final leg home in advance.",
        ],
        "signals": ["rail efficiency", "micro-neighborhoods", "food depth", "seasonal culture"],
        "tips": [
            "Use neighborhoods as themes rather than trying to cover the whole city each day.",
            "Reserve one omakase or premium meal early if that matters to the trip.",
            "Pair shrines, retail, and cafes in the same district for low-friction days.",
        ],
        "attractions": [
            {
                "name": "Asakusa and Senso-ji",
                "why": "Strong traditional atmosphere with clear first-visit orientation value.",
                "tags": ["culture", "history", "iconic", "walkable"],
                "bestTime": "Morning",
                "estimatedCost": 6,
                "budgetBand": "budget",
                "theme": "Heritage streets and temple ritual",
            },
            {
                "name": "Shibuya and Harajuku design axis",
                "why": "Best for fashion, youth culture, and modern Tokyo energy in one connected area.",
                "tags": ["shopping", "high-energy", "design", "mid"],
                "bestTime": "Afternoon",
                "estimatedCost": 18,
                "budgetBand": "mid",
            },
            {
                "name": "teamLab and waterfront district",
                "why": "Good for immersive tech-forward experiences and evening visuals.",
                "tags": ["art", "technology", "scenic", "premium"],
                "bestTime": "Late afternoon",
                "estimatedCost": 30,
                "budgetBand": "premium",
            },
        ],
        "food": [
            {
                "name": "Kissaten breakfast and coffee stop",
                "why": "Delivers classic Tokyo atmosphere with calm pacing.",
                "tags": ["coffee", "culture", "relaxed", "budget"],
                "bestTime": "Breakfast",
                "estimatedCost": 12,
                "budgetBand": "budget",
            },
            {
                "name": "Depachika lunch circuit",
                "why": "Efficient way to sample quality without overcommitting time or spend.",
                "tags": ["food", "market", "mid"],
                "bestTime": "Lunch",
                "estimatedCost": 20,
                "budgetBand": "mid",
            },
            {
                "name": "Shinjuku omakase or izakaya corridor",
                "why": "High-value contrast between polished premium dining and buzzy casual options.",
                "tags": ["food", "high-energy", "premium"],
                "bestTime": "Dinner",
                "estimatedCost": 68,
                "budgetBand": "premium",
            },
        ],
        "favorites": [
            {
                "name": "Yanaka backstreets",
                "why": "Old Tokyo texture with lower friction and quieter local rhythm.",
                "tags": ["culture", "walkable", "relaxed"],
                "bestTime": "Late morning",
                "estimatedCost": 8,
                "budgetBand": "budget",
            },
            {
                "name": "Kiyosumi-Shirakawa cafe pockets",
                "why": "Excellent coffee signal and slower neighborhood cadence.",
                "tags": ["coffee", "design", "relaxed"],
                "bestTime": "Afternoon",
                "estimatedCost": 14,
                "budgetBand": "mid",
            },
            {
                "name": "Nakameguro evening walk",
                "why": "One of the strongest atmosphere-driven local strolls in the city.",
                "tags": ["scenic", "local", "balanced"],
                "bestTime": "Evening",
                "estimatedCost": 16,
                "budgetBand": "mid",
            },
        ],
    },
    "dubai": {
        "destination": "Dubai",
        "summary": "Dubai combines luxury hospitality, polished infrastructure, international dining, and high-contrast neighborhoods into a destination that rewards intentional routing.",
        "whyNow": "Dubai is particularly strong for premium comfort, iconic architecture, and climate-controlled planning during warmer periods.",
        "bestTime": "November to March",
        "seasonNote": "Cooler months unlock outdoor promenades, desert experiences, and evening city views more comfortably.",
        "riskLevel": "Low risk with climate awareness",
        "safetyConfidence": 91,
        "transportNote": "Metro is efficient for major corridors, but app rides are often the best final-mile option.",
        "safetyNotes": [
            "Heat management matters for daytime outdoor segments.",
            "Book desert or rooftop experiences ahead during peak season.",
            "Modest dress is smart for cultural sites and government-adjacent venues.",
        ],
        "signals": ["luxury hospitality", "iconic skyline", "retail", "desert excursions"],
        "tips": [
            "Use indoor and observation experiences midday, then move outdoors in the evening.",
            "Pair Old Dubai with a creek or souk route for more texture.",
            "Budget travelers should concentrate around metro-connected districts.",
        ],
        "attractions": [
            {
                "name": "Burj Khalifa and Downtown Dubai",
                "why": "Essential skyline context with strong first-visit orientation.",
                "tags": ["iconic", "scenic", "premium"],
                "bestTime": "Sunset",
                "estimatedCost": 46,
                "budgetBand": "premium",
                "theme": "Skyline spectacle and flagship city icons",
            },
            {
                "name": "Al Fahidi Historical District",
                "why": "Adds cultural contrast and heritage depth to a modern-city itinerary.",
                "tags": ["culture", "history", "walkable", "budget"],
                "bestTime": "Morning",
                "estimatedCost": 10,
                "budgetBand": "budget",
            },
            {
                "name": "Dubai Marina and Bluewaters",
                "why": "High visual polish with an easy evening promenade pattern.",
                "tags": ["scenic", "high-energy", "mid"],
                "bestTime": "Evening",
                "estimatedCost": 18,
                "budgetBand": "mid",
            },
        ],
        "food": [
            {
                "name": "Jumeirah beach cafe circuit",
                "why": "Strong blend of design, coffee, and relaxed daytime energy.",
                "tags": ["coffee", "design", "mid"],
                "bestTime": "Morning",
                "estimatedCost": 18,
                "budgetBand": "mid",
            },
            {
                "name": "Global food hall in Downtown",
                "why": "Practical for variety and mixed budgets in one polished environment.",
                "tags": ["food", "market", "mid"],
                "bestTime": "Lunch",
                "estimatedCost": 24,
                "budgetBand": "mid",
            },
            {
                "name": "Desert-view fine dining",
                "why": "Creates a high-end signature memory point if the trip budget supports it.",
                "tags": ["food", "premium", "scenic"],
                "bestTime": "Dinner",
                "estimatedCost": 94,
                "budgetBand": "premium",
            },
        ],
        "favorites": [
            {
                "name": "Al Seef creekside stroll",
                "why": "Easy local-feeling route with heritage styling and soft evening energy.",
                "tags": ["scenic", "culture", "relaxed"],
                "bestTime": "Evening",
                "estimatedCost": 12,
                "budgetBand": "budget",
            },
            {
                "name": "Alserkal Avenue",
                "why": "Best for contemporary art and creative-industry atmosphere.",
                "tags": ["art", "design", "local"],
                "bestTime": "Afternoon",
                "estimatedCost": 14,
                "budgetBand": "mid",
            },
            {
                "name": "Satwa food strip",
                "why": "Excellent local-value dining and a less polished but more lived-in feel.",
                "tags": ["food", "local", "budget"],
                "bestTime": "Dinner",
                "estimatedCost": 16,
                "budgetBand": "budget",
            },
        ],
    },
    "singapore": {
        "destination": "Singapore",
        "summary": "Singapore is a high-trust, high-efficiency city for food, gardens, architecture, and premium urban comfort with remarkably low planning friction.",
        "whyNow": "Singapore suits travelers who want clean logistics, excellent food diversity, and a polished city experience that still leaves room for neighborhood nuance.",
        "bestTime": "February to April",
        "seasonNote": "These months often bring slightly more favorable weather for longer walking days and waterfront evenings.",
        "riskLevel": "Low risk",
        "safetyConfidence": 96,
        "transportNote": "MRT handles most routes cleanly; walking the final segment often adds the best city texture.",
        "safetyNotes": [
            "Humidity can slow long walking routes, so plan cool-down stops.",
            "Carry light rain protection because weather can shift quickly.",
            "Reserve marquee rooftop or tasting experiences ahead.",
        ],
        "signals": ["hawker culture", "urban gardens", "clean transit", "premium city comfort"],
        "tips": [
            "Mix one green-space block into each day to keep the trip breathable.",
            "Use hawker centers for maximum value and culinary variety.",
            "Night views are strongest when paired with the bayfront district.",
        ],
        "attractions": [
            {
                "name": "Gardens by the Bay",
                "why": "A flagship experience that captures Singapore's futuristic civic identity.",
                "tags": ["scenic", "technology", "iconic", "mid"],
                "bestTime": "Late afternoon",
                "estimatedCost": 24,
                "budgetBand": "mid",
                "theme": "Future-city nature and skyline drama",
            },
            {
                "name": "Kampong Glam and Haji Lane",
                "why": "Best for boutique streets, design energy, and easy cafe pairing.",
                "tags": ["design", "shopping", "walkable", "mid"],
                "bestTime": "Afternoon",
                "estimatedCost": 14,
                "budgetBand": "mid",
            },
            {
                "name": "Singapore Botanic Gardens",
                "why": "A calming, high-quality nature anchor with strong pacing benefits.",
                "tags": ["nature", "relaxed", "budget"],
                "bestTime": "Morning",
                "estimatedCost": 6,
                "budgetBand": "budget",
            },
        ],
        "food": [
            {
                "name": "Maxwell or Lau Pa Sat hawker run",
                "why": "High-trust entry point to Singapore's strongest everyday food experience.",
                "tags": ["food", "market", "budget"],
                "bestTime": "Lunch",
                "estimatedCost": 14,
                "budgetBand": "budget",
            },
            {
                "name": "Tiong Bahru brunch and coffee block",
                "why": "Great for a slower morning with design and residential texture.",
                "tags": ["coffee", "design", "relaxed"],
                "bestTime": "Morning",
                "estimatedCost": 16,
                "budgetBand": "mid",
            },
            {
                "name": "Bayfront skyline dinner",
                "why": "Good premium spend if you want a polished evening climax.",
                "tags": ["food", "premium", "scenic"],
                "bestTime": "Dinner",
                "estimatedCost": 70,
                "budgetBand": "premium",
            },
        ],
        "favorites": [
            {
                "name": "Joo Chiat shophouse streets",
                "why": "A colorful local-feeling district with good food crossover.",
                "tags": ["culture", "local", "walkable"],
                "bestTime": "Afternoon",
                "estimatedCost": 14,
                "budgetBand": "budget",
            },
            {
                "name": "Gillman Barracks",
                "why": "Quiet contemporary art zone that rewards slower travel styles.",
                "tags": ["art", "relaxed", "local"],
                "bestTime": "Afternoon",
                "estimatedCost": 10,
                "budgetBand": "budget",
            },
            {
                "name": "Robertson Quay night walk",
                "why": "Soft evening energy without the intensity of the most crowded zones.",
                "tags": ["scenic", "balanced", "mid"],
                "bestTime": "Evening",
                "estimatedCost": 18,
                "budgetBand": "mid",
            },
        ],
    },
    "paris": {
        "destination": "Paris",
        "summary": "Paris excels when approached as a city of districts: museum density, cafe rituals, river movement, and neighborhood texture all reward thoughtful pacing.",
        "whyNow": "Paris is strongest for travelers who care about atmosphere, culture, food, and the emotional quality of urban exploration.",
        "bestTime": "April to June and September to October",
        "seasonNote": "These months usually give you the best balance between weather, walkability, and crowd pressure.",
        "riskLevel": "Moderate city awareness",
        "safetyConfidence": 84,
        "transportNote": "Metro is efficient, but some of the best value comes from clustering districts and walking between them.",
        "safetyNotes": [
            "Keep an eye on belongings in dense tourist corridors and transit hubs.",
            "Reserve major museum slots in advance during busy months.",
            "Use main boulevards for late-evening returns.",
        ],
        "signals": ["museum density", "cafe culture", "walkability", "district identity"],
        "tips": [
            "Structure each day around one Left Bank or Right Bank cluster.",
            "Mix major icons with a quieter neighborhood route to avoid fatigue.",
            "A slower pace usually improves Paris more than an overpacked schedule.",
        ],
        "attractions": [
            {
                "name": "Louvre or Musee d'Orsay anchor block",
                "why": "Strong cultural payoff and reliable planning anchor.",
                "tags": ["art", "culture", "iconic", "mid"],
                "bestTime": "Morning",
                "estimatedCost": 22,
                "budgetBand": "mid",
                "theme": "Museum depth and classic city icons",
            },
            {
                "name": "Seine river and island walk",
                "why": "Ties major landmarks together while preserving a sense of urban rhythm.",
                "tags": ["scenic", "walkable", "budget"],
                "bestTime": "Late afternoon",
                "estimatedCost": 8,
                "budgetBand": "budget",
            },
            {
                "name": "Montmartre hillside circuit",
                "why": "High atmosphere with layers of art history and city views.",
                "tags": ["culture", "scenic", "high-energy"],
                "bestTime": "Evening",
                "estimatedCost": 14,
                "budgetBand": "mid",
            },
        ],
        "food": [
            {
                "name": "Corner boulangerie and cafe breakfast",
                "why": "One of the simplest and best-value ways to feel immediately in Paris.",
                "tags": ["coffee", "culture", "budget"],
                "bestTime": "Breakfast",
                "estimatedCost": 12,
                "budgetBand": "budget",
            },
            {
                "name": "Market lunch near a museum district",
                "why": "Efficient and high-quality midday fuel without losing route momentum.",
                "tags": ["food", "market", "mid"],
                "bestTime": "Lunch",
                "estimatedCost": 20,
                "budgetBand": "mid",
            },
            {
                "name": "Classic bistro dinner",
                "why": "Strong payoff for travelers prioritizing atmosphere and culinary identity.",
                "tags": ["food", "culture", "premium"],
                "bestTime": "Dinner",
                "estimatedCost": 62,
                "budgetBand": "premium",
            },
        ],
        "favorites": [
            {
                "name": "Canal Saint-Martin stroll",
                "why": "A strong local-feeling route with cafes and softer city energy.",
                "tags": ["local", "walkable", "balanced"],
                "bestTime": "Afternoon",
                "estimatedCost": 12,
                "budgetBand": "budget",
            },
            {
                "name": "Le Marais side streets",
                "why": "Strong mix of history, independent retail, and food stops.",
                "tags": ["shopping", "culture", "local"],
                "bestTime": "Late afternoon",
                "estimatedCost": 18,
                "budgetBand": "mid",
            },
            {
                "name": "Rue des Martyrs food stretch",
                "why": "Great for food-first travelers who want local repeat-customer signal.",
                "tags": ["food", "local", "mid"],
                "bestTime": "Morning",
                "estimatedCost": 16,
                "budgetBand": "mid",
            },
        ],
    },
    "goa": {
        "destination": "Goa",
        "summary": "Goa delivers a mix of beach reset, cafe culture, nightlife, heritage pockets, and slower coastal movement that changes significantly by sub-region.",
        "whyNow": "Goa is excellent for travelers who want a lighter, more personal trip with lifestyle-driven pacing and strong memory value.",
        "bestTime": "November to February",
        "seasonNote": "The dry season is the strongest window for beaches, drives, and outdoor dining.",
        "riskLevel": "Relaxed with transport awareness",
        "safetyConfidence": 81,
        "transportNote": "Scooters and hired cars are common, but late-night returns should be planned before heading out.",
        "safetyNotes": [
            "Road confidence matters more than raw distance in Goa.",
            "Beach and party zones need extra awareness after dark.",
            "Monsoon months require more weather-sensitive planning.",
        ],
        "signals": ["beach pacing", "cafe culture", "nightlife", "heritage villages"],
        "tips": [
            "Choose north or south clusters per day to avoid wasting time in transit.",
            "Keep sunset blocks sacred because they drive the emotional memory of the trip.",
            "Blend one quiet beach or village block with one social or food-heavy evening.",
        ],
        "attractions": [
            {
                "name": "Fontainhas and Latin quarter walk",
                "why": "Adds heritage color and visual identity beyond the beach narrative.",
                "tags": ["culture", "walkable", "budget"],
                "bestTime": "Morning",
                "estimatedCost": 6,
                "budgetBand": "budget",
                "theme": "Coastal ease with heritage texture",
            },
            {
                "name": "Ashwem to Mandrem coastal stretch",
                "why": "Stronger for laid-back travelers who want scenic pacing and cafe stops.",
                "tags": ["nature", "relaxed", "scenic"],
                "bestTime": "Afternoon",
                "estimatedCost": 12,
                "budgetBand": "budget",
            },
            {
                "name": "Chapora sunset loop",
                "why": "One of the highest memory-value evening arcs in Goa.",
                "tags": ["scenic", "high-energy", "mid"],
                "bestTime": "Sunset",
                "estimatedCost": 18,
                "budgetBand": "mid",
            },
        ],
        "food": [
            {
                "name": "Beachside breakfast cafe",
                "why": "Best way to open a Goa day without rushing the mood.",
                "tags": ["coffee", "relaxed", "scenic"],
                "bestTime": "Breakfast",
                "estimatedCost": 14,
                "budgetBand": "budget",
            },
            {
                "name": "Goan seafood lunch spot",
                "why": "High local payoff if food is a trip priority.",
                "tags": ["food", "local", "mid"],
                "bestTime": "Lunch",
                "estimatedCost": 24,
                "budgetBand": "mid",
            },
            {
                "name": "Sunset cocktail and dinner lounge",
                "why": "Worth one premium spend if the trip is experience-first.",
                "tags": ["food", "premium", "high-energy"],
                "bestTime": "Dinner",
                "estimatedCost": 58,
                "budgetBand": "premium",
            },
        ],
        "favorites": [
            {
                "name": "Assagao creative cafe loop",
                "why": "Great for slower, design-aware, lifestyle-driven travel styles.",
                "tags": ["design", "coffee", "relaxed"],
                "bestTime": "Late morning",
                "estimatedCost": 16,
                "budgetBand": "mid",
            },
            {
                "name": "South Goa hidden beach window",
                "why": "Useful counterweight if the north feels too high-energy.",
                "tags": ["nature", "local", "relaxed"],
                "bestTime": "Afternoon",
                "estimatedCost": 10,
                "budgetBand": "budget",
            },
            {
                "name": "Anjuna local market pocket",
                "why": "Adds browsing and snack-based discovery without hard planning.",
                "tags": ["market", "local", "budget"],
                "bestTime": "Evening",
                "estimatedCost": 12,
                "budgetBand": "budget",
            },
        ],
    },
}


DESTINATION_SEEDS = merge_destination_demo_intelligence(DESTINATION_SEEDS)


class RecommendationEngine:
    VERSION = "rule-engine-v2"

    def __init__(
        self,
        source_discovery: SourceDiscovery | None = None,
        prioritization_engine: PrioritizationEngine | None = None,
        itinerary_planner: ItineraryPlanner | None = None,
        risk_analyzer: RiskAnalyzer | None = None,
        social_signal_engine: SocialSignalEngine | None = None,
    ) -> None:
        self.source_discovery = source_discovery or SourceDiscovery(DESTINATION_SEEDS, FALLBACK_PROFILE)
        self.prioritization_engine = prioritization_engine or PrioritizationEngine()
        self.itinerary_planner = itinerary_planner or ItineraryPlanner()
        self.risk_analyzer = risk_analyzer or RiskAnalyzer()
        self.social_signal_engine = social_signal_engine or SocialSignalEngine()

    def generate(self, payload: dict[str, Any] | RecommendationInput) -> dict[str, Any]:
        request = payload if isinstance(payload, RecommendationInput) else self._coerce_input(payload)
        profile, recognized = self.source_discovery.discover(request.destination)
        budget_per_day = round(request.budget / max(request.duration, 1), 2)

        ranked_attractions = self.prioritization_engine.rank_items(
            profile["attractions"], request.interests, request.travel_style, request.pace, budget_per_day, limit=3
        )
        ranked_food = self.prioritization_engine.rank_items(
            profile["food"], request.interests, request.travel_style, request.pace, budget_per_day, limit=3
        )
        ranked_favorites = self.prioritization_engine.rank_items(
            profile["favorites"], request.interests, request.travel_style, request.pace, budget_per_day, limit=3
        )
        itinerary = self.itinerary_planner.build(
            request.duration, ranked_attractions, ranked_food, ranked_favorites, request.pace
        )
        safety = self.risk_analyzer.analyze(profile, request.pace, budget_per_day)
        scores = self._build_scores(recognized, budget_per_day, safety["confidence"], request.interests, profile)
        supporting_signals = self._build_supporting_signals(profile, request)
        social_references = self.social_signal_engine.build_bundle(
            destination=profile["destination"],
            profile=profile,
            attractions=ranked_attractions,
            food=ranked_food,
            favorites=ranked_favorites,
            itinerary=itinerary,
        )
        ranked_attractions_with_refs = self.social_signal_engine.attach_item_references(
            ranked_attractions,
            references_by_name=social_references["attractions"],
        )
        ranked_food_with_refs = self.social_signal_engine.attach_item_references(
            ranked_food,
            references_by_name=social_references["foodAndCafes"],
        )
        ranked_favorites_with_refs = self.social_signal_engine.attach_item_references(
            ranked_favorites,
            references_by_name=social_references["localFavorites"],
        )
        itinerary_with_refs = self.social_signal_engine.attach_itinerary_references(
            itinerary,
            itinerary_references=social_references["itinerary"],
        )

        return {
            "meta": {
                "engineVersion": self.VERSION,
                "recognizedDestination": recognized,
                "mode": "seeded-destination-intelligence" if recognized else "adaptive-fallback-intelligence",
                "scores": scores,
                "signals": profile["signals"],
            },
            "request": {
                "destination": request.destination,
                "budget": request.budget,
                "currency": request.currency,
                "duration": request.duration,
                "interests": request.interests,
                "travelStyle": request.travel_style,
                "pace": request.pace,
            },
            "destinationSummary": {
                "headline": f"{profile['destination']} optimized for a {request.pace} {request.travel_style.lower()} journey",
                "overview": profile["summary"],
                "whyThisWorks": profile["whyNow"],
                "explanationSummary": profile.get("explanationSummary", profile["whyNow"]),
                "travelStyleFit": self._travel_style_fit(request.travel_style, request.pace, budget_per_day),
            },
            "topAttractions": [self._format_experience(item, request.currency) for item in ranked_attractions_with_refs],
            "foodAndCafes": [self._format_experience(item, request.currency) for item in ranked_food_with_refs],
            "localFavorites": [self._format_experience(item, request.currency) for item in ranked_favorites_with_refs],
            "dayWiseItinerary": itinerary_with_refs,
            "budgetGuidance": self._budget_guidance(request, profile, budget_per_day),
            "safetyAndRisk": safety,
            "bestTimeToVisit": {
                "window": profile["bestTime"],
                "why": profile["seasonNote"],
            },
            "travelTips": profile["tips"][:4],
            "supportingSignals": supporting_signals,
            "socialReferences": social_references,
        }

    def _coerce_input(self, payload: dict[str, Any]) -> RecommendationInput:
        interests = payload.get("interests", [])
        if isinstance(interests, str):
            interests = [item.strip() for item in interests.split(",") if item.strip()]

        normalized_interests = [item.lower() for item in interests][:6]
        return RecommendationInput(
            destination=str(payload.get("destination", "")).strip().title(),
            budget=int(payload.get("budget", 0)),
            currency=str(payload.get("currency", "USD")).strip().upper() or "USD",
            duration=int(payload.get("duration", 1)),
            interests=normalized_interests or ["culture", "food"],
            travel_style=str(payload.get("travelStyle", "Balanced Explorer")).strip() or "Balanced Explorer",
            pace=str(payload.get("pace", "balanced")).strip().lower() or "balanced",
        )

    def _format_experience(self, item: dict[str, Any], currency: str) -> dict[str, Any]:
        return {
            "name": item["name"],
            "why": item["why"],
            "bestTime": item.get("bestTime", "Flexible"),
            "estimatedCost": item.get("estimatedCost", 0),
            "currency": currency,
            "budgetBand": item.get("budgetBand", "mid"),
            "references": item.get("references", [])[:2],
        }

    def _build_scores(
        self,
        recognized: bool,
        budget_per_day: float,
        safety_confidence: int,
        interests: list[str],
        profile: dict[str, Any],
    ) -> dict[str, int]:
        score_inputs = profile.get("scoreInputs", {})
        destination_intelligence = int(score_inputs.get("destinationIntelligence", 92 if recognized else 74))
        local_signal_dynamic = min(96, 72 + len(interests) * 5 + floor(len(profile["favorites"]) * 1.5))
        if budget_per_day < 90:
            budget_fit_dynamic = 79
        elif budget_per_day <= 180:
            budget_fit_dynamic = 90
        elif budget_per_day <= 320:
            budget_fit_dynamic = 94
        else:
            budget_fit_dynamic = 88

        budget_fit = int(round((budget_fit_dynamic + score_inputs.get("budgetFit", budget_fit_dynamic)) / 2))
        local_signal = int(round((local_signal_dynamic + score_inputs.get("localSignal", local_signal_dynamic)) / 2))
        blended_safety = int(round((safety_confidence + score_inputs.get("safetyConfidence", safety_confidence)) / 2))

        return {
            "destinationIntelligence": destination_intelligence,
            "budgetFit": budget_fit,
            "localSignal": local_signal,
            "safetyConfidence": blended_safety,
        }

    def _travel_style_fit(self, travel_style: str, pace: str, budget_per_day: float) -> str:
        travel_style_lower = travel_style.lower()
        if "food" in travel_style_lower:
            base = "The engine leans toward markets, standout meals, and cafe rituals."
        elif "budget" in travel_style_lower:
            base = "The engine protects value density, transit efficiency, and free or low-cost cultural anchors."
        elif "luxury" in travel_style_lower:
            base = "The engine prioritizes polished hospitality, premium dining, and low-friction logistics."
        else:
            base = "The engine balances signature highlights with neighborhood texture and practical movement."

        if pace == "slow":
            return f"{base} It also reduces transition load so the trip feels calmer and more intentional."
        if pace == "fast":
            return f"{base} It also compresses higher-signal experiences into each day without losing route logic."
        if budget_per_day > 250:
            return f"{base} The higher budget unlocks one premium experience anchor per day."
        return base

    def _budget_guidance(
        self,
        request: RecommendationInput,
        profile: dict[str, Any],
        budget_per_day: float,
    ) -> dict[str, Any]:
        if budget_per_day < 100:
            tier = "Value-led"
            guidance = "Focus on walkable districts, markets, transit efficiency, and one standout paid experience."
        elif budget_per_day <= 220:
            tier = "Balanced comfort"
            guidance = "You can mix iconic attractions, quality food, and one premium moment without overspending."
        else:
            tier = "Premium flexibility"
            guidance = "You have enough headroom for reservations, premium dining, and low-friction routing."

        return {
            "tier": tier,
            "totalBudget": request.budget,
            "currency": request.currency,
            "duration": request.duration,
            "budgetPerDay": budget_per_day,
            "guidance": guidance,
            "suggestedAllocation": {
                "stay": f"{max(25, min(40, int(34 + budget_per_day / 50)))}%",
                "food": f"{max(20, min(34, int(24 + budget_per_day / 80)))}%",
                "localTransport": "10%",
                "experiences": "22%",
                "buffer": "8%",
            },
            "destinationNote": f"{profile['destination']} performs well when spend is concentrated in high-signal districts rather than spread thin across long transfers.",
        }

    def _build_supporting_signals(
        self,
        profile: dict[str, Any],
        request: RecommendationInput,
    ) -> dict[str, Any]:
        return {
            "core": profile.get("signals", [])[:5],
            "social": profile.get("socialSignals", [])[:4],
            "socialReferencePolicy": {
                "platforms": ["YouTube", "Reddit"],
                "mode": "public-search-links-only",
            },
            "bestFor": profile.get("bestFor", [request.travel_style, "Flexible city break"])[:3],
            "styleIndicators": profile.get(
                "styleIndicators",
                [request.travel_style, request.pace.title(), profile.get("bestTime", "Flexible timing")],
            )[:4],
            "budgetIndicators": profile.get("budgetIndicators", {}),
            "itineraryHints": profile.get("itineraryHints", [])[:4],
            "scoreInputs": profile.get("scoreInputs", {}),
        }
