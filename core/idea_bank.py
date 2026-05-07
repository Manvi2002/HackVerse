import random

IDEA_BANK = {
    "ai": [
        {"title":"AI Mental Health Companion","problem":"Students lack affordable mental health support.","solution":"A chatbot using NLP that detects emotional tone and provides coping strategies, journaling prompts, and crisis escalation.","tech_stack":["Python","HuggingFace","Django","React"]},
        {"title":"Resume Skill Gap Analyzer","problem":"Job seekers don't know what skills to learn next.","solution":"Upload a resume and a target job description; AI highlights gaps and recommends free courses to bridge them.","tech_stack":["Python","spaCy","Gemini API","Next.js"]},
        {"title":"Deepfake Detection Browser Extension","problem":"Deepfake images spread misinformation online.","solution":"A browser extension that flags AI-generated images in real time using a lightweight CNN model.","tech_stack":["PyTorch","ONNX","JavaScript","Chrome Extension API"]},
        {"title":"AI Crop Disease Detector","problem":"Farmers lose crops due to undetected disease.","solution":"Point your phone at a crop leaf; the app identifies disease and recommends organic treatment using image classification.","tech_stack":["TensorFlow Lite","Flutter","FastAPI","Firebase"]},
        {"title":"Smart Meeting Summarizer","problem":"Long meetings waste productivity.","solution":"Record a meeting; AI transcribes, extracts action items, assigns owners, and emails a summary automatically.","tech_stack":["Whisper","LangChain","Python","SendGrid"]},
        {"title":"Code Review AI Assistant","problem":"Junior developers lack mentorship on code quality.","solution":"Paste code and receive detailed feedback on bugs, security issues, and best practices with explanations.","tech_stack":["OpenAI API","FastAPI","React","PostgreSQL"]},
    ],
    "ml": [
        {"title":"Fake News Classifier","problem":"Misinformation spreads faster than corrections.","solution":"A BERT-based model that classifies news articles as real or fake with a confidence score and source analysis.","tech_stack":["BERT","PyTorch","Flask","React"]},
        {"title":"Predictive Student Dropout System","problem":"Universities lose students without early warning.","solution":"ML model trained on attendance, grades, and engagement data predicts dropout risk 6 weeks in advance.","tech_stack":["Scikit-learn","Pandas","Django","Chart.js"]},
        {"title":"Dynamic Pricing Engine","problem":"Small retailers lose revenue with static pricing.","solution":"Reinforcement learning model adjusts product prices in real time based on demand, competition, and stock.","tech_stack":["Python","Stable Baselines3","FastAPI","PostgreSQL"]},
        {"title":"Personalized Fitness Coach","problem":"Generic workout plans don't adapt to individual progress.","solution":"ML model analyzes workout logs and biometric data to generate adaptive weekly training plans.","tech_stack":["TensorFlow","Flutter","Firebase","Python"]},
        {"title":"Traffic Flow Predictor","problem":"Cities lack tools to anticipate congestion.","solution":"LSTM model trained on historical traffic data predicts congestion 30 minutes ahead and reroutes smart signals.","tech_stack":["LSTM","Keras","OpenStreetMap","Django"]},
    ],
    "web3": [
        {"title":"Decentralized Freelancer Escrow","problem":"Freelancers and clients don't trust payment systems.","solution":"Smart contract holds funds in escrow; released automatically when both parties approve milestone completion.","tech_stack":["Solidity","Hardhat","React","Ethers.js"]},
        {"title":"NFT Academic Certificates","problem":"Fake degrees are hard to detect.","solution":"Universities issue tamper-proof NFT degrees on-chain; employers verify authenticity with one wallet scan.","tech_stack":["Solidity","IPFS","Next.js","MetaMask"]},
        {"title":"DAO Community Voting Platform","problem":"Online communities lack transparent governance.","solution":"Token-weighted voting system for community proposals with on-chain result recording and execution.","tech_stack":["Solidity","OpenZeppelin","React","The Graph"]},
        {"title":"Blockchain Supply Chain Tracker","problem":"Counterfeit products enter supply chains undetected.","solution":"Each product gets a unique on-chain ID; every handoff is recorded and publicly verifiable by consumers.","tech_stack":["Ethereum","Solidity","Node.js","QR Code API"]},
        {"title":"Decentralized Crowdfunding","problem":"Traditional platforms take high fees and can freeze accounts.","solution":"Creators launch campaigns using smart contracts; backers get NFT perks; funds release on milestone completion.","tech_stack":["Solidity","Chainlink","React","IPFS"]},
    ],
    "fintech": [
        {"title":"AI Expense Splitter","problem":"Splitting shared expenses among groups is chaotic.","solution":"App scans receipts using OCR, auto-categorizes items, and splits bills fairly with UPI payment integration.","tech_stack":["Python","Tesseract OCR","React Native","Razorpay API"]},
        {"title":"Micro-Investment Platform for Students","problem":"Students can't afford minimum investment thresholds.","solution":"Round up spare change from daily UPI transactions into a diversified micro-portfolio starting from ₹1.","tech_stack":["Python","Django","React","Zerodha Kite API"]},
        {"title":"Loan Eligibility Predictor","problem":"Bank loan rejections are opaque and biased.","solution":"ML model evaluates alternative creditworthiness signals (utility bills, rent history) and explains decisions.","tech_stack":["XGBoost","Flask","React","PostgreSQL"]},
        {"title":"Real-Time Fraud Alert System","problem":"Transaction fraud is detected hours too late.","solution":"Stream transactions through an anomaly detection model; flag suspicious patterns and freeze cards in milliseconds.","tech_stack":["Apache Kafka","Scikit-learn","FastAPI","Redis"]},
        {"title":"Budget Coach Chatbot","problem":"People overspend without realizing it.","solution":"Connect your bank account; the chatbot analyzes spending patterns and sends proactive budget nudges via WhatsApp.","tech_stack":["Python","Plaid API","Twilio","LangChain"]},
    ],
    "cybersecurity": [
        {"title":"Phishing Email Analyzer","problem":"Employees fall for sophisticated phishing emails.","solution":"Browser extension that scans incoming emails for phishing indicators and shows a trust score with explanation.","tech_stack":["Python","NLP","Chrome Extension","FastAPI"]},
        {"title":"Dark Web Monitor","problem":"Companies don't know when their data is leaked.","solution":"Continuously crawls dark web forums and paste sites; alerts businesses when their emails or credentials appear.","tech_stack":["Python","Tor","Elasticsearch","Django"]},
        {"title":"Vulnerability Scanner for SMBs","problem":"Small businesses can't afford enterprise security audits.","solution":"Automated tool scans web apps and networks for common vulnerabilities (OWASP Top 10) and generates fix reports.","tech_stack":["Python","Nmap","OWASP ZAP","React"]},
        {"title":"Zero Trust Access Manager","problem":"Remote work increases insider threat risk.","solution":"Dynamic access control system that continuously validates user identity, device health, and behavior before granting access.","tech_stack":["Python","OAuth2","FastAPI","Redis"]},
        {"title":"Password Health Dashboard","problem":"Users reuse weak passwords across services.","solution":"Analyze saved passwords, check against breach databases (HaveIBeenPwned), and guide users through secure replacements.","tech_stack":["Python","HaveIBeenPwned API","React","AES Encryption"]},
    ],
    "fullstack": [
        {"title":"Remote Team Standup Board","problem":"Async remote teams lose sync without daily standups.","solution":"Automated daily check-in form; answers aggregate into a visual team board with blockers highlighted for managers.","tech_stack":["Django","React","WebSockets","PostgreSQL"]},
        {"title":"Hyperlocal Service Marketplace","problem":"Finding reliable local plumbers, electricians is hard.","solution":"Geo-based platform connects residents with verified service providers; live tracking and in-app payment included.","tech_stack":["Django","React Native","Google Maps API","Stripe"]},
        {"title":"Open Source Contribution Tracker","problem":"Developers can't showcase open source work professionally.","solution":"GitHub-linked dashboard that aggregates contributions, calculates impact scores, and generates shareable portfolios.","tech_stack":["Node.js","GitHub API","React","MongoDB"]},
        {"title":"Real-Time Collaborative Whiteboard","problem":"Remote teams lack a simple digital brainstorming space.","solution":"Infinite canvas with real-time sync, sticky notes, voting, and AI-powered idea clustering for meetings.","tech_stack":["React","Socket.io","Node.js","Canvas API"]},
        {"title":"Developer Portfolio Builder","problem":"Building a portfolio site is time-consuming for developers.","solution":"Answer 10 questions; AI generates a custom portfolio site with projects, skills, and contact form — deployed in minutes.","tech_stack":["Next.js","OpenAI API","Vercel","Tailwind CSS"]},
    ],
    "ecommerce": [
        {"title":"Visual Search Shopping","problem":"Users can't describe what they want to search for.","solution":"Upload or point your camera at any product; AI finds visually similar items across multiple stores with price comparison.","tech_stack":["TensorFlow","React Native","FastAPI","Elasticsearch"]},
        {"title":"AI Personal Stylist","problem":"Online shoppers return clothes due to poor fit/style match.","solution":"Answer a style quiz; AI curates a weekly outfit recommendation using your existing wardrobe and new arrivals.","tech_stack":["Python","Recommendation Engine","Django","React"]},
        {"title":"Abandoned Cart Recovery Bot","problem":"70% of online carts are abandoned before checkout.","solution":"WhatsApp bot sends personalized reminders with dynamic discounts based on cart value and customer history.","tech_stack":["Python","Twilio","Django","PostgreSQL"]},
        {"title":"Live Shopping Platform","problem":"Traditional e-commerce lacks the social shopping experience.","solution":"Influencers host live streams with clickable product overlays; viewers purchase without leaving the stream.","tech_stack":["WebRTC","React","Node.js","Stripe"]},
        {"title":"Sustainability Scorecard for Products","problem":"Eco-conscious shoppers can't verify sustainability claims.","solution":"Browser extension that overlays a green score on product pages based on brand practices, materials, and certifications.","tech_stack":["JavaScript","Python","Chrome Extension","FastAPI"]},
    ],
    "healthtech": [
        {"title":"Medication Reminder & Tracker","problem":"Patients forget doses leading to treatment failure.","solution":"App sends smart reminders based on prescription schedule; family members get alerts for missed doses.","tech_stack":["Flutter","Firebase","Django","Twilio"]},
        {"title":"AI Symptom Checker","problem":"People delay seeking care due to health anxiety or cost.","solution":"Chat-based triage tool that maps symptoms to probable conditions and recommends urgency level (home care vs. ER).","tech_stack":["NLP","FastAPI","React","Medical Ontology API"]},
        {"title":"Telemedicine Queue Manager","problem":"Rural clinics have no way to manage patient wait times digitally.","solution":"SMS-based virtual queue system for clinics; patients join from a basic phone and get SMS updates on wait time.","tech_stack":["Django","Twilio","PostgreSQL","SMS API"]},
        {"title":"Mental Wellness Journal","problem":"People lack structured tools for daily mental health reflection.","solution":"Guided journaling app with mood tracking, AI-detected emotional patterns, and weekly wellness reports.","tech_stack":["React Native","Firebase","Python","HuggingFace"]},
        {"title":"Elderly Fall Detection System","problem":"Elderly people living alone face danger after falls.","solution":"Wearable + phone app combo detects sudden impacts using accelerometer data and auto-calls emergency contacts.","tech_stack":["Python","TensorFlow Lite","Flutter","Twilio"]},
    ],
    "edtech": [
        {"title":"Adaptive Quiz Engine","problem":"One-size-fits-all quizzes don't address individual gaps.","solution":"AI selects next question based on response patterns; weak areas get reinforced automatically using spaced repetition.","tech_stack":["Python","Django","React","PostgreSQL"]},
        {"title":"Lecture Summarizer","problem":"Students struggle to review hours of recorded lectures.","solution":"Upload a lecture video; AI transcribes, generates chapter summaries, and creates flashcards automatically.","tech_stack":["Whisper","LangChain","React","FastAPI"]},
        {"title":"Peer Study Group Matcher","problem":"Students study alone and lack peer collaboration.","solution":"Platform matches students by subject, schedule, and learning style to form productive virtual study groups.","tech_stack":["Django","React","WebRTC","PostgreSQL"]},
        {"title":"Code Learning Sandbox","problem":"Beginners struggle with setting up coding environments.","solution":"Browser-based IDE with guided challenges, real-time error explanations in plain English, and progress tracking.","tech_stack":["React","Monaco Editor","Docker","FastAPI"]},
        {"title":"Parent Progress Dashboard","problem":"Parents have no visibility into their child's school progress.","solution":"Real-time dashboard pulling attendance, grades, and teacher feedback from school systems into one parent view.","tech_stack":["Django","React","REST API","Chart.js"]},
    ],
    "sustainability": [
        {"title":"Food Waste Marketplace","problem":"Restaurants throw away tons of unsold food daily.","solution":"Platform lets restaurants list surplus food at discount; nearby buyers get notified and pick up before closing time.","tech_stack":["Django","React Native","Google Maps API","Stripe"]},
        {"title":"Carbon Footprint Tracker","problem":"Individuals don't know their daily carbon impact.","solution":"Log meals, travel, and purchases; app calculates CO2 footprint and suggests offset actions with measurable impact.","tech_stack":["Python","Django","React","Carbon API"]},
        {"title":"Smart Irrigation System","problem":"Farmers over-water crops wasting water.","solution":"IoT soil moisture sensors feed data to an ML model that schedules irrigation only when needed, cutting water use by 40%.","tech_stack":["Arduino","MQTT","Python","React Dashboard"]},
        {"title":"E-Waste Collection Network","problem":"Electronics are improperly disposed causing toxic pollution.","solution":"Map-based platform connects households with certified e-waste collectors; incentivizes participation with reward points.","tech_stack":["Django","Google Maps API","React","PostgreSQL"]},
        {"title":"Green Commute Planner","problem":"Commuters default to cars due to lack of eco route info.","solution":"App compares carbon footprint of different commute routes and recommends lowest-emission option with time trade-off.","tech_stack":["Python","Google Maps API","React Native","Firebase"]},
    ],
    "open": [
        {"title":"Civic Issue Reporter","problem":"Residents have no easy way to report potholes or broken lights.","solution":"One-tap issue reporting app with photo, GPS, and auto-routing to the correct municipal department.","tech_stack":["React Native","Django","Google Maps API","PostgreSQL"]},
        {"title":"Local Skill Exchange Platform","problem":"Communities underutilize the diverse skills of their members.","solution":"Barter platform where people trade skills (e.g., guitar lessons for cooking classes) without money.","tech_stack":["Django","React","WebSockets","PostgreSQL"]},
        {"title":"Disaster Relief Coordination Hub","problem":"Aid organizations duplicate efforts during disasters.","solution":"Real-time map showing which areas have been covered, what's needed, and how to volunteer or donate.","tech_stack":["React","Django","WebSockets","Google Maps API"]},
        {"title":"Community Library of Things","problem":"People buy tools they use once and discard.","solution":"Neighborhood platform for borrowing items (drills, tents, ladders) with reputation scores and deposit management.","tech_stack":["Django","React","Stripe","PostgreSQL"]},
        {"title":"Language Buddy App","problem":"Immigrants struggle to learn the local language without practice partners.","solution":"App pairs immigrants with native speakers for 30-minute weekly voice calls with structured conversation topics.","tech_stack":["Django","WebRTC","React Native","Firebase"]},
    ],
}

