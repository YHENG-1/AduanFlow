# "AI CAN DO IT" Tencent Cloud x UTM Hackathon 2026 Challenge Brief

## AI Agent Track Handbook

---

## 1. Event Overview

The **"AI CAN DO IT" Tencent Cloud x UTM Hackathon 2026** is a collaboration between **Universiti Teknologi Malaysia (UTM)** and **Tencent Cloud**. This hackathon brings together industry-leading AI technologies and academic excellence to empower the next generation of AI innovators.

Participants will develop AI-powered solutions using **Tencent CodeBuddy**, **WorkBuddy**, or **Miora** while tackling real-world industry challenges developed in collaboration with industry experts. They will also gain insights from AI specialists and transform innovative ideas into practical solutions.

Supported by the **Tencent Institute of Games**, **Tencent WeTech Academy**, and the **Tencent Interactive Entertainment Group (IEG) Social Value Exploration Center**, the competition features five regional divisions worldwide:
* Hong Kong and Macao SARs
* East China
* North China
* South China
* Southeast Asia

It covers leading universities and game developer communities in China and abroad.

Each division will host offline Demo Day roadshows, giving participants a first-hand opportunity to showcase their work and engage with the industry.

Compete for exciting prizes, connect with industry leaders, and showcase your creativity on the international stage at the **Grand Final in Shenzhen, China**!

*Join us and discover what AI can do!*

---

## 2. The AI Agent Track Challenges

### Description
Collaborate with industry-leading companies to build AI agents that solve real-world business challenges. In this track, participants will tackle problem statements provided by industry leaders, leveraging AI technologies to develop practical, impactful solutions that address real needs across different industries.

### Requirement
This challenge presents **Three** real-world enterprise case studies contributed by our industry partners across the Financial Services, Technology, and Conglomerate sectors.

Each team is required to select only **ONE** case study to solve. Please clearly indicate your chosen case study at the beginning of your presentation.

---

### Case Study 1: AI-Powered Banking Dispute Automation Pipeline

#### Introduction
A Malaysian regional bank serving 1.8 million retail and SME customers faces mounting pressure to modernize its complaint-handling operations. Currently, dispute resolution is a manual, multi-department process that averages 90 minutes per case, with approximately 11% of regulatory deadlines missed. The bank must comply with Bank Negara Malaysia (BNM) Policy Document on Complaints Handling and the Financial Markets Ombudsman Service (FMOS) framework, which mandates resolution timelines ranging from 5 to 20 working days depending on case complexity. With seven distinct dispute categories spanning unauthorized transactions, billing errors, mis-selling claims, and digital payment issues, the bank urgently needs an automated, AI-driven pipeline that can scale.

#### Problem Statement
How can a team of non-technical business professionals leverage AI agents and cloud infrastructure to automate the full lifecycle of banking dispute resolution — from email intake and security enforcement to investigative verification and customer communication — while maintaining regulatory compliance under BNM and FMOS frameworks?

#### Challenge
Design and build an end-to-end dispute automation pipeline that enables a small, non-technical team (5 participants) to orchestrate parallel AI agents for complaint ingestion, verification, financial resolution, and customer communication. The solution must process disputes across seven categories:
* Unauthorized transactions (35% volume)
* Billing errors (22%)
* Mis-selling claims (18%)
* ATM/debit card disputes (12%)
* Insurance/takaful claims (6%)
* Loan/financing disputes (5%)
* E-money/digital payment disputes (2%)

while embedding regulatory compliance checks at each stage. The ideal goal is to dramatically reduce processing time from the current 90-minute average, with a stretch target of under 5 minutes per case for fully automated (PASS-verified) disputes.

#### What the Solution Should Solve
Participants are expected to build a functional prototype incorporating the following capabilities:
* **Email Intake & Security Enforcement**: Connect to a complaints mailbox, parse text and apply OCR to PDF attachments to extract key identifiers (account numbers, NRICs, dispute amounts), and apply encryption for sensitive data at rest and in transit.
* **Automated Case Classification & Metadata Enrichment**: Automatically categorize disputes into their respective categories, assign urgency levels (High: 5 WD; Medium: 20 WD; Low: 20 WD + extensions), and stamp each case with a governance schema aligned to BNM policy.
* **Core System Verification Engine**: Cross-reference dispute data against core banking systems and CRM using MCP (Model Context Protocol) to output a verification status: PASS, FAIL, or MANUAL_REVIEW.
* **Autonomous Financial Resolution**: Automatically calculate adjustments, generate journal entries, post reversals or credits to complainant accounts, and update case status to FINANCIALLY_RESOLVED for verified (PASS) cases.
* **Compliant Customer Communication**: Auto-populate pre-approved email templates with mandatory BNM compliance disclosures and FMOS redress timelines. For claims $\le$ RM 250,000 where the customer remains dissatisfied, embed automated notice of their right to refer the matter to FMOS within 6 months.
* **Real-Time Management Dashboard**: A web-based dashboard that visualizes case pipeline status, classification accuracy, processing times, regulatory deadline tracking, and investigator workload distribution in real time.

