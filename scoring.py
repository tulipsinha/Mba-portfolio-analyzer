import json

def load_colleges():
    with open("data/colleges.json") as f:
        data = json.load(f)
    return data["colleges"]


def score_academics(profile_academics):
    """
    Turns three percentages into one 0-100 academic strength score.
    We average class 10, class 12, and graduation percent equally.
    """
    values = [
        profile_academics["class_10_percent"],
        profile_academics["class_12_percent"],
        profile_academics["graduation_percent"]
    ]
    return sum(values) / len(values)


def score_exam(entrance_exam):
    """
    The exam percentile is already 0-100, so we use it directly.
    """
    return entrance_exam["percentile"]


def score_work_experience(work_experience):
    """
    Work experience score caps out at 5 years = 100 points.
    Beyond 5 years doesn't add extra score in this simple model,
    since most colleges value a sweet spot (2-5 years), not endless experience.
    """
    years = work_experience["years"]
    capped_years = min(years, 5)
    return (capped_years / 5) * 100


def calculate_college_score(profile, college):
    """
    Combines the three sub-scores using THIS college's specific weightage.
    Only factors present in the college's weightage are counted.
    """
    weightage = college["weightage"]
    total_score = 0
    total_weight_used = 0

    if "academics" in weightage:
        academic_score = score_academics(profile["academics"])
        total_score += academic_score * (weightage["academics"] / 100)
        total_weight_used += weightage["academics"]

    if "entrance_exam_score" in weightage:
        exam_score = score_exam(profile["entrance_exam"])
        total_score += exam_score * (weightage["entrance_exam_score"] / 100)
        total_weight_used += weightage["entrance_exam_score"]

    if "work_experience" in weightage:
        we_score = score_work_experience(profile["work_experience"])
        total_score += we_score * (weightage["work_experience"] / 100)
        total_weight_used += weightage["work_experience"]

    # Scale to account for weightage we couldn't calculate
    # (e.g. essays, interviews - things we don't score numerically yet)
    if total_weight_used > 0:
        final_score = (total_score / total_weight_used) * 100
    else:
        final_score = 0

    return round(final_score, 1)


def score_profile_against_all_colleges(profile):
    """
    Runs the scoring for every college and returns a list of results.
    """
    colleges = load_colleges()
    results = []

    for college in colleges:
        score = calculate_college_score(profile, college)
        results.append({
            "college_id": college["id"],
            "college_name": college["name"],
            "score": score
        })

    # Sort so the best-fit college shows first
    results.sort(key=lambda r: r["score"], reverse=True)
    return results