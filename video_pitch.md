# 🎥 FINCRAWL: 2-Minute Devpost Pitch Script

**Target Audience**: Hackathon Judges, Investors, Tech Community.
**Tone**: Urgent, Professional, Innovative ("Bloomberg meets AI").
**Length**: ~2 Minutes.

---

## 🎬 0:00 - 0:20 | The Hook (Problem)
**(Camera on You or Montage of Stock Charts/News Headlines)**

"Every year, investors lose billions due to sudden corporate failures—fraud, bankruptcy, and hidden risks buried deep in thousands of pages of regulatory filings. 
The problem isn't lack of data; it's *overload*. No human analyst can read every 10-K, 8-K, and news wire in real-time."

**"What if you had an autonomous AI agent that read everything for you, 24/7, and alerted you to risks *before* the market reacted?"**

---

## 🚀 0:20 - 0:50 | The Solution (What is FinCrawl?)
**(Screen Share: Show the FinCrawl Landing/Dashboard - Dark Mode UI)**

"Introducing **FinCrawl**: An Autonomous Filings & Disclosures Early-Warning System.
FinCrawl doesn't just keyword search. It *understands* financial stability."

**(Action: Scroll through the Dashboard Risk Feed)**

"It continuously ingests SEC filings and financial news feeds.
It uses a **Retrieval-Augmented Generation (RAG)** pipeline to effectively 'read' every document.
It then applies a hybrid **Risk Scoring Engine** to detect subtle red flags—like material weakness disclosures, executive churn, or liquidity concerns—giving every document a quantifiable Risk Score from 0 to 100."

---

## 🛠️ 0:50 - 1:20 | Under the Hood (The Tech)
**(Screen Share: Code / Terminal / Architecture Diagram)**

"We built this using a lean, powerful stack designed for speed and autonomy:
1.  **Ingestion**: Python-based Crawlers monitoring SEC EDGAR RSS feeds in real-time.
2.  **Vector Engine**: We use **ChromaDB** and **SentenceTransformers** to semantically index millions of text chunks locally.
3.  **The Brain**: A specialized scoring algorithm that combines pattern matching with semantic proximity to known risk events (like bankruptcy templates).
4.  **Frontend**: A responsive **React + Vite** dashboard with a premium dark-mode interface for instant visualization."

---

## 💻 1:20 - 1:50 | The Demo (Live Walkthrough)
**(Screen Share: Live Demo Flow)**

"Let's see it in action.
Here are the latest filings ingested just seconds ago.
**(Point to a High Risk item)**
Take a look at this entry. FinCrawl flagged it with a **Score of 85**. Why?
Because it detected a 'Going Concern' warning buried in the footnotes.
A human analyst might miss this on a Friday afternoon. FinCrawl caught it instantly."

**(Show the Search/Filter)**
"We can also query the vector database directly: 'Show me all companies mentioning supply chain fraud'. The RAG engine retrieves the exact paragraphs for verification."

---

## 🏁 1:50 - 2:00 | Conclusion & Impact
**(Camera on You)**

"FinCrawl democratizes institutional-grade financial intelligence.
We are moving from *passive* reading to *autonomous* risk detection.
This isn't just a search engine; it's a shield for your portfolio.
I'm [Your Name], and this is FinCrawl."

**(Fade to Black with Logo/URL)**
