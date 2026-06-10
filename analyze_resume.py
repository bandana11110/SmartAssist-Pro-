def analyze_resume(text):

    score = 0

    feedback = []

    keywords = [
        "python",
        "sql",
        "machine learning",
        "data science",
        "project",
        "github",
        "internship",
        "streamlit"
    ]

    found = []

    lower_text = text.lower()

    for keyword in keywords:

        if keyword in lower_text:

            score += 10
            found.append(keyword)

    if score > 100:
        score = 100

    feedback.append(f"📊 Resume Score: {score}/100")

    feedback.append("")

    feedback.append("✅ Skills Detected:")

    if found:

        for item in found:
            feedback.append(f"• {item}")

    else:
        feedback.append(
            "No important technical keywords found."
        )

    feedback.append("")

    feedback.append("🚀 Suggestions:")

    if "github" not in lower_text:
        feedback.append(
            "• Add GitHub profile link"
        )

    if "project" not in lower_text:
        feedback.append(
            "• Mention academic/personal projects"
        )

    if "internship" not in lower_text:
        feedback.append(
            "• Include internships or practical experience"
        )

    if "streamlit" not in lower_text:
        feedback.append(
            "• Mention deployed projects"
        )

    return "\n".join(feedback)