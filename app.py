# Astra Resume Engine — Personalised for Lakshmi K (v1.1)
# US Senior Data Engineer Edition — "Top 5-10% of Applications"
# Built on the Astra v4.0 architecture (Charan edition), customised per Lakshmi's preferences.
# v1.1 patches: title-preservation, metric-provenance allowed-list, skills category validation,
# DR + tenant-support patterns, mandatory Terraform anchor, financial-services domain weight.
import streamlit as st
import json
import re
import io
import ast
import datetime
from typing import List
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
from xml.sax.saxutils import escape

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# API KEYS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
try:
    google_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    google_key = ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MODELS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GENERATION_MODEL = "gemini-3-flash-preview"
SCORING_MODEL = "gemini-3.1-flash-lite-preview"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAGE_TITLE = "Astra — Lakshmi K"
DEFAULT_TITLE = "Senior Data Engineer"
CONTACT_LINE = "+1 (469) 723-2320 | lakshmik3272@gmail.com | linkedin.com/in/lakshmi-k-19aa79330"
CANDIDATE_NAME = "Lakshmi K"

LAKSHMI_BASE_RESUME = """LAKSHMI K
Senior Data Engineer
+1 (469) 723-2320 | lakshmik3272@gmail.com | linkedin.com/in/lakshmi-k-19aa79330

Professional Summary
Senior Data Engineer with 5+ years of experience building scalable, high-performance data platforms across AWS, Azure, and GCP. Specialized in ETL/ELT pipelines, big data processing (Spark, Kafka), and cloud data warehousing. Proven track record of optimizing data workflows, reducing processing time, and enabling real-time analytics for business-critical applications.

Technical Skills
Cloud Platforms: AWS, Azure, GCP, Google Cloud Bigtable, Amazon S3, Google Cloud Storage.
Big Data Technologies: Apache Hadoop, Apache Spark, Apache Kafka, Apache Flink.
Data Warehousing: Amazon Redshift, Google BigQuery, Snowflake, Azure Synapse Analytics.
Database Technologies: SQL (MySQL, PostgreSQL, SQL Server, Oracle, MariaDB), NoSQL (MongoDB, DynamoDB).
ETL/ELT and Data Integration: Apache NiFi, AWS Glue, Azure Data Factory, Google Cloud Dataflow, Apache Airflow, dbt, Informatica, Talend.
Data Manipulation: Python (Pandas, NumPy, Matplotlib, Seaborn), PySpark.
Real-Time Data Processing: Apache Kafka, AWS Kinesis, Azure Event Hubs, Google Cloud Pub/Sub, Apache Flink.
Data Modeling: Star Schema, Snowflake Schema, Dimensional Modeling.
CI/CD & Automation: Jenkins, Azure DevOps, GitLab CI, AWS CodePipeline, Google Cloud Build, Terraform.
Business Intelligence & Analytics: Power BI, Tableau, Looker, Qlik, Excel.
Machine Learning & AI (Exposure): TensorFlow, PyTorch, Azure ML, AWS SageMaker, GCP Vertex AI.
Serverless: AWS Lambda, Google Cloud Functions, Azure Functions.
Infrastructure as Code: Terraform, CloudFormation, ARM Templates.
Monitoring & Logging: Prometheus, Grafana, ELK Stack, Splunk, CloudWatch, Stackdriver.
Containerization & Orchestration: Kubernetes, Docker, OpenShift, GKE, AKS, EKS.
Operating Systems: Linux, Unix.

Professional Experience

Azure Data Engineer | Northwestern Mutual | San Antonio, TX, USA | July 2024 - Present
- Architected and managed end-to-end ETL workflows using Azure Data Factory (ADF), integrating data from SQL Server, Cosmos DB, REST APIs, and ADLS, processing 500GB+ daily data.
- Designed and optimized data warehouse solutions using Azure Synapse Analytics and Azure SQL Database, improving query performance by 30%.
- Built and maintained real-time and batch data pipelines using Azure Databricks (PySpark), Azure Event Hubs, and Azure Stream Analytics, reducing data latency by 25%.
- Implemented Star and Snowflake schema data modeling to support Power BI reporting, improving reporting efficiency.
- Developed ETL processes using PySpark, SQL, and Hive, transforming structured and semi-structured data (JSON, Parquet) into curated datasets.
- Designed and deployed data lake solutions using ADLS Gen2 and Blob Storage, enabling scalable storage for high-volume data.
- Performed performance tuning on Azure SQL Database and Cosmos DB, improving throughput by 20% through indexing and partitioning strategies.
- Built event-driven data pipelines using Azure Functions and Logic Apps, improving workflow efficiency by 30%.
- Integrated multiple enterprise data sources using API-based ingestion frameworks.
- Loaded and transformed data into cloud data warehouses including Snowflake and BigQuery, supporting cross-platform analytics.
- Developed ADF pipeline deployment scripts (JSON) and reusable components, reducing deployment time by 20%.
- Created Linux/Unix shell scripts for automation and scheduling.
- Utilized Apache Kafka, Flume, and Zookeeper for real-time data streaming.
- Performed data validation and cleansing using Python (Pandas) and SQL.
- Collaborated with BI teams to deliver dashboards using Power BI and Synapse Analytics.
- Worked closely with data scientists to prepare datasets for machine learning models using Azure Databricks and Azure ML.

AWS Data Engineer | McKesson Corporation | Irving, TX, USA | August 2023 - May 2024
- Architected and managed end-to-end ETL workflows using AWS Glue, AWS Lambda, and Amazon Kinesis, integrating data from on-prem systems, Amazon RDS, Redshift, and S3, processing 400GB+ daily data.
- Built and maintained real-time data pipelines using Amazon Kinesis, AWS Lambda, and S3, enabling low-latency streaming analytics.
- Designed and implemented data lake architecture using Amazon S3 and AWS Data Lake, optimizing storage and reducing costs by 25%.
- Administered and optimized Amazon RDS, Redshift, and DynamoDB, improving query performance by 30% using partitioning, indexing, and query tuning.
- Developed and optimized data warehouse solutions using Amazon Redshift and AWS Glue.
- Automated data pipelines using AWS Lambda, Step Functions, and CloudWatch, reducing manual intervention by 30%.
- Built and orchestrated workflows using Apache Airflow.
- Developed real-time streaming applications using Apache Kafka and Spark Streaming.
- Monitored and troubleshot data pipelines using Splunk and CloudWatch.
- Integrated datasets for reporting using Amazon QuickSight, Redshift Spectrum, and Power BI.
- Collaborated with data scientists to prepare datasets for machine learning models using Amazon SageMaker, EMR, and AWS Glue.

GCP Data Engineer | Mindtree Limited (BigBasket) | Bengaluru, India | August 2021 - July 2022
- Architected and managed ETL workflows using GCP Dataflow and Dataproc (PySpark), integrating data from BigQuery, Cloud Storage, and on-prem systems, processing 300GB+ daily data.
- Administered and optimized Google BigQuery, Cloud SQL, and Cloud Spanner, improving query performance by 25% using partitioning, clustering, and query optimization.
- Designed and implemented data warehouse solutions using BigQuery, applying dimensional modeling (Star and Snowflake Schema).
- Built and maintained real-time data pipelines using Google Cloud Pub/Sub and Dataflow.
- Monitored system performance using Prometheus and Grafana, tracking CPU, memory, and pipeline throughput.
- Managed and optimized Google Cloud Storage and BigQuery datasets.
- Performed performance tuning on BigQuery and Cloud SQL.
- Integrated multiple data sources using Dataflow, Apache Beam, and Cloud Functions.
- Utilized Google Cloud Data Catalog for metadata management and data lineage tracking.
- Worked with BI teams to build reporting datasets using BigQuery, Looker, and Google Data Studio.
- Collaborated with data scientists to prepare datasets for ML models using GCP AI Platform and TensorFlow.

Data Engineer | Geeky Ants India Private Limited | Bengaluru, India | June 2020 - July 2021
- Architected and developed ETL pipelines using Apache Spark, Apache Kafka, and Apache Airflow.
- Managed and optimized relational and NoSQL databases including PostgreSQL, MySQL, and MongoDB.
- Implemented data security and access control mechanisms using AWS IAM and encryption techniques.
- Built and maintained real-time data processing pipelines using Apache Kafka and Spark Streaming.
- Automated data workflows using Apache Airflow and AWS Lambda, improving pipeline efficiency by 25%.
- Monitored data pipelines using CloudWatch, Prometheus, and Grafana.
- Integrated data with BI tools such as Power BI, Tableau, and Looker.
- Optimized data processing workflows using parallel processing and distributed computing with Apache Spark.
- Maintained code quality and deployment processes using Jenkins, Git, and CI/CD pipelines.

Data Engineer | Exide Energy Solutions Limited | Bengaluru, India | December 2019 - May 2020
- Designed and implemented big data processing pipelines using Apache Spark and Hadoop (HDFS, Hive) for large-scale data transformation.
- Set up and configured Hadoop and Spark clusters to process high-volume data (2TB+ datasets), enabling scalable distributed computing.
- Developed data ingestion and transformation workflows to load structured and unstructured data into enterprise data warehouse systems.
- Built and optimized Spark jobs for data processing, improving performance using parallel and distributed computing.
- Integrated data across multiple systems using Hive, HBase, and HDFS.
- Automated data workflows using Apache Oozie.
- Developed Python scripts for data extraction, transformation, and automation.
- Designed and implemented data models in MongoDB.
- Converted existing systems to serverless architecture using AWS Lambda and Kinesis.
- Provided production support and monitoring for data pipelines.
- Defined and maintained data governance standards.

Education
Lamar University — Master in Management Information Systems

Certifications
- AWS Certified Data Engineer — Associate (Aug 2025)
- AWS Certified Cloud Practitioner
- Google Cloud Certified — Professional Data Engineer
- Python (Google)
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DOMAIN VOCABULARY DICTIONARY
# Used to inject domain-specific framing into bullets without inventing experience.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DOMAIN_VOCAB = {
    "financial": "regulatory reporting, trading data feeds, risk analytics, transaction processing, audit trails, real-time financial insights, SOX-aligned data lineage",
    "fintech": "payments data, transaction streams, fraud signals, ledger reconciliation, real-time risk scoring",
    "insurance": "actuarial datasets, policy data, claims pipelines, underwriting analytics, regulatory reporting feeds",
    "healthcare": "HIPAA-aligned pipelines, clinical data, patient records, EHR integration, claims processing, pharmacy datasets, PHI-safe storage",
    "retail": "customer 360 datasets, transaction data, inventory feeds, demand signals, recommendation features, omnichannel analytics",
    "ecommerce": "order pipelines, catalogue data, recommendation features, customer behavior streams, marketplace analytics",
    "energy": "IoT telemetry, sensor data, grid analytics, asset performance, SCADA feeds, predictive maintenance datasets",
    "ad-tech": "impression data, attribution pipelines, real-time bidding feeds, audience segmentation, campaign analytics",
    "telecom": "CDR processing, network telemetry, subscriber analytics, billing pipelines",
    "logistics": "route optimization data, fleet telemetry, supply-chain visibility, shipment tracking",
    "media": "content metadata, viewership analytics, recommendation pipelines, ad-serving telemetry",
    "general": "",
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SKILL CATEGORY CAPS — credible 5-year breadth limits
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SKILL_CATEGORY_CAPS = {
    "cloud": 4,
    "big data": 4,
    "warehousing": 4,
    "warehouse": 4,
    "database": 5,
    "etl": 4,
    "elt": 4,
    "integration": 4,
    "stream": 4,
    "real-time": 4,
    "data modeling": 3,
    "modeling": 3,
    "ci/cd": 4,
    "devops": 4,
    "automation": 4,
    "reporting": 3,   # her explicit ask
    "bi": 3,
    "intelligence": 3,
    "analytics": 3,
    "ml": 3,
    "ai": 3,
    "serverless": 3,
    "iac": 3,
    "infrastructure": 3,
    "monitoring": 3,
    "logging": 3,
    "container": 3,
    "orchestration": 3,
    "programming": 3,
    "language": 3,
    "data manipulation": 3,
    "operating": 2,
}
DEFAULT_CAP = 4

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ASTRA PROMPT — Title-Match Engine + Domain Mapping + Bullet Engine
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ASTRA_PROMPT = """
Role: You are Astra, an elite resume tailoring engine for Lakshmi K. Your job: place this candidate in the top 5–10% of applications for the target role.