#### The Solution Should Be
* **Accessible to non-technical users**: Operable through natural language commands without requiring programming expertise, enabling business professionals to orchestrate complex automation pipelines.
* **Regulatory-compliant by design**: Embed BNM and FMOS compliance checks at every stage of the pipeline, with the ideal goal of eliminating regulatory deadline misses while maintaining a complete audit trail.
* **Secure and auditable**: Implement encryption at rest, encryption in transit, and role-based data access controls. All actions should be logged for audit purposes.
* **Scalable across dispute categories**: Adapt to handle all 7 dispute types with category-specific processing logic — start with the highest-volume categories and expand incrementally.
* **Measurable impact**: Demonstrate quantifiable improvements in processing time (stretch target: < 5 min for automated cases), classification accuracy (aim for significant improvement from baseline), and investigator time freed (target: meaningful reduction in manual effort).

> **Note**: The features listed above are provided as guidance only. Participants are strongly encouraged to explore alternative approaches that meaningfully address the problem statement. The solution may take the form of a web application, an AI agent orchestration platform, a mobile app, or any combination thereof.

#### Suggested Tools & Technologies (WorkBuddy Ecosystem)
*All tools are accessible through WorkBuddy's built-in ecosystem without complex development environment setup. Operate via natural language.*

| Area | Recommended Tools | Description |
| :--- | :--- | :--- |
| **AI Agent** | WorkBuddy Ecosystem | A unified AI workspace that enables users to build, use, and manage intelligent agents through a natural language interface. |
| **Cloud** | Tencent Cloud | Provides the full AI agent infrastructure, from model orchestration and sandbox runtime to development platforms and extensible tools. |
| **Email** | Email MCP | Access the complaints inbox and watch for incoming emails. |
| **PDF/OCR** | Pdf skill (e.g. `pdfkit-py`) | Parse PDF files and perform OCR recognition. |

---

### Case Study 2: Intelligent Early Warning System for Organisational Performance
*(AI Analytics / Anomaly Detection / Executive Dashboard)*

#### Introduction
Large organizations track hundreds of indicators across finance, operations, projects, workforce, sustainability, and customer-related activities. However, performance issues are often only noticed after reports are manually prepared or after problems have already escalated into crises. Modern enterprises generate vast amounts of real-time and historical data that remains underutilized — waiting to be transformed into actionable intelligence. There is a critical opportunity to harness data science and artificial intelligence to detect early signals of underperformance, operational risk, and unusual trends before they become major issues that impact business continuity, financial health, or stakeholder confidence.

#### Problem Statement
How might we design an intelligent early warning system that helps decision-makers detect emerging risks, anomalies, and performance issues across multiple business areas before they escalate — moving organisations from reactive reporting to proactive, data-driven decision-making?

#### Challenge
Build a prototype that can analyse sample KPI data across multiple business dimensions, identify unusual patterns and anomalies, flag areas requiring immediate management attention, and explain possible root causes behind the alerts. The system should be capable of processing multi-dimensional organisational data — spanning financial indicators, operational metrics, project progress, workforce analytics, sustainability measures, and customer experience data — and surfacing actionable insights through an intuitive interface that empowers leadership to act before problems materialize. The ideal scope starts with 2–3 core business domains and expands incrementally.

