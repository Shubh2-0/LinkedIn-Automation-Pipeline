<div align="center">
  <img src="banner.png" width="80%" height="80%" style="object-fit: cover; border-radius: 12px;"/>
  
  <br><br>
  
  <h1>🔗 Autonomous LinkedIn Outreach & Posting Script</h1>
  <i>A Python-based AI Pipeline for Document Processing and Social Graph Management</i>
  <br><br>

  <p>
    <img src="https://img.shields.io/badge/Python_3-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/Algorithms-412991?style=for-the-badge&logo=hackthebox&logoColor=white" />
    <img src="https://img.shields.io/badge/Automation-43B02A?style=for-the-badge&logo=selenium&logoColor=white" />
  </p>
</div>

<br>

## 💡 Executive Summary
Maintaining an active professional presence requires immense manual labor. This project is a hands-free, autonomous Python pipeline that authenticates, navigates, and formulates scheduled posts incorporating heavy PDF media structures.

By tying together **Data Serialization**, **Session Caching/Tokenization**, and **Python Scripting**, this acts as a fully autonomous digital avatar ensuring sustained networking trajectory throughout the week.

---

## ⚡ Core Engineering Details
> *Merging automation scripts into a robust, fault-tolerant execution model.*

- **Headless Logic & API Hooking:** Utilizes advanced browser scraping or direct API session emulation via `get_token.py` to interact with dynamic web elements safely.
- **Complex Media Handling:** Contains highly dynamic scheduling architecture (`schedule.json`) that processes large internal PDF rendering (`pdfs/`) sequentially based on calendar logic.
- **Exception Resilience:** Social media ecosystems change rapidly. The `post_to_linkedin.py` layers utilize `try-catch` structures to auto-recover from stale network paints without crashing the primary loop.
- **Data Encapsulation:** Employs strictly isolated configurations so tokens and sensitive schedule mapping do not bleed into the functional executing logic.

---

## 🛠️ The System Layer
| Layer | Technologies used | Justification |
| --- | --- | --- |
| **Logic/Hooks** | `Python 3` | Acts as the primary driver executing core workflows and reading system storage files. |
| **Authentication Logic** | `Tokenizers`| Safely scrapes or stores required authentication logic avoiding rigid hard-coding constraints. |
| **Schedule Control**| `JSON Management` | Drives asynchronous scheduling allowing the script to know "what" to post and "when". |

---

## 🚀 How to Execute (Local Pipeline)

<details>
  <summary><b>Click to expand deployment steps</b></summary>
  
  <br/>
  
  1. **Clone the Infrastructure**
     ```bash
     git clone https://github.com/Shubh2-0/linkedin-ai-automation.git
     ```
  2. **Provide Protected Keys & PDFs**
     Execute `get_token.py` or manually map your access token so the script assumes your persona securely. Ensure target PDFs reside inside the correct folder map.
  3. **Trigger the Pipeline**
     ```bash
     python post_to_linkedin.py
     ```
</details>

<br>

<div align="center">
  <b>Built by Shubham Bhati</b> — <i>Software Engineer (Backend & AI Pipelines)</i>
</div>