Candidate: Lakshmi K — Senior Data Engineer with 5+ years across 5 roles. US-based (Texas).
- Northwestern Mutual (Insurance / Azure DE / current): ADF, Synapse, Databricks, Event Hubs, 500GB+/day
- McKesson Corporation (Healthcare / AWS DE): Glue, Lambda, Kinesis, Redshift, S3, 400GB+/day
- Mindtree (BigBasket) (Retail/E-commerce / GCP DE): Dataflow, BigQuery, Pub/Sub, 300GB+/day
- Geeky Ants (Tech Services / Multi-tool DE): Spark, Kafka, Airflow
- Exide Energy (Energy / Big Data DE): Hadoop, Spark, 2TB+ datasets

Target seniority: Senior (5+ yrs).

=== STEP 1 — TITLE-MATCH ROUTING (DO THIS FIRST) ===
Detect the JD's role title. Compare with Lakshmi's current Azure Data Engineer identity.

BRANCH A — TITLE MATCHES (JD title is "Data Engineer", "Senior Data Engineer", "Cloud Data Engineer", "Azure/AWS/GCP Data Engineer", "ETL Engineer", "Big Data Engineer", or close variant):
- Apply the 90% Rule: align bullets deeply with the JD. Surface every JD requirement she can credibly support from her real history.
- Identity is implicit, no need to defend it.

BRANCH B — TITLE DIFFERS (JD title is "Software Engineer (Data)", "Database Engineer", "Platform Engineer", "Data Architect", "Analytics Engineer", "ML Engineer", "DataOps", or anything else):
- Apply the 20/80 Rule: 20% of bullets across the resume preserve her Azure DE identity (anchor bullets — typical DE work like ADF orchestration, Synapse warehousing, Databricks PySpark). 80% of bullets translate her real work into the JD's vocabulary.
- Example: JD "Database Engineer" → 80% of bullets emphasize SQL Server / Cosmos DB / Redshift / BigQuery / Cloud SQL / partitioning / indexing / query tuning / replication / HA — using her actual database administration work as raw material.
- Example: JD "Software Engineer, Data" → 80% emphasize software-engineering practice: code quality, CI/CD, testing, modular pipeline design, API integration, system reliability.
- Never fabricate. Use only what she has actually done; reframe the framing.

State the routing decision in your output as "target_company" + summary phrasing — but DO NOT print "Branch A" or "Branch B" anywhere user-facing.

=== STEP 1.5 — EMPLOYMENT TITLE PRESERVATION (CRITICAL — NEVER FABRICATE) ===
The role_title field for each experience item MUST exactly match the source resume:
- Northwestern Mutual: "Azure Data Engineer"
- McKesson Corporation: "AWS Data Engineer"
- Mindtree Limited (BigBasket): "GCP Data Engineer"
- Geeky Ants India Private Limited: "Data Engineer"
- Exide Energy Solutions Limited: "Data Engineer"

These are immutable historical fact. US recruiters verify titles via LinkedIn and background-check firms (The Work Number, HireRight). Rewriting employment titles is resume falsification and can disqualify the candidate.

ONLY the candidate_title field (the line under the name in the header) reflects the JD's role language. That's the *target role*, not employment history.

DO NOT inject "Platform", "Cloud", "Senior", "Big Data", "Lead", or any other modifier into the per-role employment titles. They stay verbatim from the source.

=== STEP 2 — INDUSTRY DETECTION + DOMAIN MAPPING ===
Detect the JD's industry: financial, fintech, insurance, healthcare, retail, ecommerce, energy, ad-tech, telecom, logistics, media, or general.

