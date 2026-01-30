def jaccard(a, b):
    a = set(a)
    b = set(b)
    if not a and not b:
        return 0
    return len(a & b) / len(a | b)

def compute_match_score(p1, p2):
    S_skills = jaccard(p1.skills, p2.skills)
    S_interests = jaccard(p1.interests, p2.interests)
    S_goals = jaccard(p1.goals, p2.goals)

    S_roles = 0
    if p1.role_preferred in p2.roles_can_do:
        S_roles += 0.5
    if p2.role_preferred in p1.roles_can_do:
        S_roles += 0.5

    S_exp = 1 - abs(p1.experience_level - p2.experience_level) / 4

    return (
        0.4 * S_skills +
        0.2 * S_roles +
        0.15 * S_interests +
        0.15 * S_goals +
        0.1 * S_exp
    )