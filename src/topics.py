"""
Topic configurations and post type templates for LinkedIn content generation.
"""

POST_TYPES = {
    "expert_challenge": {
        "name": "Expert Challenge",
        "description": "A tricky technical question to test expert knowledge",
        "prompt_instruction": (
            "Create a challenging technical scenario or code snippet that makes experienced professionals stop and think. "
            "Ask what happens, what is wrong, or what would you do differently. "
            "End by inviting people to drop their answer in the comments. "
            "Keep it under 300 words. No emojis."
        ),
    },
    "open_discussion": {
        "name": "Open Discussion",
        "description": "Thought-provoking question to spark community discussion",
        "prompt_instruction": (
            "Share a personal observation or experience that challenges conventional wisdom. "
            "Be honest about what you have seen in practice. Present both sides fairly. "
            "End with a genuine open-ended question that invites people to share their own experience. "
            "Keep it under 250 words. No emojis."
        ),
    },
    "tip_of_day": {
        "name": "Tip of the Day",
        "description": "A practical, actionable tip with code or example",
        "prompt_instruction": (
            "Share something you learned recently that made a real difference in your work. "
            "Include a concrete before/after example or code snippet. "
            "Structure: Hook line, then the problem you faced, then what you did, then the result. "
            "Keep it under 300 words. No emojis."
        ),
    },
    "myth_vs_reality": {
        "name": "Myth vs Reality",
        "description": "Bust a common misconception in the field",
        "prompt_instruction": (
            "Challenge a popular belief with evidence from your own experience. "
            "Start with what most people believe, then share what you have actually seen in practice. "
            "Explain why the misconception exists and what the better approach looks like. "
            "Keep it under 300 words. No emojis."
        ),
    },
    "series_deep_dive": {
        "name": "Series Deep Dive",
        "description": "In-depth explanation of a specific concept",
        "prompt_instruction": (
            "Break down a concept in a way that makes it click for someone learning it. "
            "Use a real-world analogy, walk through a practical example, and share what tripped you up when you first learned it. "
            "Structure: What it is, why it matters, how it works with a real example, and the key thing most people get wrong. "
            "Keep it under 400 words. No emojis."
        ),
    },
}