#### What the Solution Should Solve
Participants are expected to build a functional prototype incorporating the following capabilities:
* **KPI Trend Analysis & Visualization**: Ingest and analyse time-series KPI data from multiple business domains. Visualize trends, cycles, and seasonal patterns to help decision-makers understand the trajectory of key metrics at a glance.
* **Anomaly Detection Engine**: Apply statistical methods and AI-powered pattern recognition to automatically detect deviations from expected performance ranges. Flag outliers, trend reversals, and emerging patterns that warrant investigation.
* **Target-vs-Actual Comparison**: Compare real-time performance data against predefined targets, budgets, and benchmarks. Highlight areas where actual performance is diverging from targets and quantify the gap with forward projections.
* **Risk Scoring & Prioritization**: Assign risk scores to detected anomalies based on severity, business impact, and urgency. Prioritize alerts so that leadership can focus on the most critical issues first.
* **Intelligent Alert Generation**: Generate contextual, human-readable alerts that explain why an issue was flagged, the potential business impact, and the data points that triggered the alert. Reduce alert fatigue by consolidating related signals.
* **Root-Cause Analysis & Explanation**: Provide AI-driven explanations of likely root causes behind detected anomalies. Correlate signals across business areas to identify systemic issues versus isolated incidents. For a hackathon prototype, correlation across 2–3 domains is a strong starting point.
* **Management Dashboard & Recommended Actions**: Present findings through an executive-friendly dashboard with drill-down capabilities. Generate recommended next actions based on the type and severity of each detected issue, enabling rapid decision-making.

#### The Solution Should Be
* **Proactive by design**: Shift organisations from reactive reporting (noticing problems after they happen) to proactive intelligence (detecting signals before problems materialize). The system should aim to anticipate rather than just report.
* **Multi-dimensional and holistic**: Integrate data from finance, operations, and customer domains as a starting point. The ideal goal is to eventually expand to projects, workforce, sustainability, and beyond — correlating signals across dimensions to surface insights that single-domain dashboards miss.
* **Interpretable and transparent**: Every alert should include an explanation of why it was triggered, what data supports it, and what the potential business impact could be. AI outputs should be explainable to build trust with decision-makers.
* **Scalable and adaptable**: Support configurable KPI definitions, customizable alert thresholds, and the ability to add new business domains without rebuilding the core engine. The system should grow with the organisation.
* **Actionable and decision-oriented**: Go beyond dashboards to provide recommended next steps, escalation pathways, and impact projections. The aim is to turn insights into operational directives that leadership can act on immediately.

> **Note**: The features and tools listed above are provided as guidance only. Participants are strongly encouraged to explore alternative approaches that meaningfully address the problem statement. The solution may take the form of a web dashboard, an AI-powered analytics platform, a mobile application, a chatbot assistant, or any combination thereof. Participants may use synthetic datasets containing monthly KPIs, targets, financial indicators, operational metrics, project progress data, workforce analytics, sustainability measures, customer experience scores, or external public indicators.

#### Suggested Tools & Technologies (WorkBuddy Ecosystem)
*All tools are accessible through WorkBuddy's built-in ecosystem without complex development environment setup. Operate via natural language.*

| Area | Recommended Tools | Description |
| :--- | :--- | :--- |
| **AI Agent** | WorkBuddy Ecosystem | A unified AI workspace that enables users to build, use, and manage intelligent agents through a natural language interface. |
| **Cloud** | Tencent Cloud | Provides the full AI agent infrastructure, from model orchestration and sandbox runtime to development platforms and extensible tools. |
| **Database** | Tencent Cloud Database | KPI data storage. |
| **Skill** | Financial skill | Pull external market data, macro-economic benchmarks, and industry reference indices for comparative analysis. |

---

### Case Study 3: AI Scam Shield
*(Intelligent AI-Powered Financial Scam Prevention Platform)*

#### Introduction
Digital banking and instant payment services have transformed the way Malaysians manage their finances, making transactions faster and more convenient than ever before. However, this convenience has also created new opportunities for cybercriminals. Financial scams have become increasingly sophisticated, leveraging artificial intelligence to generate convincing phishing messages, clone voices, impersonate trusted individuals, create fake investment opportunities, and manipulate victims through social engineering. As scams continue to evolve, traditional rule-based fraud detection systems struggle to identify emerging scam patterns before financial losses occur.

#### Problem Statement
Financial scams are becoming increasingly sophisticated, leveraging AI, social engineering, and rapidly evolving attack techniques to deceive victims. Existing solutions often struggle to keep pace with new scam patterns and emerging threats. There is a growing need for intelligent, adaptive solutions that can proactively identify, and respond to scams while protecting customers and strengthening trust in digital financial services.

#### Challenge
Participants are challenged to design an AI-powered Scam Shield that helps identify potential scam activities and supports users in making safer financial decisions. The solution may leverage a wide range of signals, such as customer behaviour, transaction patterns, device activity, communication channels, scam intelligence, or other relevant contextual information.

#### What the Solution Should Solve
The solution should use AI to assess potential scam risks, provide timely alerts or recommendations, explain why a situation is considered suspicious, and help users take appropriate action while minimizing unnecessary disruptions to legitimate activities.

