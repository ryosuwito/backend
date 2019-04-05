# -*- coding: utf-8 -*-
# flake8: noqa
from main.models import OnlineApplication, Position


positions = [
    Position(
        "Fundamental Quantitative Researcher", "FQRES",
        ["The fundamental quantitative researchers develop trading ideas using fundamental and quantitative analysis. A mixed background of finance, programming and statistics is preferred for this position."],
        [
            [
                "Recent Master/PhD from a finance, accounting, economics or related field. Bachelors with exceptional performance will also be considered",
                "Key interest in financial markets",
                "Attention to detail",
                "Excellent analytical and financial skills",
            ],
            "The following skills are bonus in recruitment and are required before on board",
            [
                "Intermediate programming skills",
                "Comfortable with Linux/Unix",
            ]
        ]
    ),
    Position(
        "Quantitative Researcher", "QRES",
        ["The quantitative researchers design and backtest trading models, which form the most important elements in the final trading strategies. They work in groups or independently, depending on the projects and/or the researchers' preference. Creativity and innovation are what we are looking for in this position."],
        [
            [
                "Recent Master/PhD from a science, engineering, or related field. Bachelors with exceptional performance will also be considered",
                "Solid background in mathematics",
                "Strong programming skills",
                "Strong problem solving and quantitative skills",
                "Possess the desire and will to learn complicated topics, to solve difficult problems, and to handle tedious tasks carefully",
            ],
            "The following skills are bonus in recruitment and are required before on board:",
            [
                "Comfortable with Linux/Unix",
                "Familiar with at least one scripting language, e.g. python, awk, etc"
            ]
        ]
    ),
    Position(
        "Front Desk Quant Developer", "DEV",
        [
            "The front desk quant developers maintain our trading/research capabilities in global markets and innovate how we do them.",
            "Typical responsibilities include:",
            [
                "Optimizing the performance of various components of the trading system",
                "Maintaining, enhancing backtest simulator",
                "Exploring big-data infrastructure for research",
                "Execution algorithms research",
                "Working with researchers on high-frequency strategies"
            ]
        ],
        [
            [
                "Expert programming skills in some well-known language, along with knowledge on computer system, e.g. networking, threading, etc.",
                "Ability to write sizable applications and manage complexity",
                "Effective communicator and decision maker",
                "Linux experience",
            ],
            "The following skills are bonus:",
            [
                "Familiar with Linux kernel",
                "Experience with hardware development, e.g. NIC, GPU, and FPGA etc.",
                "System administration experience"
            ]
        ]
    ),
    Position(
        "Data Engineer", "DATAENG",
        [
            "Data Engineers coordinate with researchers to develop and manage data inventories and design framework to facilitate efficient processing of large-scale data. They monitor and maintain data production on a daily basis.",
        ],
        [
            [
                "Highly detail-oriented",
                "Strong problem-solving skills in python and good understanding of data structure/algorithms",
                "Ability to prioritize work and multi-task",
                "Ability to take responsibility and work well as a team member",
                "Comfortable with Linux",
            ],
            "The following skills are bonus:",
            [
                "Knowledge on database and big data tools like hadoop, spark",
                "Web development experience",
                "Experience with large data (>100G)",
            ]
        ]
    ),
    Position(
        "Trading Operation Specialist", "TRADEOP",
        [
            "Operation specialists are responsible for the global trading operation around the clock.They work with quant researchers and developers to support end-to-end stock trading related activities with cutting edge technologies. The candidates will have a chance to gain knowledge on the entire workflow of advanced algorithmic trading.",
            "Typical responsibilities include:",
            [
                "Monitor global trading activities and investigate various trading related issues from both front office and back office",
                "Handle miscellaneous requests from researchers and developers to support their daily work",
                "Develop and maintain automation jobs and data pipelines across trading engines",
                "Analyze post-trade data to evaluate the performance of trading strategies and algorithms in different stock markets and identify potential trading risk"
            ]
        ],
        [
            [
				"Demonstrated programming skills in Python and Bash",
				"Love to automate the daily work by programming as much as possible",
				"Strong problem-solving skills and detail-oriented when taking multiple tasks",
				"Strong responsibility and keen learner",
				"Good interpersonal skills",
            ],
			"Fresh graduates are welcome to apply."
        ]
    ),
    Position(
        "Fundamental Quantitative Researcher (Internship)", "FQRESINTERN",
        [
            [
                "Developing trading strategies using fundamental information in quantitative methodology"
            ],
        ],
        [
            [
                "Master or PhD in Mathematics, Physics, Economics, Finance, Computer Engineering, Engineering, or other related fields from top universities. Applicants with a Bachelor’s degree and exceptional performance will also be considered",
                "Possess a strong interest in financial markets",
                "Advanced quantitative, analytical and problem-solving skills",
                "Detail-oriented",
                "A strong background in mathematics",
                "Past experience in the secondary market or quantitative finance is preferred",
            ],
            "The following skills are bonus and you will be required to complete learning projects before onboarding:",
            [
                "Knowledge of Linux",
                "Solid programming skills in Python or C++"
            ],
            "Return offer will be given upon exceptional performance during internship."
        ],
        location=["Shanghai"],
        duration=[
            [
                "Full-time: at least 2 months",
                "Part-time: at least 3 days per week for a minimum of 4 months",
            ]
        ]
    ),
    Position(
        "Quantitative Researcher (Internship)", "QRESINTERN",
        [
            [
                "Focus on research topics with the guidance of senior researchers",
                "Implement trading signals and quantitative strategies",
            ],
        ],
        [
            [
                "Master or PhD in Mathematics, Physics, Economics, Finance, Computer Engineering, Engineering, or other related fields from top universities. Applicants with a Bachelor’s degree and exceptional performance will also be considered",
                "Strong mathematical and statistical skills",
                "Good programming skills",
                "Excellent problem-solving skills",
                "Detail-oriented with the ability to handle tedious tasks carefully",
                "Proactive and eager to learn complicated topics",

            ],
            "The following skills are bonus and you will be required to complete learning projects before onboarding:",
            [
                "Experience with Linux/Unix",
                "Familiar with at least one scripting language, e.g. Python, MATLAB, etc.",
            ],
            "Return offer will be given upon exceptional performance during internship."
        ],
        location=["Shanghai"],
        duration=[
            [
                "Full-time: at least 2 months",
                "Part-time: at least 3 days per week for a minimum of 4 months",
            ]
        ]
    ),
    Position(
    "Data Engineer (Internship)", "DATAENGINTERN",
        [
            "Data Engineers interns maintain our data inventories, collect and clean the data we have gathered from various sources to make sure of the integrity, completeness and usefulness of our data."],
        [
            [
                "Year 2 or Year 3 student pursuing a degree in Computer Science, Business Analytics, Engineering, Science.",
                "Detail-oriented team player with strong problem-solving skills",
                "Good knowledge in python and understanding of data structure & algorithms",
                "Comfortable with Linux",
            ],
            "The following skills are bonus:",
            [
                "Knowledge on database and big data tools like hadoop, spark",
                "Web development experience",
                "Experience with large data (>100G)",
            ],
        ],
        location=[
            "Singapore",
            "Status Open to Singaporeans and PR holders. Foreign applicants must currently be a full-time student in Singapore.",
        ],
        duration=[
            [
                "Part-time: at least 16 hours per week for 4 months",
                "Full-time: at least 2 months",
            ]
        ],
    )
]
