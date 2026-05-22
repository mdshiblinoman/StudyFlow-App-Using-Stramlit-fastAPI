from urllib.parse import quote_plus


def make_search_link(query, site=None):
    q = quote_plus(query)
    if site == "youtube":
        return f"https://www.youtube.com/results?search_query={q}"
    if site == "google":
        return f"https://www.google.com/search?q={q}"
    return f"https://www.google.com/search?q={q}"


RESOURCES = {
    # Programming languages
    "Python": {
        "youtube": ["Corey Schafer", "freeCodeCamp.org", "Tech With Tim", "Sentdex"],
        "books": ["Automate the Boring Stuff with Python", "Python Crash Course"],
        "blogs": ["Real Python", "Towards Data Science"],
    },
    "C": {
        "youtube": ["Neso Academy", "freeCodeCamp.org"],
        "books": ["The C Programming Language (Kernighan & Ritchie)"],
        "blogs": ["GeeksforGeeks"],
    },
    "C++": {
        "youtube": ["The Cherno", "CppNuts"],
        "books": ["Effective Modern C++", "C++ Primer"],
        "blogs": ["cppreference.com"],
    },
    "Java": {
        "youtube": ["Java Brains", "Derek Banas"],
        "books": ["Head First Java", "Effective Java"],
        "blogs": ["Baeldung"],
    },
    "JavaScript": {
        "youtube": ["Traversy Media", "Fun Fun Function"],
        "books": ["Eloquent JavaScript"],
        "blogs": ["MDN Web Docs", "CSS-Tricks"],
    },
    "Rust": {
        "youtube": ["Let’s Get Rusty", "Chris Biscardi"],
        "books": ["The Rust Programming Language"],
        "blogs": ["Rust by Example"]
    },

    # Algorithms & DS
    "Algorithms": {
        "youtube": ["MIT OpenCourseWare", "Abdul Bari", "William Fiset"],
        "books": ["Introduction to Algorithms (CLRS)", "Grokking Algorithms"],
        "blogs": ["TopCoder", "GeeksforGeeks"],
    },
    "Data Structures": {
        "youtube": ["mycodeschool", "William Fiset"],
        "books": ["Data Structures and Algorithms in Python", "Algorithms, 4th Edition"],
        "blogs": ["GeeksforGeeks", "LeetCode"],
    },

    # Databases
    "Database Management Systems (DBMS)": {
        "youtube": ["The Net Ninja", "freeCodeCamp.org"],
        "books": ["Database System Concepts", "Designing Data-Intensive Applications"],
        "blogs": ["Use The Index, Luke", "Database Star"],
    },

    # Operating Systems
    "Operating Systems": {
        "youtube": ["Gaurav Sen", "Neso Academy"],
        "books": ["Operating System Concepts", "Modern Operating Systems"],
        "blogs": ["GeeksforGeeks"]
    },

    # AI/ML
    "Machine Learning": {
        "youtube": ["3Blue1Brown", "Two Minute Papers", "Sentdex"],
        "books": ["Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow"],
        "blogs": ["Towards Data Science", "Distill.pub"]
    },
    "Artificial Intelligence (AI)": {
        "youtube": ["Andrew Ng (Coursera)", "Two Minute Papers"],
        "books": ["Artificial Intelligence: A Modern Approach"],
        "blogs": ["AI Alignment Forum", "Towards Data Science"]
    },

    # Software engineering
    "Software Engineering": {
        "youtube": ["TechLead", "Academind"],
        "books": ["Clean Code", "Refactoring"],
        "blogs": ["Martin Fowler"]
    },
}


def get_resources_for(subject):
    # direct match
    if subject in RESOURCES:
        return RESOURCES[subject]

    # try some normalization
    key = subject.split("(")[0].strip()
    return RESOURCES.get(key, None)