#### The Solution Should Be
The proposed solution should go beyond conventional fraud detection by leveraging AI to help customers and financial institutions identify, assess, and respond to evolving scam threats. Participants are encouraged to explore innovative approaches that improve customer safety, trust, and decision-making.

The solution may include, but is not limited to, the following capabilities:
* Intelligently identify potential scam risks using relevant behavioural, contextual, transactional, or external signals.
* Provide timely insights, alerts, or recommendations to support safer customer decisions during digital interactions.
* Adapt to evolving scam tactics by learning from new patterns, emerging threats, and changing customer behaviour.
* Support effective scam response and mitigation, helping customers and organizations take appropriate actions when risks are identified.
* Empower financial institutions to stay ahead of evolving scam threats by leveraging AI to identify, assess, and respond to potential scams, enabling customers to make informed financial decisions while enhancing trust and confidence.

#### Suggested Tools & Technologies (WorkBuddy Ecosystem)
*All tools are accessible through WorkBuddy's built-in ecosystem without complex development environment setup. Operate via natural language.*

| Area | Recommended Tools | Description |
| :--- | :--- | :--- |
| **AI Agent** | WorkBuddy Ecosystem | A unified AI workspace that enables users to build, use, and manage intelligent agents through a natural language interface. |
| **Cloud** | Tencent Cloud | Provides the full AI agent infrastructure, from model orchestration and sandbox runtime to development platforms and extensible tools. |
| **Skill** | Financial skill | Skill to retrieve abnormal transactions, sudden amount spikes, and high-frequency micro-transactions. |
| **Database** | Tencent Cloud Database | User activity log and device information storage. |

---

## 3. Project Requirements

### Project Basic Requirements
* The project must be original and built on at least one of the products: **CodeBuddy** or **WorkBuddy**.
* **Proof of product usage is mandatory**: chat screenshots, API call logs, or a written development-process description. Without proof, the project will not proceed to scoring.

### Submission Requirements

| Submission Items | Req. | Description |
| :--- | :--- | :--- |
| **Project title** | Required | The name of your AI Agent project. |
| **Short blurb** | Required | A summary of what your project does or the value it delivers. **Hard limit: under 10 words**. |
| **Project Description** | Required | • **Project Overview**: Target Scenarios, Users, and Value Proposition.<br>• **Real-World Scenario Insights**: Source of Pain Points, Target Audience, and Core Problems Solved.<br>• **Comprehensive Solution Design**: Business and technical architecture, and how prompts drive the AI generation.<br>• **Business Value**: Quantifiable metrics or clearly defined impact. |
| **CodeBuddy Conversation History** | Required | The CodeBuddy chat history used during the project development process. |
| **Cover Image** | Required | A 16:9 cover image for your project, used for the online showcase. Recommended size: $380 \times 216\text{px}$. |
| **Demo video** | Optional | A 5–8 minute video covering:<br>• Project overview<br>• Core Agent features and how it's used<br>• A short reflection on your build approach and any development-tool tips |
| **Chat history** | Required | Minimum of 3 screenshots of your chat logs from CodeBuddy or WorkBuddy during the development process. |
| **Project link** | Optional (Bonus) | A live URL or demo link for your project. Optional, but earns bonus points. |

---

## 4. Competition Timeline

| Date | Stage & Description |
| :--- | :--- |
| **10 July 2026** | **Challenge Kick-off**: Challenge launch & submissions open |
| **13–17 July 2026** | **Online & Offline Training**: Hands-on workshops |
| **5 August 2026** | **Project Submission Deadline** |
| **11 August 2026** | **Campus Selection**: Shortlist Top 10 teams per track for Demo Day |
| **14 August 2026 (TBC)** | **Malaysia Demo Day**: Crown the Malaysia Winners |
| **Early September 2026** | **Grand Final**: Compete on the international stage in Shenzhen |

### Global Schedule

| Division | Demo Day Location | Schedule |
| :--- | :--- | :--- |
| **Hong Kong & Macao SARs** | Hong Kong SAR | July |
| **East China** | Shanghai | July |
| **North China** | Beijing | June |
| **South China** | Wuhan | July |
| **Southeast Asia** | Indonesia | July |
| **Grand Final** | Shenzhen | September |

---

## 5. How to Participate

* **Step 1: Register**  
  Sign up by clicking the registration link below. Only one registration is required per team. Each team may consist of 1–3 members and must include at least one UTM student.