THEME_ALIASES = {
    "ai": ["ai", "artificial intelligence", "ai/ml", "machine learning", "ml", "deep learning", "nlp"],
    "web3": ["web3", "blockchain", "crypto", "nft", "defi", "ethereum", "solidity", "decentralized"],
    "fintech": ["fintech", "finance", "financial", "banking", "payments", "investment", "money"],
    "cybersecurity": ["cybersecurity", "security", "hacking", "cyber", "infosec", "privacy"],
    "fullstack": ["full stack", "fullstack", "web development", "web dev", "backend", "frontend"],
    "ecommerce": ["ecommerce", "e-commerce", "shopping", "retail", "marketplace"],
    "healthtech": ["health", "healthtech", "medical", "medicine", "healthcare", "wellness", "fitness"],
    "edtech": ["edtech", "education", "learning", "teaching", "school", "university", "courses"],
    "sustainability": ["sustainability", "green", "environment", "climate", "eco", "clean energy"],
    "open": ["open", "open innovation", "social", "civic", "community", "startup", "for good"],
}


def match_theme(query: str) -> str:
    """Match user input to the closest theme key."""
    query = query.lower().strip()
    for key, aliases in THEME_ALIASES.items():
        for alias in aliases:
            if alias in query or query in alias:
                return key
    return "open"  # fallback


def get_ideas(theme: str, count: int = 5) -> list:
    """Return `count` shuffled ideas for the given theme."""
    key = match_theme(theme)
    pool = IDEA_BANK.get(key, IDEA_BANK["open"])
    sample = random.sample(pool, min(count, len(pool)))
    return sample
