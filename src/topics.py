"""
Topic configurations and post type templates for LinkedIn content generation.
"""

POST_TYPES = {
    "expert_challenge": {
        "name": "Expert Challenge",
        "description": "A tricky technical question to test expert knowledge",
        "prompt_instruction": (
            "Create a challenging technical quiz question that will make experts think. "
            "Include a code snippet or scenario, ask what happens/what is the output/what is wrong, "
            "and end with '💬 Drop your answer below!' and relevant hashtags. "
            "Format it as an engaging LinkedIn post (no more than 300 words)."
        ),
    },
    "open_discussion": {
        "name": "Open Discussion",
        "description": "Thought-provoking question to spark community discussion",
        "prompt_instruction": (
            "Write a thought-provoking open discussion post that invites professionals to share their opinions. "
            "Start with a bold statement or controversial take, explain your perspective briefly, "
            "then ask an open-ended question. End with '👇 What's your take?' and relevant hashtags. "
            "Format it as an engaging LinkedIn post (no more than 250 words)."
        ),
    },
    "tip_of_day": {
        "name": "Tip of the Day",
        "description": "A practical, actionable tip with code or example",
        "prompt_instruction": (
            "Share a practical tip that most practitioners don't know or overlook. "
            "Include a concrete code example or before/after comparison. "
            "Structure it as: Hook (1 line) → Problem → Solution (with example) → Key takeaway. "
            "End with relevant hashtags. Format it as an engaging LinkedIn post (no more than 300 words)."
        ),
    },
    "myth_vs_reality": {
        "name": "Myth vs Reality",
        "description": "Bust a common misconception in the field",
        "prompt_instruction": (
            "Debunk a common myth or misconception. "
            "Start with '🚫 Myth:' then the misconception, followed by '✅ Reality:' and the truth. "
            "Explain WHY the myth exists and what the correct approach is with a practical example. "
            "End with relevant hashtags. Format it as an engaging LinkedIn post (no more than 300 words)."
        ),
    },
    "series_deep_dive": {
        "name": "Series Deep Dive",
        "description": "In-depth explanation of a specific concept",
        "prompt_instruction": (
            "Write an educational deep-dive post explaining a specific concept clearly. "
            "Use emojis as bullet points, include a real-world analogy, and provide a practical example. "
            "Structure: Concept intro → Why it matters → How it works → Real example → Key takeaway. "
            "End with relevant hashtags. Format it as an engaging LinkedIn post (no more than 400 words)."
        ),
    },
}

TOPICS = {
    "gen_ai": {
        "name": "Generative AI",
        "hashtags": "#GenAI #LLM #AI #MachineLearning #ArtificialIntelligence",
        "subtopics": [
            "RAG (Retrieval-Augmented Generation) architecture patterns",
            "LLM prompt engineering techniques",
            "Vector databases and embeddings",
            "Fine-tuning vs RAG vs prompt engineering trade-offs",
            "LLM evaluation and benchmarking",
            "AI agents and tool use",
            "Context window management strategies",
            "LLM hallucination mitigation",
            "Multimodal AI (vision + text)",
            "AI safety and responsible AI practices",
            "Token optimization and cost reduction",
            "LLM output structured parsing",
            "Semantic chunking for RAG",
            "Hybrid search (vector + keyword)",
            "LLM caching strategies",
        ],
    },
    "databricks": {
        "name": "Databricks",
        "hashtags": "#Databricks #ApacheSpark #DeltaLake #DataEngineering #BigData",
        "subtopics": [
            "Delta Lake ACID transactions and time travel",
            "Spark query optimization techniques",
            "Unity Catalog data governance",
            "MLflow experiment tracking",
            "Databricks AutoML",
            "Delta Live Tables (DLT) pipelines",
            "Photon engine performance",
            "Databricks SQL Analytics",
            "Cluster configuration best practices",
            "Z-Ordering and data skipping",
            "Databricks notebooks vs jobs",
            "Feature Store for ML",
            "Structured Streaming with Delta",
            "Databricks Workflows orchestration",
            "Cost optimization on Databricks",
        ],
    },
    "sql_server": {
        "name": "SQL Server",
        "hashtags": "#SQLServer #TSQL #DatabaseOptimization #DataEngineering #SQL",
        "subtopics": [
            "Query execution plan analysis",
            "Index design and optimization",
            "T-SQL window functions",
            "Common Table Expressions (CTEs) best practices",
            "Stored procedure optimization",
            "Deadlock detection and prevention",
            "Partitioning strategies for large tables",
            "Column store indexes for analytics",
            "SQL Server In-Memory OLTP",
            "Query store and performance regression detection",
            "Statistics maintenance and auto-update",
            "Temporal tables for data history",
            "JSON support in SQL Server",
            "Always On availability groups",
            "TempDB contention and optimization",
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