* **Step 2: Join the WhatsApp Group and Receive the Hackathon Handbook**  
  You will be invited to join the WhatsApp group, and the Hackathon Handbook will also be sent to you via email.

* **Step 3: Create Your Accounts and Claim Your Credits**  
  Each team member may create CodeBuddy, WorkBuddy, and Miora accounts to receive complimentary credits and access Tencent Cloud's AI-powered development tools.

* **Step 4: Build and Submit Your Project**  
  Develop your project using CodeBuddy, WorkBuddy, or Miora, and submit it before the deadline.

### Important Links
* **Registration Link**: [https://tinyurl.com/TencentCloudUTMHackathon](https://tinyurl.com/TencentCloudUTMHackathon)
* **Submission Link**: [https://tinyurl.com/UTMProject-Submission](https://tinyurl.com/UTMProject-Submission)

---

## 6. Preliminary Judging Mechanism

Projects will be evaluated across the following four dimensions for a total score of **100 points**:

| Evaluation Dimension | Score | Key Review Focus |
| :--- | :--- | :--- |
| **AI Innovation** | 30 Points | Scenario Insight & Depth of AI Utilization |
| **Technical Excellence** | 20 Points | Engineering Implementation, Mastery of AI Tools, and Functional Completeness & Stability |
| **User Experience & Demo** | 25 Points | How smooth the demo is, thoughtfulness of interaction design and general user-friendliness. |
| **Business Value & Viability** | 25 Points | How well the project solves a real problem and its potential for commercial roll-out. |

### Review Process
1. **Campus Selection**: Each partner school submits projects to Tencent Cloud and selects one outstanding project from its own submissions to form a school representative team for the regional roadshow.
2. **Malaysia Demo Day Review**: Representative teams from participating schools present their projects live at the offline roadshow. Judges score each project based on theme alignment, use of AI tools, and game quality, and select regional award winners and teams advancing to the grand final.
3. **Grand Final Review**: Winning teams from each region gather at the grand final for the final competition through extreme development and a global roadshow presentation. Final rankings are determined by a combination of judge scoring and public voting.

---

## 7. Participant Benefits and Awards

### Registration Benefits (For All Participants)

| Track Tool | Credit Allocation |
| :--- | :--- |
| **CodeBuddy / WorkBuddy** | 2,000 credits / person |
| **Miora** | 1,000 credits / person |

### Malaysia Winners
The top 10 campus-selected teams will present their projects at the Malaysia Demo Day.

| Award | Prize |
| :--- | :--- |
| **Top 1 Winning Team per Track** | Will receive 30,000 Credits |
| **Top 2 Winning Teams per Track** | Will be sponsored to represent Malaysia at the Grand Finals in Shenzhen.* |

*\*Travel expenses for each winning team participating in The International Grand Finals will be fully covered.*

### Grand Final Awards
The top 2 winning teams will represent Malaysia at the Grand Finals in Shenzhen, competing against international finalists for the grand prizes below:

| Award | Team Quota | Prize |
| :--- | :--- | :--- |
| **First Prize** | 1 | RMB 50,000 |
| **Second Prize** | 1 | RMB 30,000 |
| **Third Prize** | 1 | RMB 20,000 |

### Additional Benefits

| Benefit | Description |
| :--- | :--- |
| **Final Interview Fast Track** | Outstanding participants may enter the fast-track final interview process for Tencent IEG and CSIG internships. |
| **Project Support** | Outstanding projects may directly advance to the 2026 Tencent Game Creation Competition and may receive opportunities for investment, publishing, and incubation support. |
| **Official Certification** | An official Tencent Cloud certification certificate with a unique online verification code and lookup entry. |

---

## 8. Terms and Conditions

### Intellectual Property and Licensing
The intellectual property rights of the entries belong to the individual entrant or team. Entrants must guarantee that their entries are original and do not infringe upon any third-party rights.

Entrants grant the organizer (Tencent Cloud) a non-exclusive, royalty-free license to use the project name, description, demo screenshots / screencasts, and team information for non-commercial purposes, such as challenge promotion, case studies, and media coverage. The organizer will credit the project and team when using such materials.

### Privacy and Data Statement
The Organiser will collect and process the personal information submitted by participants (such as name, contact details and team information). Such information will be used solely for the purpose of event registration, judging, notifications, and related publicity or follow-up, and will not be used for unrelated purposes or disclosed to any unauthorised third party. Participants may request access to, correction of, or deletion of their personal information via the official contact channels.

---

*All the best for the Challenge — AI CAN DO IT!*