TOPICS = {
    "gen_ai": {
        "name": "Generative AI",
        "hashtags": "#GenAI #LLM #AI #MachineLearning #ArtificialIntelligence",
        "subtopics": [
            # Trending / high-engagement topics
            "Will AI replace software engineers or make them 10x more productive",
            "The real cost of running LLMs in production — what nobody talks about",
            "Why most RAG implementations fail and how to fix them",
            "AI agents that actually work — lessons from real deployments",
            "The skills gap: what hiring managers really want in AI engineers",
            "Claude vs GPT vs Gemini vs Llama — honest comparison from someone who uses all of them",
            "How I cut our LLM costs by 80% without losing quality",
            "The biggest mistakes teams make when adopting AI for the first time",
            "Why prompt engineering is becoming a real engineering discipline",
            "Building AI products vs AI demos — the gap nobody warns you about",
            "Fine-tuning is overrated — when RAG and prompting are enough",
            "AI hallucinations in production — war stories and solutions",
            "The future of coding with AI copilots — what changed in my workflow",
            "Why your vector database choice matters less than your chunking strategy",
            "Multimodal AI is here — practical use cases beyond the hype",
            "Open source vs closed source LLMs — the real trade-offs in 2026",
            "How non-technical teams are using AI and what engineers can learn from them",
            "The one AI pattern that transformed how our team ships features",
            "Why context window size is a trap — and what actually matters for quality",
            "AI governance is not optional anymore — lessons learned the hard way",
            "What I wish I knew before building my first AI-powered application",
            "The uncomfortable truth about AI benchmarks and leaderboards",
            "Small language models are quietly winning in production",
            "How to evaluate if your AI feature is actually helping users",
            "The rise of AI engineering as a career path — roadmap for 2026",
        ],
    },
    "databricks": {
        "name": "Databricks",
        "hashtags": "#Databricks #ApacheSpark #DeltaLake #DataEngineering #BigData",
        "subtopics": [
            # Trending / high-engagement topics
            "Why your Databricks bill is 3x what it should be — and how to fix it",
            "Medallion architecture — is it still the best pattern or are we over-engineering",
            "The migration from legacy ETL to Databricks — honest lessons from the trenches",
            "Delta Lake vs Iceberg vs Hudi — which lakehouse format is winning",
            "Unity Catalog changed how we think about data governance — here is how",
            "Databricks vs Snowflake — when to use which and why the debate misses the point",
            "The most underrated Databricks features that senior engineers actually use",
            "How we reduced Spark job runtime from 4 hours to 20 minutes",
            "Data pipeline testing strategies that actually catch bugs before production",
            "Real-time streaming on Databricks — when it is worth it and when batch wins",
            "The data engineer career path in 2026 — what companies are hiring for",
            "Why your Delta tables are slow and the fix is simpler than you think",
            "Databricks Workflows vs Airflow vs Prefect — picking the right orchestrator",
            "How to build a data platform that scales without drowning in technical debt",
            "The Lakehouse architecture two years in — what worked and what we would change",
            "Spark performance tuning — the 5 things that make the biggest difference",
            "How Photon engine changed our query economics overnight",
            "Data quality frameworks on Databricks — what actually works in practice",
            "The biggest data engineering interview mistakes I see as a hiring manager",
            "From notebooks to production — the gap that breaks most data teams",
            "MLflow in practice — model tracking beyond the hello world tutorial",
            "Why data mesh failed at some companies and succeeded at others",
            "Building cost-aware data pipelines that finance teams actually approve",
            "Databricks SQL vs traditional data warehouses — real benchmark results",
            "How we handle schema evolution in production without breaking downstream",
        ],
    },
    "sql_server": {
        "name": "SQL Server",
        "hashtags": "#SQLServer #TSQL #DatabaseOptimization #DataEngineering #SQL",
        "subtopics": [
            # Trending / high-engagement topics
            "The query that brought our production database to its knees — and how we fixed it",
            "Why DBAs are not going away — the evolving role in the cloud era",
            "SQL Server vs PostgreSQL — an honest take from someone who uses both daily",
            "The most expensive indexing mistakes I see in production databases",
            "Migrating SQL Server to the cloud — the hidden gotchas nobody mentions",
            "T-SQL tricks that senior developers use but rarely teach",
            "Why your database is slow — it is probably not what you think",
            "The execution plan patterns every developer should recognize",
            "How we handle 1 billion rows in SQL Server without breaking a sweat",
            "SQL Server 2025 features that change everything for data professionals",
            "The career path from DBA to data platform architect — what I learned",
            "Why most database performance tuning advice on the internet is wrong",
            "Deadlocks in production — the debugging approach that always works",
            "When to use stored procedures vs ORMs — the nuanced answer",
            "The cost of ignoring index maintenance — real numbers from production",
            "Window functions that solve problems most developers use subqueries for",
            "High availability setup that actually survives real failures",
            "Temporal tables — the feature I wish I knew about 5 years ago",
            "How to convince your team to care about database performance",
            "The SQL Server monitoring stack that saved our on-call team",
            "Partitioning done right — lessons from managing multi-TB databases",
            "Why I stopped writing complex CTEs and what I do instead",
            "JSON in SQL Server — when it makes sense and when it is a code smell",
            "Database CI/CD pipelines — how we deploy schema changes without fear",
            "The interview questions I ask SQL Server candidates and why",
        ],
    },
}

# Posting schedule: maps day index (0=Mon, 6=Sun) to topic key
WEEKLY_SCHEDULE = {
    0: "gen_ai",        # Monday
    1: "databricks",    # Tuesday
    2: "sql_server",    # Wednesday
    3: "gen_ai",        # Thursday
    4: "databricks",    # Friday
    5: "sql_server",    # Saturday
    6: "gen_ai",        # Sunday
}

# Post type rotation order
POST_TYPE_ROTATION = [
    "expert_challenge",
    "open_discussion",
    "tip_of_day",
    "myth_vs_reality",
    "series_deep_dive",
]
