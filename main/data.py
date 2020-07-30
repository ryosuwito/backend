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
        ],
        plus=[
            "The following skills are bonus in recruitment and are required before on board",
            [
                "Intermediate programming skills",
                "Comfortable with Linux/Unix",
            ]
        ],
        location=("Singapore",),
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
        ],
        plus=[
            "The following skills are bonus in recruitment and are required before on board:",
            [
                "Comfortable with Linux/Unix",
                "Familiar with at least one scripting language, e.g. python, awk, etc"
            ]
        ],
        location=("Singapore",),
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
        ],
        plus=[
            "The following skills are bonus:",
            [
                "Familiar with Linux kernel",
                "Experience with hardware development, e.g. NIC, GPU, and FPGA etc.",
                "System administration experience"
            ]
        ],
        location=("Singapore",),
    ),
    Position(
        "Full-Stack Web Developer", "",
        [
            "Primary responsibilities include:",
            [
                "builds and maintains web applications on the linux platform.",
                "Client-server architecture design",
                "Creation and maintenance of scalable, customizable and robust web applications",
                "Technical documentation",
                "Database administration",
            ]
        ],
        [
            [
                'Familiarity with common stacks.',
                'Knowledge of multiple front-end languages and libraries (e.g. HTML/ CSS, JavaScript, XML, jQuery, Bootstrap, React)',
                'Experience with modern server-side frameworks such as Django, Laravel, Express.js, Flask, Rails.',
                'Familiarity with databases (e.g. MySQL, MongoDB, Postgresql), web servers (e.g. Apache, Nginx) and UI/UX design.',
                'Great attention to detail.',
                'Excellent communication and teamwork skills.',
                'Fast adapting to new technologies.',
            ]
        ],
        location=("Singapore",),
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
        ],
        plus=[
            "The following skills are bonus:",
            [
                "Knowledge on database and big data tools like hadoop, spark",
                "Web development experience",
                "Experience with large data (>100G)",
            ]
        ],
        location=("Singapore",),
    ),
    Position(
        "Trading Operation Specialist", "TRADEOP",
        [
            "The trading operations team is primarily responsible for managing DTL’s trading environment and ensuring that everything runs smoothly. We help DTL build and maintain best-in-class systems and processes.",
            "This involves configuring, monitoring and optimising the firm’s trading with a focus on risk management and control. The team oversees core operational processes and participates in projects and initiatives that will help streamline critical workflows.",
            " Project areas include: market access, trade monitoring, process optimization, system enhancement, alpha management and automation. This is a mission-critical role that requires a dependable individual with a can-do attitude and exceptional attention to detail.",
            "Key responsibilities:",
            [
                "Monitor global trading activities and analyse and troubleshoot issues that may arise in the normal course of business in a timely and accurate manner",
                "Work collaboratively with researchers and developers and be their first line of support for any queries",
                "Identify opportunities to automate and streamline legacy processes to enhance productivity and controls",
                "Analyse post-trade data to evaluate the performance of trading strategies and algorithms in different stock markets and identify potential trading risks",
            ]
        ],
        [
            [
                 "Proficient in Python and Bash scripting",
                 "Comfortable with Linux",
                 "Strong business judgment and ability to identify and escalate issues",
                 "Patient, extremely detail-oriented and highly responsible",
                 "Excellent problem-solving skills",
                 "Good communication and interpersonal skills"
            ],
        ],
        plus=[
            "The following skills are bonus:",
            [
                "Understanding of market data/order entry systems",
                "Interest in the financial markets"
            ]
        ],
        location=("Singapore",),
    ),
    Position(
        "System Administrator", "SYSAD",
        [
            "System administrators ensure reliable operation of computer systems and servers. They also actively resolve problems and issues with operating systems and hardwares. They continuously improve hardware infrastructure to keep up with business need.",
            "Typical responsibilities:",
            [
                "Assemble PC, install Linux systems, primarily Ubuntu and CentOS.",
                "Support users' hardware and software issues.",
                "Monitor workstations and servers.",
                "Install and configure networking equipments.",
                "Set up and manage server rooms and data centers.",
            ],

        ],
        [
            [
                "Proficient in Ubuntu and CentOS, Windows administration.",
                "Knowledge of Linux bash script.",
                "Understanding of networking.",
                "Strong problem-solving skill.",
                "Experience in hardware troubleshooting.",
            ],
        ],
        plus=[
            "Knowledge in this area will be a plus:",
            [
                "LDAP, DNS",
                "nagios, ansible, puppet, docker",
            ],
        ],
        location=("Singapore",),
    ),
    Position(
        "FPGA Engineer", "",
        [
            "The FPGA Engineers maintain our trading/ research capabilities in global markets and innovate how we do them.",
            "Typical responsibilities include:",
            [
                "Build/ maintain FPGA designs for trading system",
                "Optimizing the performance of various components of the trading system",
                "Maintaining, enhancing backtest simulator",
                "Research and propose innovative solutions to improve FPGA development ",
            ],
        ],
        [
            [
                "Expert hardware programming skills.",
                "Strong RTL skills, e.g. Verilog, SystemVerilog.",
                "Experience in full process of FPGA hardware development, e.g. design, test, validate.",
                "Strong understanding of hardware and software interaction.",
                "Ability to solve problems and manage complexity.",
            ],
        ],
        plus=[
            "The following skills are bonus:",
            [
                "C++ experience.",
                "Linux experience.",
                "Familiar with at least one scripting language, e.g. phyton etc.",
                "System administration experience.",
            ],
        ],
        location=('Singapore',),
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
            "Return offer will be given upon exceptional performance during internship."
        ],
        plus=[
            "The following skills are bonus and you will be required to complete learning projects before onboarding:",
            [
                "Knowledge of Linux",
                "Solid programming skills in Python or C++"
            ],
        ],
        # location=["Shanghai, Singapore, remote"],
        duration=[
            [
                "Full-time: at least 3 months",
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
            "Return offer will be given upon exceptional performance during internship."
        ],
        plus=[
            "The following skills are bonus and you will be required to complete learning projects before onboarding:",
            [
                "Experience with Linux/Unix",
                "Familiar with at least one scripting language, e.g. Python, MATLAB, etc.",
            ],
        ],
        # location=["Shanghai, Singapore, remote"],
        duration=[
            [
                "Full-time: at least 3 months",
                "Part-time: at least 3 days per week for a minimum of 4 months",
            ]
        ]
    ),
    Position(
        "Front Desk Quant Developer (Internship)", "DEV_INTERN",
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
                "Pursuing a Bachelor degree in computer science",
                "Expert programming skills in some well-known language, along with knowledge on computer system, e.g. networking, threading, etc.",
                "Ability to write sizable applications and manage complexity",
                "Effective communicator and decision maker",
                "Linux experience",
            ],
        ],
        plus=[
            "The following skills are bonus:",
            [
                "Familiar with Linux kernel",
                "Experience with hardware development, e.g. NIC, GPU, and FPGA etc.",
                "System administration experience"
            ]
        ],
        # location=["Singapore, Shanghai, remote"],
        duration=[
            [
                "Full-time: at least 3 months",
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
        ],
        plus=[
            "The following skills are bonus:",
            [
                "Knowledge on database and big data tools like hadoop, spark",
                "Web development experience",
                "Experience with large data (>100G)",
            ],
        ],
        # location=[
            # "Singapore, Shanghai, remote",
#            "Status Open to Singaporeans and PR holders. Foreign applicants must currently be a full-time student in Singapore.",
        # ],
        duration=[
            [
                "Part-time: at least 16 hours per week for 4 months",
                "Full-time: at least 2 months",
            ]
        ],
    ),
    Position(
        "Data Analyst (Internship)", "",
        [
            "Data Analyst interns maintain our data inventories, collect and clean the data we have gathered from various sources to make sure of the integrity, completeness and usefulness of our data."
        ],
        [
            [
                "Student pursuing a degree in Computer Science, Business Analytics, Finance, Engineering, Science.",
                "Detail-oriented team player with strong problem-solving skills.",
                "Basic knowledge in Finance.",
            ],
        ],
        plus=[
            "The following will be a plus:",
            [
                "Good knowledge in python.",
                "Understanding of algorithms & data structure.",
                "Comfortable with Linux.",
            ],
        ],
        # location=["Singapore, Shanghai, remote"],
        duration=[
            [
                "Part-time: at least 16 hours per week for 4 months",
                "Full-time: at least 2 months",
            ]
        ],

    )
]