DOMAIN VOCABULARY (inject where it fits without lying):
- financial / fintech / wealth-management / brokerage: regulatory reporting, trading data feeds, brokerage data, wealth-management analytics, transaction streams, audit trails, real-time financial insights, SOX-aligned data lineage, PII safeguards on customer financial data, regulated trading platforms
- insurance: actuarial datasets, policy data, claims pipelines, underwriting analytics
- healthcare: HIPAA-aligned, clinical data, EHR integration, claims processing, pharmacy datasets
- retail / ecommerce: customer 360, transaction data, inventory feeds, demand signals, recommendation features
- energy: IoT telemetry, sensor data, grid analytics, SCADA feeds
- ad-tech: impression data, attribution, real-time bidding, audience segmentation
- telecom: CDR processing, network telemetry, subscriber analytics
- logistics: route optimization, fleet telemetry, supply-chain visibility
- media: content metadata, viewership analytics

DOMAIN HONESTY RULE:
- Lakshmi has worked in: Insurance / Financial Services (Northwestern Mutual is a Fortune 100 insurance + investment management firm — this counts as financial-services experience), Healthcare (McKesson), Retail/E-commerce (BigBasket), Tech Services (Geeky Ants, Mindtree), Energy (Exide).
- If JD industry is financial / wealth-management / brokerage / fintech (Schwab, Fidelity, Vanguard, JPMorgan, etc.) → claim financial-services tenure DIRECTLY via Northwestern Mutual. Do NOT frame Northwestern Mutual as "transferable from healthcare" — that under-sells her actual financial-services years.
- If JD industry MATCHES one she has lived → claim it directly in summary ("4 years across regulated financial-services and healthcare data platforms…").
- If JD industry is DIFFERENT (e.g., ad-tech, telecom) → frame as transferable in summary, but inject the JD's domain vocabulary into specific bullets where it fits naturally. Never claim "5 years in ad-tech" if she hasn't done it.

For Schwab / wealth-management / brokerage JDs SPECIFICALLY:
- Summary must emphasize: regulated financial-services environments, auditability, PII safeguards, financial reporting cadence, multi-region resilience.
- Lead with Northwestern Mutual as a financial-services anchor, not as insurance-only.

=== STEP 3 — BULLET PHRASING ENGINE (THE 4 RULES) ===
Every bullet must satisfy ALL of these:

RULE A — WHY IT MATTERS (mandatory pattern):
[strong verb] + [what was built/solved] + [scale or scope] + [outcome: improved X by Y%, OR enabled business outcome]
- Bad: "Architected end-to-end ETL workflows."
- Good: "Architected end-to-end ETL workflows in Azure Data Factory ingesting 500GB/day, cutting downstream reporting latency by 25% and enabling near real-time financial insights."

RULE B — ANTI-REPETITION:
- Track verb usage across all 5 roles. Same responsibility (e.g., "built data pipelines") MUST be re-phrased per role with domain-specific framing.
- Verb pool — rotate, never repeat in adjacent bullets within one role: built, architected, designed, engineered, shipped, delivered, developed, productionized, stood up, refactored, migrated, hardened, tuned, automated, orchestrated, integrated, scaled.
- Don't open three bullets in a row with the same verb.

RULE C — ANTI-TOOL-STACKING:
- Maximum 1–2 tools per bullet. Never "worked on Spark, Kafka, Power BI, and Airflow" — that's a red flag of inflated experience.
- Each tool gets its own context. If multiple tools were used, split into separate bullets.

RULE D — QUANTIFY OR SKIP:
- Every bullet MUST end in a number, scale reference, or concrete business outcome (500GB/day, 30% latency cut, 5-second SLA, Tier-1 reporting hours, 200+ Power BI dashboards).
- If a bullet has no metric and no concrete outcome, drop it or merge it.

=== STEP 4 — ACHIEVEMENTS FORMAT (DELTA RULE) ===
Achievements section per role uses BEFORE-TO-AFTER format whenever the source data supports it.
- Preferred: "Cut Synapse query latency from ~12s to ~7s on 500GB datasets."
- Acceptable when no baseline exists: "Achieved 30% throughput gain on Azure SQL workloads."
- FORBIDDEN: inventing a baseline. If source says "improved by 30%", DO NOT make up "from 70% to 91%". Use only what's in the source resume.

=== STEP 5 — SKILLS COMPRESSION (CREDIBLE 5-YEAR BREADTH) ===
DO NOT copy all skills from the source resume. The source over-stacks.

CATEGORY CONTENT VALIDATION (HARD RULES — never scramble):
Each tool belongs in EXACTLY ONE category. Misplacing a tool is a hard failure.

- Cloud Platforms: AWS, Azure, GCP / Google Cloud Platform (the cloud names themselves only — not services)
- Compute & Serverless: EC2, Compute Engine, Cloud Run, Cloud Functions, AWS Lambda, Azure Functions
- Data Warehousing: BigQuery, Snowflake, Amazon Redshift, Azure Synapse Analytics
- Big Data & Processing: Apache Spark, PySpark, Apache Hadoop, Databricks, Dataproc, EMR, Apache Flink, Apache Beam, Hive
- Streaming & Messaging: Apache Kafka, AWS Kinesis, Azure Event Hubs, Google Cloud Pub/Sub, Kafka Connect
- Orchestration & ETL: Apache Airflow, Cloud Composer, Azure Data Factory, AWS Glue, Google Cloud Dataflow, Apache NiFi, Step Functions, Logic Apps, dbt, Cloud Scheduler, Apache Oozie
- Database Technologies: SQL Server, MySQL, PostgreSQL, Oracle, MariaDB, Cosmos DB, MongoDB, DynamoDB, Cloud SQL, Cloud Spanner, RDS, Bigtable, HBase
- Cloud Storage: S3, ADLS Gen2, Azure Blob, Google Cloud Storage, HDFS
- IaC & DevOps: Terraform, CloudFormation, ARM Templates, Google Cloud Deployment Manager, Azure DevOps, Jenkins, GitLab CI, AWS CodePipeline, Google Cloud Build, Git
- Networking & Security: VPC, Subnets, Firewalls, IAM, Cloud Armor, Security Groups, KMS
- Containers & Orchestration: Docker, Kubernetes, OpenShift, GKE, AKS, EKS
- Monitoring & Observability: Prometheus, Grafana, ELK Stack, Splunk, CloudWatch, Stackdriver, Azure Monitor
- Programming: Python, SQL, PySpark, Linux Shell Scripting
- BI & Reporting: Power BI, Tableau, Looker, QuickSight, Google Data Studio, Qlik
- ML/AI (Exposure only — include only if JD asks): TensorFlow, PyTorch, Azure ML, AWS SageMaker, GCP Vertex AI

VALIDATION CHECK before writing skills output: confirm every tool is in its correct category above. A database in "Monitoring", or a warehouse in "Streaming", is rejected.

