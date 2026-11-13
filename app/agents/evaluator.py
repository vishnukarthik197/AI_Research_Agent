
def evaluate_report(report, sources):

    required_sections = [
        "Executive Summary",
        "Introduction",
        "Key Findings",
        "Detailed Explanation",
        "Source Analysis",
        "Limitations",
        "Conclusion"
    ]

    missing_sections = []

    for section in required_sections:
        if section.lower() not in report.lower():
            missing_sections.append(section)

    word_count = len(report.split())

    # Calculate report structure score
    total_sections = len(required_sections)
    completed_sections = total_sections - len(missing_sections)

    structure_score = round(
        (completed_sections / total_sections) * 100, 2
    )

    evaluation = {
        "report_generated": bool(report.strip()),
        "word_count": word_count,
        "total_sources": len(sources),
        "missing_sections": missing_sections,
        "all_sections_present": len(missing_sections) == 0,
        "structure_score": structure_score
    }

    return evaluation

