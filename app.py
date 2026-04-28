# Astra Resume Engine — Personalised for Lakshmi K (v1.3)
# US Senior Data Engineer Edition — "Top 5-10% of Applications"
# Built on the Astra v4.0 architecture (Charan edition), customised per Lakshmi's preferences.
# v1.3 changes: Summary engine rebuilt — 5 sentences, exact JD title opener,
# banned corporate closers, NO company name in summary, Charan-style flow.
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
# SKILL EXPANSION DICTIONARY — Charan's pattern, additive
# When a trigger tool is found in the source skills, related tools get appended.
# Mechanical, deterministic, runs post-LLM-generation.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LAKSHMI_SKILL_EXPANSIONS = {
    # === Cloud Data Warehousing ===
    "Snowflake": "Snowpark, Snowpipe, Snowflake Streams, Snowflake Tasks",
    "BigQuery": "BigQuery ML, BigQuery DataFrames, Dataform",
    "Amazon Redshift": "Redshift Spectrum, Concurrency Scaling, WLM",
    "Azure Synapse": "Synapse Pipelines, Synapse Spark Pool, Dedicated SQL Pool",
    # === Big Data & Processing ===
    "Apache Spark": "Spark SQL, Spark Streaming, Spark MLlib",
    "PySpark": "Spark DataFrames, Catalyst Optimizer",
    "Databricks": "Delta Lake, Databricks Workflows, Unity Catalog, Photon",
    "Hadoop": "HDFS, YARN, MapReduce",
    "Hive": "HiveQL, Hive Metastore",
    # === Orchestration & ETL ===
    "Apache Airflow": "DAG Orchestration, Airflow Operators, XCom, Sensors",
    "Azure Data Factory": "Mapping Dataflows, Linked Services, Integration Runtime",
    "AWS Glue": "Glue Catalog, Glue Crawlers, Glue Data Quality",
    "Google Cloud Dataflow": "Apache Beam, Dataflow Templates, Flex Templates",
    "Cloud Composer": "Airflow on GCP, Composer DAGs",
    "dbt": "dbt Core, dbt Tests, Data Lineage, Jinja Macros",
    # === Streaming & Messaging ===
    "Apache Kafka": "Kafka Streams, Kafka Connect, KSQL, Schema Registry",
    "Amazon Kinesis": "Kinesis Data Streams, Kinesis Firehose, Kinesis Analytics",
    "Azure Event Hubs": "Event Hubs Capture, Event Grid",
    "Google Cloud Pub/Sub": "Pub/Sub Lite, Cloud Eventarc",
    # === Compute & Serverless ===
    "AWS Lambda": "Step Functions, EventBridge, Lambda Layers",
    "Azure Functions": "Logic Apps, Durable Functions",
    "Cloud Functions": "Cloud Run, Cloud Scheduler",
    # === Databases ===
    "SQL Server": "T-SQL, SSIS, SSAS, Stored Procedures",
    "PostgreSQL": "PL/pgSQL, pgAdmin, Logical Replication",
    "MongoDB": "MongoDB Atlas, Aggregation Pipelines",
    "Cosmos DB": "SQL API, Change Feed, Multi-Region Writes",
    "Cloud SQL": "Cloud SQL Proxy, Read Replicas",
    "DynamoDB": "DynamoDB Streams, Global Tables",
    # === Storage ===
    "S3": "S3 Lifecycle Policies, S3 Glacier, S3 Object Lock",
    "ADLS Gen2": "Hierarchical Namespace, Azure Blob",
    "Google Cloud Storage": "GCS Lifecycle Policies, Storage Classes",
    # === IaC & DevOps ===
    "Terraform": "HCL, Terraform State Management, Terragrunt, Modules",
    "Jenkins": "Jenkinsfile, Declarative Pipelines",
    "Azure DevOps": "Azure Pipelines, Azure Boards, Azure Repos",
    "GitLab CI": "GitLab Runners, GitLab Pipelines",
    "Git": "GitHub Actions, Bitbucket Pipelines",
    # === Containers ===
    "Docker": "Docker Compose, ECR, Container Registry",
    "Kubernetes": "Helm, kubectl, Kustomize",
    # === Networking & Security ===
    "VPC": "Subnets, Security Groups, Network ACLs, VPC Peering",
    "IAM": "Role-Based Access Control, Service Accounts, IAM Conditions",
    # === BI & Reporting ===
    "Power BI": "DAX, Power Query, Power BI Service, Tabular Editor",
    "Tableau": "Tableau Server, Tableau Prep, LOD Calculations",
    "Looker": "LookML, Looker Studio",
    # === Programming ===
    "Python": "Pandas, NumPy, PySpark, Polars",
    "SQL": "Window Functions, CTEs, Query Optimization",
    # === Monitoring ===
    "Prometheus": "PromQL, Alertmanager",
    "Grafana": "Grafana Dashboards, Grafana Loki",
    "Splunk": "SPL, Splunk Dashboards",
    "CloudWatch": "CloudWatch Logs, CloudWatch Metrics, X-Ray",
    # === ML / AI Exposure ===
    "TensorFlow": "Keras, PyTorch",
    "AWS SageMaker": "SageMaker Pipelines, SageMaker Endpoints",
    "Azure ML": "Azure ML Pipelines, Azure ML Designer",
    "Vertex AI": "Vertex Pipelines, Vertex Feature Store",
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ASTRA PROMPT — Title-Match Engine + Domain Mapping + Bullet Engine
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ASTRA_PROMPT = """
Role: You are Astra, an elite resume tailoring engine for Lakshmi K. Your only job: place this candidate in the top 5–10% of applications for the target role.

Candidate: Lakshmi K — Senior Data Engineer with 5+ years across 5 roles. US-based (Texas).
- Northwestern Mutual (Insurance / Financial Services / Azure DE / current): ADF, Synapse, Databricks, Event Hubs, 500GB+/day
- McKesson Corporation (Healthcare / AWS DE): Glue, Lambda, Kinesis, Redshift, S3, 400GB+/day
- Mindtree (BigBasket) (Retail/E-commerce / GCP DE): Dataflow, BigQuery, Pub/Sub, 300GB+/day
- Geeky Ants (Tech Services / Multi-tool DE): Spark, Kafka, Airflow
- Exide Energy (Energy / Big Data DE): Hadoop, Spark, 2TB+ datasets

Target seniority: Senior (5+ yrs).

=== DOMAIN HONESTY ===
Lakshmi has actually worked in: Insurance / Financial Services (Northwestern Mutual), Healthcare (McKesson), Retail/E-commerce (BigBasket), Tech Services (Geeky Ants, Mindtree), Energy (Exide).
When the JD's industry MATCHES: Claim it directly.
When the JD's industry is DIFFERENT: Frame as transferable multi-cloud DE skills.
NEVER FABRICATE employment titles. The role_title field MUST exactly match the source resume: "Azure Data Engineer", "AWS Data Engineer", "GCP Data Engineer", "Data Engineer". Only the candidate_title field reflects the JD's role language.

=== ZERO MISSING KEYWORDS (ATS HACK) — THE #1 RULE ===
Your ultimate goal is to leave ZERO missing keywords. Extract EVERY hard skill, tool, framework, and language mentioned in the JD. EVERY SINGLE ONE must appear in the generated resume.
- If it's a DE tool (e.g., Snowflake, dbt, Fivetran), feature it prominently.
- If the JD asks for tools outside her core DE stack (e.g., React, Vue, Angular, .NET, Java, C++, DVC, front-end development, niche CRMs), you MUST STILL INCLUDE THEM to pass ATS filters without claiming she is a developer in them.
- HOW TO FOLD THEM IN LOGICALLY:
  1. Skills Section: Add them to an "Ecosystem Integration & Exposure" category.
  2. Experience Bullets: Weave them in as integration points, upstream/downstream dependencies, or cross-collaboration efforts. 
     * Example for Front-End (React/Vue/Angular): "Engineered scalable data pipelines to feed curated datasets directly into React/Vue.js customer-facing dashboards."
     * Example for Backend (Java/.NET): "Collaborated with backend teams to integrate PySpark ELT workflows with legacy Java/.NET microservices."
     * Example for ML (DVC/MLflow): "Provisioned infrastructure and integrated ML versioning tools like DVC to support downstream data science models."
=== METRIC PROVENANCE — STRICT ALLOWED-LIST ===
Every percentage, ratio, GB/TB volume, or quantitative claim MUST trace to the source resume. Complete allowed-metrics list:
- Northwestern Mutual: 500GB+/day, 30% (query perf), 25% (latency), 20% (throughput), 30% (workflow efficiency), 20% (deployment time)
- McKesson: 400GB+/day, 25% (storage cost), 30% (query perf), 30% (manual intervention)
- Mindtree (BigBasket): 300GB+/day, 25% (query perf)
- Geeky Ants: 25% (pipeline efficiency)
- Exide: 2TB+ datasets

Any other number is FORBIDDEN. Examples that have caused failures and must NEVER appear: "100% data integrity", "99.9% availability", "40% IAM access reduction", "15% maintenance cost", "200+ dashboards", "24/7 monitoring", "5-second response time", invented RPO/RTO numbers, invented ticket counts, invented uptime percentages, invented customer counts.

If a bullet has no source metric to anchor it, write a QUALITATIVE outcome instead — never invent a number. Acceptable qualitative patterns:
- "Strengthened IAM posture by replacing role-wide grants with scoped service-account policies"
- "Cut on-call escalations by introducing pre-deployment validation in CI/CD"
- "Hardened cross-region replication by adopting paired-region storage and tested failover playbooks"

=== TITLE-MATCH ROUTING ===
Detect the JD's role title. Compare with Lakshmi's identity (Azure Data Engineer + senior multi-cloud DE).

If JD title MATCHES (Data Engineer, Senior Data Engineer, Cloud Data Engineer, Azure/AWS/GCP Data Engineer, ETL Engineer, Big Data Engineer, or close variant): apply the 90% Rule. Align bullets deeply with the JD. Surface every JD requirement she can credibly support.

If JD title DIFFERS (Software Engineer (Data), Database Engineer, Platform Engineer, Data Architect, Analytics Engineer, ML Engineer, DataOps, etc.): apply the 20/80 Rule. About 20% of bullets across the resume preserve her DE identity (anchor bullets: ADF orchestration, Synapse warehousing, Databricks PySpark). The other 80% translate her real work into the JD's vocabulary using her actual experience as raw material — never fabricate.

=== INDUSTRY DETECTION + DOMAIN VOCABULARY ===
Detect JD industry: financial / fintech / wealth-management / brokerage / insurance / healthcare / retail / ecommerce / energy / ad-tech / telecom / logistics / media / general.

Inject domain vocabulary into bullets where it fits without lying:
- financial / fintech / wealth-management / brokerage: regulatory reporting, trading data feeds, brokerage data, transaction streams, audit trails, real-time financial insights, SOX-aligned data lineage, PII safeguards on customer financial data
- insurance: actuarial datasets, policy data, claims pipelines, underwriting analytics
- healthcare: HIPAA-aligned, clinical data, EHR integration, claims processing, pharmacy datasets
- retail / ecommerce: customer 360, transaction data, inventory feeds, demand signals, recommendation features
- energy: IoT telemetry, sensor data, grid analytics, SCADA feeds
- ad-tech: impression data, attribution, real-time bidding, audience segmentation
- telecom: CDR processing, network telemetry, subscriber analytics
- logistics: route optimization, fleet telemetry, supply-chain visibility
- media: content metadata, viewership analytics

=== SUMMARY (5 sentences — substantive professional profile, not a brochure) ===
This is the showpiece of the resume. A recruiter's eye lands here in the first 6 seconds. It must read like a senior engineer talking, not a marketing block. NEVER mention the target company by name anywhere in the summary — name-dropping reads as desperate template-filling. The summary earns the call by demonstrating depth, not by stating the obvious.

Sentence 1 — IDENTITY ANCHOR (exact JD title + years + multi-cloud + scale fact):
Open with the EXACT JD role title + 5+ years + multi-cloud foundation + a concrete scale fact. Pattern: "[JD title] with 5+ years building production data platforms across AWS, Azure, and GCP, currently moving 500GB/day in regulated financial services."
- Good: "Cloud Data Platform Engineer with 5+ years building production data platforms across AWS, Azure, and GCP, currently moving 500GB/day in regulated financial services."
- Good: "Database Engineer with 5+ years across SQL Server, PostgreSQL, BigQuery, and Cloud SQL, currently optimizing 500GB/day workloads in regulated financial environments."
- Bad: "Highly motivated Data Engineer with 5+ years…"
- Bad: "Senior Data Engineer who has shipped production data platforms…" (avoids JD title)

Sentence 2 — TECHNICAL DEPTH (specific tools and patterns at production scale):
Name the specific technologies and patterns she actually uses at scale. Reflect the JD's stack where it overlaps with her real experience. This is where she proves she's not a generalist.
- Good: "Deep production work in PySpark, Snowflake, and Airflow at billion-row scale, with hands-on Terraform-managed infrastructure across the three clouds."
- Good: "Production fluency in Azure Synapse, Amazon Redshift, and BigQuery, with metadata-driven ELT pipelines orchestrated through ADF, Glue, and Cloud Composer."
- Bad: "Specialized in cutting-edge data engineering practices and innovative cloud solutions." (vague brochure-speak)

Sentence 3 — DOMAIN STORY (claim if lived, transfer if not, never inflate):
State the industries she has actually worked in, framed correctly per the Domain Honesty rule. Match the JD's industry directly if she has it; frame as transferable cross-industry experience if she doesn't. Never claim industry tenure she lacks.
- Good (matched financial JD): "Direct production experience in regulated financial services and healthcare data platforms, including auditability, PII safeguards, and SOX-aligned data lineage."
- Good (matched healthcare JD): "Direct healthcare-data experience at McKesson with HIPAA-aligned clinical pipelines, complemented by financial-services data work at Northwestern Mutual."
- Good (different industry, e.g., ad-tech): "Cross-industry production background spanning financial services, healthcare, and retail, with transferable expertise in high-volume streaming and dimensional warehousing."
- Bad: "Passionate about leveraging data for business outcomes." (banned phrasing)

Sentence 4 — SPECIALIZED STRENGTH (the engineering edge that makes her output reliable):
Highlight ONE concrete strength that goes beyond keyword stuffing — the thing that makes her engineering work stick. Choose the angle that best fits the JD: governance/lineage, data quality, IaC discipline, real-time/streaming maturity, Lakehouse/Delta architecture, cost optimization, dimensional modeling, or DR/resilience. Be specific.
- Good (governance JD): "Engineering discipline rooted in metadata-driven pipelines, schema-validated ingestion, and version-controlled Terraform deployments for repeatable infrastructure."
- Good (real-time JD): "Streaming maturity from Event Hubs and Kinesis to Pub/Sub, with sub-minute latency patterns and idempotent retry logic baked into every pipeline."
- Good (Lakehouse JD): "Lakehouse-native delivery on Delta Lake with Bronze-Silver-Gold layering, ACID-compliant transformations, and Databricks Workflows for orchestration."
- Bad: "Driven to deliver scalable, robust, and innovative solutions." (rule-of-three + banned vocab)

Sentence 5 — JD-STACK FIT (close on the JD's stated stack/problem, NOT the company name):
Close by reflecting the JD's own technical language — its stack, its problem, its delivery model. NEVER name the company. Use a flat positional verb (uses, applies, brings, fits, transfers) or just state the parallel directly.
- Good: "The same multi-cloud foundation and Snowflake-on-AWS expertise transfer directly to a long-term project-delivery model with onshore/offshore engagement."
- Good: "This combination of GCP-native services, IaC discipline, and CDW operations fits a self-service Google Cloud analytics ecosystem at enterprise scale."
- Good: "The healthcare and clinical-data background applies directly to building and growing a multi-year medical data registry platform."
- Bad: "Aims to support [Company] in their data transformation journey." (banned closer + company name)
- Bad: "Ready to lead [Company] client workstreams." (banned closer + company name)
- Bad: "Excited to drive technical innovation at [Company]." (banned closer + company name)

BANNED summary OPENERS (sentence 1): "Highly motivated", "Results-driven", "Passionate", "Dedicated professional", "Detail-oriented", "Seasoned", "Dynamic professional", "Innovative thinker", "Experienced professional", "Senior Data Engineer who has shipped" (avoids JD title — use the JD title directly).

BANNED summary CLOSERS (sentence 5): "Aims to / Aiming to", "Ready to", "Seeking to", "Eager to", "Looking to", "Excited to", "Driven to", "Poised to", "Hoping to", "Committed to". These create the corporate brochure feel and mark the resume as AI-template.

BANNED summary CONTENT (anywhere in summary):
- The target company's name (NEVER use it — talk about the work, not the brand)
- Phrases like "at [Company]", "for [Company]", "[Company] client", "[Company]'s [problem]"
- "transformation journey", "digital transformation", "innovation journey"
- "drive value", "drive outcomes", "drive impact", "drive results", "drive innovation"
- "make a difference", "contribute to success"
- Three-adjective stacks ("scalable, reliable, and efficient")

HARD RULES:
- Exactly 5 sentences. Not 4. Not 6. Five.
- Sentence 1 MUST contain the JD's exact role title (or closest credible variant if the JD title is unusual).
- Sentence 1 MUST contain "AWS, Azure, and GCP" (or "all three major clouds" / "across the three clouds" for variety) — multi-cloud is her core differentiator.
- Sentence 1 MUST contain a concrete scale fact (500GB/day OR billion-row OR 5+ years OR similar).
- The target company name MUST NOT appear anywhere in the summary.
- No sentence may start with a banned closer verb ("Aims to / Ready to / Seeking to / Eager to / Looking to / Excited to / Driven to / Poised to / Hoping to / Committed to").
- Each sentence does ONE job per the structure above. Do not blur sentences together.

=== SKILLS ===
Output 6–8 skill categories. List the tools she actually uses + ALL harvested JD keywords. Place JD-mentioned tools FIRST in each category.

Category content rules — each tool belongs in EXACTLY ONE category:
- Cloud Platforms: AWS, Azure, GCP (the cloud names only, not services)
- Compute & Serverless: EC2, Compute Engine, Cloud Run, Cloud Functions, AWS Lambda, Azure Functions
- Data Warehousing: BigQuery, Snowflake, Amazon Redshift, Azure Synapse Analytics
- Big Data & Processing: Apache Spark, PySpark, Hadoop, Databricks, Dataproc, EMR, Flink, Beam, Hive
- Streaming & Messaging: Apache Kafka, AWS Kinesis, Azure Event Hubs, Google Cloud Pub/Sub
- Orchestration & ETL: Apache Airflow, Cloud Composer, Azure Data Factory, AWS Glue, Google Cloud Dataflow, dbt, Cloud Scheduler, Apache Oozie, Apache NiFi, Step Functions, Logic Apps
- Database Technologies: SQL Server, MySQL, PostgreSQL, Oracle, MariaDB, Cosmos DB, MongoDB, DynamoDB, Cloud SQL, Cloud Spanner, RDS, Bigtable, HBase
- Cloud Storage: S3, ADLS Gen2, Azure Blob, Google Cloud Storage, HDFS
- IaC & DevOps: Terraform, CloudFormation, ARM Templates, Cloud Deployment Manager, Azure DevOps, Jenkins, GitLab CI, AWS CodePipeline, Google Cloud Build, Git
- Networking & Security: VPC, Subnets, Firewalls, IAM, Cloud Armor, Security Groups, KMS
- Containers & Orchestration: Docker, Kubernetes, OpenShift, GKE, AKS, EKS
- Monitoring & Observability: Prometheus, Grafana, ELK Stack, Splunk, CloudWatch, Stackdriver, Azure Monitor
- Programming: Python, SQL, PySpark, Linux Shell Scripting, Java (only if JD asks AND source has it)
- BI & Reporting: Power BI, Tableau, Looker, QuickSight, Google Data Studio, Qlik
- ML/AI Exposure: TensorFlow, PyTorch, Azure ML, AWS SageMaker, GCP Vertex AI (include only if JD asks)
- Ecosystem Integration & Exposure (CRITICAL): Place any JD keywords here that are NOT core DE tools (e.g., React, Vue, Angular, .NET, C++, Java backend, DVC, front-end development) so she gets ATS credit.

=== EXPERIENCE BULLETS — THE 4 RULES ===
ALL 5 roles MUST appear in reverse chronological order. Per role: 5–8 responsibilities + 2–3 achievements.
RULE A — WHY IT MATTERS: [strong verb] + [what was built/solved] + [scale or scope] + [outcome: improved X by Y%, OR enabled business outcome].
RULE B — ANTI-REPETITION: track verbs across all 5 roles. Rotate verbs.
RULE C — KEYWORD WEAVING (CRITICAL): You must integrate the non-core JD keywords (React, Vue, DVC, etc.) logically as integration points, frontend-feeds, or cross-functional collaborations in at least 1-2 bullets across the resume.
RULE D — QUANTIFY OR SKIP: every bullet ends in a number from the allowed metrics list, or a strong qualitative outcome.

ACHIEVEMENTS use BEFORE-TO-AFTER format whenever the source data supports it:
- Preferred: "Cut Synapse query latency from ~12s to ~7s on 500GB datasets."
- Acceptable when no baseline exists: "Achieved 30% throughput gain on Azure SQL workloads."
- FORBIDDEN: inventing a baseline.

=== CONDITIONAL BULLET TRIGGERS ===
DR / failover / RTO / RPO / resilience / BCP — use ONLY if JD asks AND with no invented numbers:
- "Participated in disaster-recovery validation for Synapse warehouses across paired Azure regions"
- "Tested cross-region failover playbooks for Cloud SQL and BigQuery with the platform reliability team"

Tenant / on-call / incident / ServiceNow / Jira — use ONLY if JD asks AND with no invented metrics:
- "Resolved platform tickets from data engineering and BI tenants, troubleshooting query performance and access issues"
- "Provided production support for Glue and Redshift workloads, partnering with cross-functional teams to minimize disruption"

Terraform / IaC / Cloud Deployment Manager / CloudFormation — when JD asks for IaC, Terraform MUST appear in at least ONE bullet (not just skills). Anchors:
- BigBasket (best for GCP-heavy JDs): "Provisioned BigQuery datasets, Pub/Sub topics, and Cloud SQL instances using Terraform with GCS-backed state"
- Northwestern Mutual: "Provisioned Azure Synapse, ADLS Gen2, and Cosmos DB resources via Terraform modules with version-controlled state"
- McKesson: "Managed S3, Glue, and Redshift resource provisioning via Terraform-backed CI/CD pipelines"
Use ONE primary, optionally a SECOND — never all three (reads as inflated).

=== ANTI-AI-WRITING RULES (sounds human, not robot) ===
BANNED words and phrases anywhere in the resume:
- "leveraging", "harnessing", "utilizing" → use "using" or "with"
- "seamless", "robust" (overused), "innovative", "groundbreaking", "cutting-edge", "state-of-the-art", "best-in-class"
- "testament to", "underscores", "pivotal", "realm", "tapestry", "landscape", "at the intersection of", "at the forefront of"
- "showcasing", "highlighting", "demonstrating", "underscoring", "fostering", "cultivating", "spearheading" (unless in source)
- "passionate about", "driven by", "committed to excellence"
- "serves as", "stands as", "functions as" → use "is"
- "ensuring alignment", "ensuring seamless"
- "worked on" → use a real verb
- "various", "multiple", "numerous" → specify the number or drop the word
- "end-to-end" → allowed once per resume MAX

WRITING STYLE: Vary sentence length. No em dashes inside bullets. No three-adjective chains ("scalable, reliable, and efficient" → pick ONE). Past tense for prior roles, present tense ONLY for current Northwestern Mutual role. Active voice, no first-person pronouns.

=== STRUCTURE ===
Sections in order: Header (NAME, role title, contact line — NO LOCATION) → Professional Summary → Technical Skills (6–8 categories) → Professional Experience (ALL 5 roles, current first) → Education (Lamar University — Master in MIS) → Certifications (4 certs; JD-relevant cert sorts to top).

Contact line (LOCKED): +1 (469) 723-2320 | lakshmik3272@gmail.com | linkedin.com/in/lakshmi-k-19aa79330
Candidate name (LOCKED): Lakshmi K
Default candidate_title: "Senior Data Engineer". Use the exact JD title if it's reasonable (e.g., "Cloud Data Engineer", "Database Engineer", "Senior Cloud Platform Engineer").
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
    summary: str = Field(description="EXACTLY 3 sentences. S1: JD title + 5+ years + multi-cloud anchor. S2: technical depth + domain bridge. S3: target company named, JD-stack/problem hook folded naturally — NEVER opens with 'Aims to/Ready to/Seeking to/Eager to'.")
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
# 5. SKILLS EXPANSION (Charan's pattern — additive, trigger-based)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def expand_skills_dense_lakshmi(skills):
    """For each skill category, walk the trigger dictionary. When a trigger
    tool is present, append its related tools to that category. Mechanical,
    deterministic, runs after the LLM produces the base skills."""
    if not skills:
        return {}
    expanded = {}
    for cat, tools_str in skills.items():
        if not tools_str or not str(tools_str).strip():
            continue
        tools_str = str(tools_str)
        for trigger, additions in LAKSHMI_SKILL_EXPANSIONS.items():
            if trigger.lower() in tools_str.lower():
                for addition in additions.split(", "):
                    if addition.lower() not in tools_str.lower():
                        tools_str += f", {addition}"
        # Dedupe while preserving order (in case the LLM listed duplicates)
        tools_list = [t.strip().rstrip('.') for t in tools_str.split(",") if t.strip()]
        seen = set()
        deduped = []
        for t in tools_list:
            t_norm = t.lower()
            if t_norm not in seen:
                seen.add(t_norm)
                deduped.append(t)
        expanded[cat] = ", ".join(deduped)
    return expanded

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
        # Apply skills expansion (Charan's pattern: additive, trigger-based)
        data['skills'] = expand_skills_dense_lakshmi(data.get('skills', {}))
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
    st.caption("Astra v1.3 | Personalised for Lakshmi K")

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
            with st.spinner("Routing title-match, mapping domain, expanding skills, optimising for ATS..."):
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