Output 6–8 dense skill categories with these caps:
- Cloud Platforms: max 4 (her 3 clouds + JD's cloud if different)
- Big Data Technologies: max 4
- Data Warehousing: max 4
- Database Technologies: max 5
- ETL/ELT & Integration: max 4
- Streaming & Real-Time: max 4
- Reporting & BI: MAX 3 (her explicit ask — never more)
- CI/CD & IaC: max 4
- Containers & Orchestration: max 3
- Monitoring & Observability: max 3
- Programming: max 3
- ML/AI (Exposure): max 3 — only include if JD asks; otherwise drop the category

ORDERING within each category: JD-mentioned tools FIRST, then her strongest, then drop the rest.
Tools she has but JD doesn't ask for and aren't core (e.g., Talend, Informatica, OpenShift) get suppressed unless the JD asks for them.

=== STEP 6 — SUMMARY ENGINE (4 sentences, never generic) ===
1. Unique opener — NOT "Data Engineer with 5+ years…". Lead with a specific capability or scale fact.
   - Good: "Senior Data Engineer who has shipped production data platforms across all three major clouds — AWS, Azure, and GCP — currently moving 500GB/day at Northwestern Mutual."
   - Bad: "Highly motivated Data Engineer with 5+ years of experience…"
2. Multi-cloud differentiator + technical depth (Spark/Kafka/Airflow at scale, warehousing, streaming).
3. Domain bridge — claim the industry directly if she has it; frame as transferable if she doesn't.
4. JD hook — name the target company and reflect their stated stack/problem.

BANNED summary openers (never use any of these): "Highly motivated", "Results-driven", "Passionate", "Dedicated professional", "Detail-oriented", "Seasoned", "Dynamic professional", "Innovative thinker", "Experienced professional".

=== ANTI-AI-WRITING RULES (LOCKED — sounds human, not robot) ===
BANNED words and phrases anywhere in the resume:
- "leveraging", "harnessing", "utilizing" → use "using" or "with"
- "seamless", "robust" (overused), "innovative" (meaningless), "groundbreaking", "cutting-edge", "state-of-the-art", "best-in-class"
- "testament to", "underscores", "pivotal", "realm", "tapestry", "landscape", "at the intersection of", "at the forefront of"
- "showcasing", "highlighting", "demonstrating", "underscoring", "fostering", "cultivating", "spearheading" (unless already in source)
- "passionate about", "driven by", "committed to excellence"
- "serves as", "stands as", "functions as" — use "is"
- "ensuring alignment", "ensuring seamless"
- "worked on" → use a real verb (built, owned, ran, shipped)
- "various", "multiple", "numerous" → specify the number or drop the word
- "end-to-end" → allowed once per resume MAX

WRITING STYLE:
- Vary sentence length. Mix short punchy lines with longer ones.
- No em dashes (—) inside bullets. Use commas or periods.
- No three-adjective chains: "scalable, reliable, and efficient" → pick ONE.
- Past tense for all prior roles. Present tense ONLY for current role at Northwestern Mutual.
- Active voice. No first-person pronouns.

=== METRIC PROVENANCE — STRICT ALLOWED-LIST (CRITICAL) ===
Every percentage, ratio, GB/TB volume, or quantitative claim in the output MUST trace to the source resume. The COMPLETE allowed-metrics list:

NORTHWESTERN MUTUAL: 500GB+/day, 30% (query perf), 25% (latency), 20% (throughput), 30% (workflow efficiency), 20% (deployment time)
MCKESSON: 400GB+/day, 25% (storage cost), 30% (query perf), 30% (manual intervention)
MINDTREE / BIGBASKET: 300GB+/day, 25% (query perf)
GEEKY ANTS: 25% (pipeline efficiency)
EXIDE: 2TB+ datasets

ANY OTHER NUMBER IS FORBIDDEN. Examples of inventions that have already caused failures and MUST NEVER appear:
- "Reduced unauthorized access by 40%" — 40% is not in source → FORBIDDEN
- "Maintained 99.9% availability" — 99.9% is not in source → FORBIDDEN
- "Reduced costs by 15%" — 15% is not in source → FORBIDDEN
- "Improved by 35%" when source says 30% — exact source numbers only → FORBIDDEN
- Any RPO/RTO number (e.g., "RTO of 4 hours") — not in source → FORBIDDEN
- Any ticket count, SLA time, response time, uptime % — not in source → FORBIDDEN
- Any customer count, transaction-per-second figure, dataset-row count — not in source → FORBIDDEN

If an achievement bullet has no source metric to anchor it, write a QUALITATIVE achievement instead — never invent a number to fill a slot.

ACCEPTABLE qualitative achievement patterns (no metric needed):
- "Strengthened IAM posture by replacing role-wide grants with scoped service-account policies"
- "Cut on-call escalations by introducing pre-deployment validation in CI/CD"
- "Stabilized the streaming layer by isolating Kafka consumer groups per tenant"
- "Hardened cross-region replication by adopting paired-region storage and tested failover playbooks"

QUANTITATIVE bullets stay only when the metric exists in the allowed-list above. Do not split, merge, or massage source metrics into new ratios.

=== STEP 7 — KEYWORD HARVESTING + EQUIVALENT TOOL BRIDGING ===
Extract every hard skill, tool, framework from the JD. Each must appear at least once in skills or bullets.
Equivalent-tool bridging (add the JD's tool alongside her actual tool):
- JD says "Databricks" + she has Synapse/EMR → add Databricks (she has it at Northwestern Mutual)
- JD says "MLflow" + she has Azure ML → add MLflow if reasonable
- JD says "Snowflake" + she has it → keep prominent
- JD says "Prefect/Dagster" + she has Airflow → add alongside Airflow
- JD says "Fivetran" + she has Glue/ADF → add Fivetran category
- JD says "dbt Cloud" + she has dbt → upgrade to "dbt Cloud"
- JD says "Kafka Connect" + she has Kafka → add "Kafka Connect"

=== STEP 8 — DR + TENANT SUPPORT FRAMINGS (USE ONLY IF JD ASKS + SOURCE IMPLIES) ===
TRIGGER (DR): Use only if JD calls out "Disaster Recovery", "BCP", "failover", "RTO", "RPO", "backup recovery", or "resilience exercises".
TRIGGER (tenant): Use only if JD calls out "tenant tickets", "platform support", "on-call", "incident response", "troubleshoot tenant issues", or "ServiceNow / Jira ticketing".

If triggered AND the source resume has matching signals (production support, monitoring, troubleshooting, BI partnership, data governance), include ONE of these bullets in the role with the strongest signal:

DR bullet candidates (pick ONE, anchor in NWM or McKesson):
- "Participated in disaster-recovery validation for Synapse warehouses, verifying recovery objectives across paired Azure regions"
- "Supported BCP exercises by validating cross-region replication for Redshift datasets and S3 lifecycle policies"
- "Tested cross-region failover playbooks for Cloud SQL and BigQuery with the platform reliability team"

Tenant-support bullet candidates (pick ONE):
- "Resolved platform tickets from data engineering and BI tenants, troubleshooting query performance and access issues across Synapse and Power BI"
- "Provided production support for Glue and Redshift workloads, partnering with cross-functional teams to minimize disruption"
- "Triaged data-platform incidents and resolved tenant-reported issues in collaboration with cloud and security teams"

HARD RULES for these bullets:
- NEVER invent ticket counts, SLA times, RTO/RPO numbers, response times, or uptime percentages.
- NEVER stack DR or tenant bullets across multiple roles. Use ONCE if at all.
- If the JD does not mention DR or tenant support, do NOT add these bullets.

=== STEP 9 — TERRAFORM BULLET REQUIREMENT (WHEN JD CALLS OUT IaC) ===
TRIGGER: JD mentions Terraform, IaC, "Infrastructure as Code", Cloud Deployment Manager, CloudFormation, ARM Templates, or "infrastructure automation".

If triggered, Terraform MUST appear in at least ONE responsibility bullet (skills section alone is insufficient — ATS keyword density rules require it in the bullet text).

Anchor candidates (pick ONE, max TWO; never all three — that reads as inflated):
1. PRIMARY anchor (best for Schwab / GCP-heavy JDs): Mindtree / BigBasket
   - "Provisioned BigQuery datasets, Pub/Sub topics, and Cloud SQL instances using Terraform with GCS-backed state"
2. Secondary anchor: Northwestern Mutual
   - "Provisioned Azure Synapse, ADLS Gen2, and Cosmos DB resources via Terraform modules with version-controlled state"
3. Tertiary anchor: McKesson
   - "Managed S3, Glue, and Redshift resource provisioning via Terraform-backed CI/CD pipelines"

Do NOT use generic phrasing like "leveraged Terraform" or "utilized IaC". Be specific about which resources.

=== STEP 10 — STRUCTURE REQUIREMENTS ===
Sections in this order:
1. Header (NAME, role title, contact line — NO LOCATION)
2. Professional Summary
3. Technical Skills (6–8 compressed categories)
4. Professional Experience (ALL 5 roles, never drop any; current role first)
5. Education (Lamar University — Master in MIS)
6. Certifications (4 certs; the JD-relevant cert sorts to top)

Per role: 5–8 responsibilities + 2–3 achievements (delta format).

=== CONTACT INFO (LOCKED) ===
Name: Lakshmi K
Contact line: +1 (469) 723-2320 | lakshmik3272@gmail.com | linkedin.com/in/lakshmi-k-19aa79330
NEVER include location in the header.

=== TARGET ROLE TITLE ===
Use the exact JD title in the role line under the name (e.g., "Senior Data Engineer", "Cloud Data Engineer", "Azure Data Engineer"). Default to "Senior Data Engineer" if JD title is unusual.
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# COVER LETTER PROMPT — US tone, 5 war stories
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COVER_LETTER_PROMPT = """
Role: You are Lakshmi K writing a direct email to a Hiring Manager in the US market.
Goal: Sound 100% human. Get a response.

BANNED PHRASES — never use any of these:
"I am writing to express my interest", "I am excited to apply", "Please find my resume attached",
"I believe I am a perfect fit", "passionate about", "driven by a desire", "committed to excellence",
"at the forefront of", "showcasing", "highlighting", "demonstrating", "serves as", "stands as",
"leveraging", "harnessing", "utilizing", "seamless", "innovative", "groundbreaking",
"testament to", "underscores", "pivotal", "realm", "tapestry"

DOMAIN HONESTY:
- She has lived in: Insurance (Northwestern Mutual), Healthcare (McKesson), Retail/E-commerce (BigBasket), Tech Services (Geeky Ants, Mindtree), Energy (Exide).
- If JD industry matches one of these, claim it directly. If not, frame as transferable.
- Never claim "5 years in [their industry]" unless she has actually lived it.

THE OPENING: Start with a specific observation about the company's data challenge from the JD. NEVER start with "I am applying for..."
- Bad: "I am applying for the Data Engineer role at CompanyX."
- Good: "Moving 500GB/day across three clouds while keeping streaming latency under five seconds is a quiet kind of hard — and from your job posting, that's the exact problem CompanyX is solving."

THE WAR STORY — pick the BEST matching story based on JD industry + stack:
1. NORTHWESTERN MUTUAL (Insurance / Azure / scale): "At Northwestern Mutual, I architected ADF pipelines moving 500GB/day from SQL Server, Cosmos DB, and REST APIs into Synapse, cutting query latency by 30% and pulling Power BI dashboards into near real-time."
2. MCKESSON (Healthcare / AWS / cost): "At McKesson, I rebuilt the data lake on S3 with Glue and Lambda, dropping storage cost by 25% while keeping 400GB/day of healthcare data flowing into Redshift."
3. MINDTREE/BIGBASKET (Retail / GCP / streaming): "At BigBasket, I built Pub/Sub plus Dataflow streaming feeds into BigQuery, processing 300GB/day of retail transaction data with dimensional models powering Looker dashboards."
4. GEEKY ANTS (Multi-tool / mid-career proof): "At Geeky Ants, I shipped Spark + Kafka + Airflow ETL pipelines across PostgreSQL, MongoDB, and AWS, lifting pipeline efficiency by 25%."
5. EXIDE ENERGY (Energy / scale): "At Exide, I configured Hadoop and Spark clusters for 2TB+ datasets, building distributed processing for energy operational data and HBase storage."

WRITING STYLE:
- Short sentences mixed with longer ones. Vary the rhythm.
- No em dashes inside paragraphs.
- No three-adjective chains.
- Sound like a senior engineer talking, not a press release.

STRUCTURE:
1. "Dear Hiring Manager,"
2. Hook (their data pain point from JD — be specific about the cloud, scale, or stack they mentioned)
3. Bridge: "This is close to a problem I solved at [Company]…"
4. War story with specific tools and numbers
5. Brief closing tying her cross-cloud breadth to their team. End with "Thank you,\nLakshmi K"

Return ONLY the letter body. No markdown. No bold. No headers.
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ATS SCORING PROMPT — adds title-match + domain-coverage dimensions
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ATS_SCORING_PROMPT = """You are a strict ATS (Applicant Tracking System) scanner for a US Senior Data Engineer.
Compare the RESUME JSON against the JOB DESCRIPTION.

Scoring criteria (0-100):
- Keyword density (35%): What % of JD hard skills/tools appear in the resume?
- Experience relevance (25%): Do bullets describe work that solves the JD's problems?
- Title-match alignment (15%): Does the candidate role line + summary phrasing reflect the JD's title language correctly?
- Domain-vocabulary density (10%): Do bullets carry JD-industry framing where natural?
- Seniority alignment (10%): Does the experience level (5+ yrs Senior DE) match what JD asks for?
- Honesty check (5%): Penalty if resume claims industry experience the candidate doesn't have.

Output ONLY valid JSON, no markdown, no backticks, no explanation:
{"score": <int 0-100>, "reasoning": "<1 sentence>", "missing_keywords": "<comma-separated JD keywords NOT in resume>", "title_match_status": "<match | partial | mismatch>", "domain_coverage": "<strong | adequate | weak>"}
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. PYDANTIC SCHEMAS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class ExperienceItem(BaseModel):
    role_title: str = Field(description="Job title exactly as it should appear, e.g., 'Azure Data Engineer'")
    company: str = Field(description="Company name")
    dates: str = Field(description="Employment dates, e.g., 'July 2024 - Present'")
    location: str = Field(description="City, State (US) or City, Country")
    responsibilities: List[str] = Field(description="5-8 bullet points reframed for the JD per the 4 bullet rules")
    achievements: List[str] = Field(description="2-3 quantified achievements; use BEFORE-TO-AFTER format where source data allows")

class EducationItem(BaseModel):
    degree: str = Field(description="Full degree name")
    college: str = Field(description="University name")

class Certification(BaseModel):
    name: str = Field(description="Full certification name")
    year: str = Field(description="Year or year+month if known; empty string if unknown")

class SkillCategory(BaseModel):
    category: str = Field(description="Skill category name, e.g., 'Cloud Platforms'")
    technologies: str = Field(description="Comma-separated tools, capped per category, JD-mentioned tools FIRST")

class ResumeSchema(BaseModel):
    candidate_name: str = Field(description="Always: Lakshmi K")
    candidate_title: str = Field(description="Role title tailored to JD; default 'Senior Data Engineer'")
    contact_info: str = Field(description="Always: +1 (469) 723-2320 | lakshmik3272@gmail.com | linkedin.com/in/lakshmi-k-19aa79330")
    summary: str = Field(description="4-sentence summary; unique opener, multi-cloud differentiator, domain bridge, JD hook")
    skills: List[SkillCategory] = Field(description="6-8 compressed skill categories; respect category caps")
    experience: List[ExperienceItem] = Field(description="ALL 5 roles in reverse chronological order. Never drop any.")
    education: List[EducationItem] = Field(description="Lamar University — Master in MIS")
    certifications: List[Certification] = Field(description="4 certs; JD-relevant cert sorts to top")
    target_company: str = Field(description="Company name extracted from JD")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SCHEMA CLEANER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def get_clean_schema(pydantic_cls):
    schema = pydantic_cls.model_json_schema()
    def _clean(d):
        if isinstance(d, dict):
            for key in ["additionalProperties", "title"]:
                d.pop(key, None)
            for v in d.values():
                _clean(v)
        elif isinstance(d, list):
            for item in d:
                _clean(item)
    _clean(schema)
    return schema

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. DATA NORMALIZER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def clean_skill_string(skill_str):
    if not isinstance(skill_str, str):
        return str(skill_str)
    if skill_str.strip().startswith("["):
        try:
            list_match = re.search(r"\[(.*?)\]", skill_str)
            if list_match:
                actual_list = ast.literal_eval(list_match.group(0))
                extra_part = skill_str[list_match.end():].strip().lstrip(",").strip()
                clean_str = ", ".join([str(s) for s in actual_list])
                if extra_part:
                    clean_str += f", {extra_part}"
                return clean_str
        except Exception:
            pass
    return skill_str

def normalize_schema(data):
    if not isinstance(data, dict):
        return {"summary": str(data), "skills": {}, "experience": []}
    normalized = {}
    normalized['candidate_name'] = data.get('candidate_name', CANDIDATE_NAME)
    normalized['candidate_title'] = data.get('candidate_title', DEFAULT_TITLE)
    raw_contact = data.get('contact_info', CONTACT_LINE)
    normalized['contact_info'] = str(raw_contact) if not isinstance(raw_contact, dict) else ' | '.join(str(v) for v in raw_contact.values() if v)
    normalized['summary'] = data.get('summary', '')

    # Skills → always dict
    raw_skills = data.get('skills', {})
    normalized['skills'] = {}
    if isinstance(raw_skills, dict):
        for k, v in raw_skills.items():
            normalized['skills'][k] = clean_skill_string(str(v))
    elif isinstance(raw_skills, list):
        for item in raw_skills:
            if isinstance(item, dict):
                cat = item.get('category', '')
                tech = item.get('technologies', '')
                if cat and tech:
                    normalized['skills'][cat] = clean_skill_string(str(tech))
            else:
                normalized['skills'] = {"General": ", ".join([str(s) for s in raw_skills])}
                break

    # Experience
    raw_exp = data.get('experience', [])
    norm_exp = []
    if isinstance(raw_exp, list):
        for role in raw_exp:
            if isinstance(role, dict):
                norm_exp.append({
                    'role_title': role.get('role_title', ''),
                    'company': role.get('company', ''),
                    'dates': role.get('dates', ''),
                    'location': role.get('location', ''),
                    'responsibilities': role.get('responsibilities', []),
                    'achievements': role.get('achievements', []),
                })
    normalized['experience'] = norm_exp

    # Education
    raw_edu = data.get('education', [])
    norm_edu = []
    if isinstance(raw_edu, list):
        for edu in raw_edu:
            if isinstance(edu, dict):
                norm_edu.append({
                    'degree': edu.get('degree', ''),
                    'college': edu.get('college', ''),
                })
            elif isinstance(edu, str):
                norm_edu.append({'degree': edu, 'college': ''})
    elif isinstance(raw_edu, str):
        norm_edu.append({'degree': raw_edu, 'college': ''})
    if not norm_edu:
        norm_edu = [{'degree': 'Master in Management Information Systems', 'college': 'Lamar University'}]
    normalized['education'] = norm_edu

    # Certifications
    raw_certs = data.get('certifications', [])
    norm_certs = []
    if isinstance(raw_certs, list):
        for cert in raw_certs:
            if isinstance(cert, dict):
                norm_certs.append({
                    'name': cert.get('name', ''),
                    'year': cert.get('year', ''),
                })
            elif isinstance(cert, str):
                norm_certs.append({'name': cert, 'year': ''})
    if not norm_certs:
        norm_certs = [
            {'name': 'AWS Certified Data Engineer — Associate', 'year': 'Aug 2025'},
            {'name': 'AWS Certified Cloud Practitioner', 'year': ''},
            {'name': 'Google Cloud Certified — Professional Data Engineer', 'year': ''},
            {'name': 'Python (Google)', 'year': ''},
        ]
    normalized['certifications'] = norm_certs

    normalized['target_company'] = data.get('target_company', 'Company')
    return normalized

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. ATS SCORING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def calculate_ats_score(resume_json, jd_text, api_key):
    if not api_key:
        return {"score": 0, "reasoning": "No API Key", "missing_keywords": "", "title_match_status": "unknown", "domain_coverage": "unknown"}
    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(
            model=SCORING_MODEL,
            contents=f"{ATS_SCORING_PROMPT}\n\nRESUME:\n{str(resume_json)[:3500]}\n\nJOB DESCRIPTION:\n{jd_text[:3500]}",
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        content = response.text.strip()
        if "```" in content:
            match = re.search(r"```(?:json)?(.*?)```", content, re.DOTALL)
            if match:
                content = match.group(1).strip()
        return json.loads(content)
    except Exception as e:
        return {"score": 0, "reasoning": f"Scoring Error: {str(e)}", "missing_keywords": "", "title_match_status": "unknown", "domain_coverage": "unknown"}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. SKILLS COMPRESSION (replaces Charan's expand_skills_dense)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def get_cap_for_category(cat_name):
    cat_lower = cat_name.lower()
    for keyword, cap in SKILL_CATEGORY_CAPS.items():
        if keyword in cat_lower:
            return cap
    return DEFAULT_CAP

def compress_skills_credibly(skills, jd_text=""):
    """Cap each category at credible 5-year breadth; sort JD-mentioned tools first."""
    if not skills:
        return {}
    jd_lower = jd_text.lower() if jd_text else ""
    compressed = {}
    for cat, tools_str in skills.items():
        if not tools_str or not str(tools_str).strip():
            continue
        tools_list = [t.strip().rstrip('.') for t in str(tools_str).split(",") if t.strip()]
        # Dedupe while preserving order
        seen = set()
        deduped = []
        for t in tools_list:
            t_norm = t.lower()
            if t_norm not in seen:
                seen.add(t_norm)
                deduped.append(t)
        # Sort: JD-mentioned first (stable sort)
        if jd_lower:
            deduped.sort(key=lambda t: 0 if t.lower() in jd_lower else 1)
        cap = get_cap_for_category(cat)
        compressed[cat] = ", ".join(deduped[:cap])
    return compressed

def to_text_block(val):
    if val is None:
        return ""
    if isinstance(val, list):
        return "\n".join([str(x) for x in val])
    return str(val)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. GENERATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def analyze_and_generate(api_key, resume_text, jd_text):
    client = genai.Client(api_key=api_key)
    try:
        safe_schema = get_clean_schema(ResumeSchema)
        response = client.models.generate_content(
            model=GENERATION_MODEL,
            contents=f"{ASTRA_PROMPT}\n\nSOURCE RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{jd_text}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=safe_schema,
            )
        )
        raw_data = json.loads(response.text)
        data = raw_data.model_dump() if hasattr(raw_data, 'model_dump') else raw_data
        # Skills list → dict
        if 'skills' in data and isinstance(data['skills'], list):
            transformed = {}
            for item in data['skills']:
                cat = item.get('category') if isinstance(item, dict) else getattr(item, 'category', '')
                tech = item.get('technologies') if isinstance(item, dict) else getattr(item, 'technologies', '')
                if cat and tech:
                    transformed[cat] = tech
            data['skills'] = transformed
        data = normalize_schema(data)
        # Apply skills compression as a final guardrail (in case the model over-stacks)
        data['skills'] = compress_skills_credibly(data.get('skills', {}), jd_text)
        # ATS scoring
        judge = calculate_ats_score(data, jd_text, api_key)
        data['ats_score'] = judge.get('score', 0)
        data['ats_reason'] = judge.get('reasoning', '')
        data['missing_keywords'] = judge.get('missing_keywords', '')
        data['title_match_status'] = judge.get('title_match_status', 'unknown')
        data['domain_coverage'] = judge.get('domain_coverage', 'unknown')
        return data
    except Exception as e:
        return {"error": f"Generation Error: {str(e)}"}

def generate_cover_letter(api_key, resume_data, jd_text):
    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(
            model=GENERATION_MODEL,
            contents=f"{COVER_LETTER_PROMPT}\n\nRESUME DATA:\n{str(resume_data)}\n\nJOB DESCRIPTION:\n{jd_text}",
        )
        return response.text
    except Exception as e:
        return f"Error generating cover letter: {str(e)}"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. DOCX RENDERER (header has NO location; adds Certifications section)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def set_font(run, size, bold=False):
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.bold = bold
    try:
        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
    except Exception:
        pass

def create_doc(data):
    doc = Document()
    s = doc.sections[0]
    s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Inches(0.5)

    # Header — NAME / ROLE TITLE / CONTACT (NO LOCATION)
    for txt, sz, b in [
        (data.get('candidate_name', CANDIDATE_NAME), 28, True),
        (data.get('candidate_title', DEFAULT_TITLE), 14, True),
        (data.get('contact_info', CONTACT_LINE), 12, True),
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(to_text_block(txt))
        if sz == 28:
            run.font.all_caps = True
        set_font(run, sz, b)

    def add_sec(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(2)
        set_font(p.add_run(title), 12, True)

    def add_body(txt, bullet=False):
        style = 'List Bullet' if bullet else 'Normal'
        p = doc.add_paragraph(style=style)
        p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        p.paragraph_format.space_after = Pt(0)
        set_font(p.add_run(to_text_block(txt)), 12)

    # Professional Summary
    add_sec("Professional Summary")
    add_body(data.get('summary', ''))

    # Technical Skills
    add_sec("Technical Skills")
    for k, v in data.get('skills', {}).items():
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        p.paragraph_format.space_after = Pt(0)
        set_font(p.add_run(f"{k}: "), 12, True)
        set_font(p.add_run(to_text_block(v)), 12)

    # Professional Experience
    add_sec("Professional Experience")
    for role in data.get('experience', []):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(0)
        line = f"{role.get('role_title')} | {role.get('company')} | {role.get('location')} | {role.get('dates')}"
        set_font(p.add_run(to_text_block(line)), 12, True)
        resps = role.get('responsibilities', [])
        if isinstance(resps, str):
            resps = resps.split('\n')
        for r in resps:
            if str(r).strip():
                add_body(r, bullet=True)
        achs = role.get('achievements', [])
        if isinstance(achs, str):
            achs = achs.split('\n')
        if achs and any(str(a).strip() for a in achs):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            set_font(p.add_run("Achievements:"), 12, True)
            for a in achs:
                if str(a).strip():
                    add_body(a, bullet=True)

    # Education
    add_sec("Education")
    for edu in data.get('education', []):
        text = f"{edu.get('degree', '')}, {edu.get('college', '')}"
        add_body(text, bullet=True)

    # Certifications
    add_sec("Certifications")
    for cert in data.get('certifications', []):
        name = cert.get('name', '')
        year = cert.get('year', '')
        text = f"{name} ({year})" if year else name
        add_body(text, bullet=True)

    return doc

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8. COVER LETTER DOCX
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def create_cover_letter_doc(cover_letter_text, data):
    doc = Document()
    s = doc.sections[0]
    s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Inches(0.5)

    def add_line(text, bold=False, space_after=12, align=WD_PARAGRAPH_ALIGNMENT.LEFT):
        if not text:
            return
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(str(text))
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.bold = bold

    add_line(data.get('candidate_name', CANDIDATE_NAME).upper(), bold=True, space_after=0)
    contact_info = data.get('contact_info', CONTACT_LINE)
    if "|" in contact_info:
        for part in contact_info.split('|'):
            add_line(part.strip(), bold=False, space_after=0)
    else:
        add_line(contact_info, bold=False, space_after=0)
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    today_str = datetime.date.today().strftime("%B %d, %Y")
    add_line(today_str, space_after=12)
    for para in cover_letter_text.split('\n'):
        if para.strip():
            add_line(para.strip(), bold=False, space_after=12, align=WD_PARAGRAPH_ALIGNMENT.JUSTIFY)
    return doc

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 9. PDF RENDERER (header NO location; adds Certifications section)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def create_pdf(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        leftMargin=0.5 * inch, rightMargin=0.5 * inch,
        topMargin=0.5 * inch, bottomMargin=0.5 * inch,
    )
    styles = getSampleStyleSheet()
    sn = ParagraphStyle('N', parent=styles['Normal'], fontName='Times-Roman', fontSize=12, leading=14, alignment=TA_JUSTIFY, spaceAfter=0)
    sh_name = ParagraphStyle('HName', parent=styles['Normal'], fontName='Times-Bold', fontSize=28, leading=30, alignment=TA_CENTER, spaceAfter=0)
    sh_title = ParagraphStyle('HTitle', parent=styles['Normal'], fontName='Times-Bold', fontSize=14, leading=16, alignment=TA_CENTER, spaceAfter=0)
    sh_contact = ParagraphStyle('HContact', parent=styles['Normal'], fontName='Times-Bold', fontSize=12, leading=14, alignment=TA_CENTER, spaceAfter=6)
    s_sec = ParagraphStyle('Sec', parent=styles['Normal'], fontName='Times-Bold', fontSize=12, leading=14, alignment=TA_LEFT, spaceBefore=12, spaceAfter=2)

    def clean(txt):
        if txt is None:
            return ""
        txt = to_text_block(txt)
        return escape(txt).replace('\n', '<br/>')

    elements = []
    elements.append(Paragraph(clean(data.get('candidate_name', CANDIDATE_NAME)).upper(), sh_name))
    elements.append(Paragraph(clean(data.get('candidate_title', DEFAULT_TITLE)), sh_title))
    elements.append(Paragraph(clean(data.get('contact_info', CONTACT_LINE)), sh_contact))

    elements.append(Paragraph("Professional Summary", s_sec))
    elements.append(Paragraph(clean(data.get('summary', '')), sn))

    elements.append(Paragraph("Technical Skills", s_sec))
    skill_items = []
    for k, v in data.get('skills', {}).items():
        text = f"<b>{clean(k)}:</b> {clean(v)}"
        skill_items.append(ListItem(Paragraph(text, sn), leftIndent=0))
    if skill_items:
        elements.append(ListFlowable(skill_items, bulletType='bullet', start='\u2022', leftIndent=15))

    elements.append(Paragraph("Professional Experience", s_sec))
    for role in data.get('experience', []):
        line = f"{role.get('role_title')} | {role.get('company')} | {role.get('location')} | {role.get('dates')}"
        elements.append(Paragraph(f"<b>{clean(line)}</b>", sn))
        elements.append(Spacer(1, 2))
        role_bullets = []
        resps = role.get('responsibilities', [])
        if isinstance(resps, str):
            resps = resps.split('\n')
        for r in resps:
            if str(r).strip():
                role_bullets.append(ListItem(Paragraph(clean(r), sn), leftIndent=0))
        if role_bullets:
            elements.append(ListFlowable(role_bullets, bulletType='bullet', start='\u2022', leftIndent=15))
        achs = role.get('achievements', [])
        if isinstance(achs, str):
            achs = achs.split('\n')
        if achs and any(str(a).strip() for a in achs):
            elements.append(Paragraph("<b>Achievements:</b>", sn))
            ach_bullets = []
            for a in achs:
                if str(a).strip():
                    ach_bullets.append(ListItem(Paragraph(clean(a), sn), leftIndent=0))
            if ach_bullets:
                elements.append(ListFlowable(ach_bullets, bulletType='bullet', start='\u2022', leftIndent=25))
        elements.append(Spacer(1, 6))

    elements.append(Paragraph("Education", s_sec))
    edu_bullets = []
    for edu in data.get('education', []):
        text = f"{edu.get('degree', '')}, {edu.get('college', '')}"
        edu_bullets.append(ListItem(Paragraph(clean(text), sn), leftIndent=0))
    if edu_bullets:
        elements.append(ListFlowable(edu_bullets, bulletType='bullet', start='\u2022', leftIndent=15))

    elements.append(Paragraph("Certifications", s_sec))
    cert_bullets = []
    for cert in data.get('certifications', []):
        name = cert.get('name', '')
        year = cert.get('year', '')
        text = f"{name} ({year})" if year else name
        cert_bullets.append(ListItem(Paragraph(clean(text), sn), leftIndent=0))
    if cert_bullets:
        elements.append(ListFlowable(cert_bullets, bulletType='bullet', start='\u2022', leftIndent=15))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 10. STREAMLIT UI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(page_title=PAGE_TITLE, layout="wide", page_icon="\U0001f680", initial_sidebar_state="expanded")
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 1.5rem;}
    div.stButton > button:first-child {border-radius: 6px; font-weight: 600;}
    div[data-testid="stMetricValue"] {font-size: 1.8rem;}
</style>
""", unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.session_state['data'] = None
if 'saved_base' not in st.session_state:
    st.session_state['saved_base'] = LAKSHMI_BASE_RESUME
if 'saved_jd' not in st.session_state:
    st.session_state['saved_jd'] = ""
if 'cover_letter' not in st.session_state:
    st.session_state['cover_letter'] = None

with st.sidebar:
    st.header("\u2699\ufe0f Configuration")
    if google_key:
        st.success("API key configured")
    else:
        st.error("API key missing — add GOOGLE_API_KEY to Streamlit secrets")
        google_key = st.text_input("Google API Key (fallback)", type="password")
    st.divider()
    st.markdown("**Target Roles:**")
    st.caption("Senior DE \u2022 Cloud DE \u2022 ETL/ELT Engineer \u2022 Big Data Engineer \u2022 Database Engineer")
    st.divider()
    st.markdown("**Models:**")
    st.caption(f"Resume: {GENERATION_MODEL}")
    st.caption(f"Scoring: {SCORING_MODEL}")
    st.divider()
    if st.button("\U0001f5d1\ufe0f Reset", use_container_width=True):
        st.session_state['data'] = None
        st.session_state['saved_base'] = LAKSHMI_BASE_RESUME
        st.session_state['saved_jd'] = ""
        st.session_state['cover_letter'] = None
        st.rerun()
    st.caption("Astra v1.1 | Personalised for Lakshmi K")

if not st.session_state['data']:
    st.markdown(f"<h1 style='text-align: center;'>{PAGE_TITLE}</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Paste a JD. Get a top-5% tailored resume. Get the call.</p>", unsafe_allow_html=True)
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("\U0001f4cb Source Resume")
        st.caption("Pre-loaded. Edit only if needed.")
        base = st.text_area("Resume", st.session_state['saved_base'], height=400, label_visibility="collapsed")
    with c2:
        st.subheader("\U0001f4bc Job Description")
        st.caption("Paste the full JD here.")
        jd = st.text_area("JD", st.session_state['saved_jd'], height=400, label_visibility="collapsed")
    if st.button("\u2728 Generate Tailored Resume", type="primary", use_container_width=True):
        if base and jd and google_key:
            st.session_state['saved_base'] = base
            st.session_state['saved_jd'] = jd
            with st.spinner("Routing title-match, mapping domain, compressing skills, optimising for ATS..."):
                data = analyze_and_generate(google_key, base, jd)
                if "error" in data:
                    st.error(data['error'])
                else:
                    st.session_state['data'] = data
                    st.rerun()
        else:
            st.warning("Please provide API Key and paste a Job Description.")
else:
    data = st.session_state['data']
    # Top bar
    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        st.markdown(f"## \U0001f3af Target: {data.get('target_company', 'Company')}")
    with c3:
        score = data.get('ats_score', 0)
        st.metric("ATS Match", f"{score}%")

    # Diagnostic chips
    chip_cols = st.columns(3)
    chip_cols[0].markdown(f"**Title Match:** `{data.get('title_match_status', 'unknown')}`")
    chip_cols[1].markdown(f"**Domain Coverage:** `{data.get('domain_coverage', 'unknown')}`")
    chip_cols[2].markdown(f"**ATS Reasoning:** {data.get('ats_reason', '')}")

    missing = data.get('missing_keywords', '')
    if missing and str(missing).strip():
        st.warning(f"**Keywords still missing from resume:** {missing}")

    tab_edit, tab_export, tab_cover = st.tabs(["\U0001f4dd Editor", "\U0001f680 Export", "\u270d\ufe0f Cover Letter"])

    with tab_edit:
        with st.form("edit_form"):
            st.subheader("Candidate Details")
            c1, c2, c3 = st.columns(3)
            data['candidate_name'] = c1.text_input("Name", to_text_block(data.get('candidate_name')))
            data['candidate_title'] = c2.text_input("Title", to_text_block(data.get('candidate_title')))
            data['contact_info'] = c3.text_input("Contact", to_text_block(data.get('contact_info')))
            data['summary'] = st.text_area("Summary", to_text_block(data.get('summary')), height=140)

            st.subheader("Skills")
            skills = data.get('skills', {})
            new_skills = {}
            s_cols = st.columns(2)
            for i, (k, v) in enumerate(skills.items()):
                col = s_cols[i % 2]
                new_val = col.text_area(k, to_text_block(v), key=f"skill_{i}", height=80)
                new_skills[k] = new_val.replace('\n', ', ')
            data['skills'] = new_skills

            st.subheader("Experience")
            for i, role in enumerate(data.get('experience', [])):
                with st.expander(f"{role.get('role_title', 'Role')} @ {role.get('company', 'Company')}"):
                    c1, c2 = st.columns(2)
                    role['role_title'] = c1.text_input("Title", to_text_block(role.get('role_title')), key=f"jt_{i}")
                    role['company'] = c2.text_input("Company", to_text_block(role.get('company')), key=f"jc_{i}")
                    c3, c4 = st.columns(2)
                    role['dates'] = c3.text_input("Dates", to_text_block(role.get('dates')), key=f"jd_{i}")
                    role['location'] = c4.text_input("Location", to_text_block(role.get('location')), key=f"jl_{i}")
                    role['responsibilities'] = st.text_area("Responsibilities", to_text_block(role.get('responsibilities')), height=220, key=f"jr_{i}")
                    role['achievements'] = st.text_area("Achievements", to_text_block(role.get('achievements')), height=110, key=f"ja_{i}")

            st.subheader("Education")
            for i, edu in enumerate(data.get('education', [])):
                c1, c2 = st.columns(2)
                edu['degree'] = c1.text_input("Degree", to_text_block(edu.get('degree')), key=f"ed_{i}")
                edu['college'] = c2.text_input("Institution", to_text_block(edu.get('college')), key=f"ec_{i}")

            st.subheader("Certifications")
            for i, cert in enumerate(data.get('certifications', [])):
                c1, c2 = st.columns([3, 1])
                cert['name'] = c1.text_input("Certification", to_text_block(cert.get('name')), key=f"cn_{i}")
                cert['year'] = c2.text_input("Year", to_text_block(cert.get('year')), key=f"cy_{i}")

            if st.form_submit_button("\U0001f4be Save Edits", type="primary"):
                st.session_state['data'] = data
                st.success("Saved!")
                st.rerun()

    with tab_export:
        st.subheader("\U0001f4e5 Download")
        c_name = data.get('candidate_name', 'Lakshmi_K')
        default_company = data.get('target_company', 'Company')
        target_company = st.text_input("Company (for filename)", default_company)
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', c_name.strip().replace(' ', '_'))
        safe_company = re.sub(r'[^a-zA-Z0-9_-]', '_', target_company.strip())
        final_filename = f"{safe_name}_{safe_company}"
        c1, c2 = st.columns(2)
        doc_obj = create_doc(data)
        bio = io.BytesIO()
        doc_obj.save(bio)
        c1.download_button(
            label="\U0001f4c4 Word (.docx)",
            data=bio.getvalue(),
            file_name=f"{final_filename}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            type="primary",
            use_container_width=True,
        )
        try:
            pdf_data = create_pdf(data)
            c2.download_button(
                label="\U0001f4d5 PDF",
                data=pdf_data,
                file_name=f"{final_filename}.pdf",
                mime="application/pdf",
                type="secondary",
                use_container_width=True,
            )
        except Exception as e:
            c2.error(f"PDF Error: {e}")

    with tab_cover:
        st.subheader("\u270d\ufe0f Cover Letter")
        st.info("Generates a human-sounding US-format cover letter using the war story closest to the JD's industry and stack.")
        if st.button("\u2728 Draft Cover Letter", type="primary"):
            if google_key and st.session_state['saved_jd']:
                with st.spinner("Picking war story, drafting narrative..."):
                    cl_text = generate_cover_letter(google_key, data, st.session_state['saved_jd'])
                    st.session_state['cover_letter'] = cl_text
            else:
                st.warning("Need API key and JD.")
        if st.session_state['cover_letter']:
            edited_cl = st.text_area("Preview (editable)", st.session_state['cover_letter'], height=400)
            st.session_state['cover_letter'] = edited_cl
            cl_doc = create_cover_letter_doc(st.session_state['cover_letter'], data)
            bio_cl = io.BytesIO()
            cl_doc.save(bio_cl)
            st.download_button(
                label="\U0001f4c4 Download Cover Letter (.docx)",
                data=bio_cl.getvalue(),
                file_name=f"Cover_Letter_{final_filename}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                type="primary",
            )

    st.divider()
    c3, c4 = st.columns(2)
    if c3.button("\u267b\ufe0f Re-Optimise", use_container_width=True):
        if st.session_state['saved_base'] and st.session_state['saved_jd']:
            with st.spinner("Re-tailoring..."):
                data = analyze_and_generate(google_key, st.session_state['saved_base'], st.session_state['saved_jd'])
                if "error" in data:
                    st.error(data['error'])
                else:
                    st.session_state['data'] = data
                    st.rerun()
    if c4.button("New Application (Keep Resume)", use_container_width=True):
        st.session_state['data'] = None
        st.session_state['saved_jd'] = ""
        st.session_state['cover_letter'] = None
        st.rerun()
