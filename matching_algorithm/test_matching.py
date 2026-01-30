# test_matching.py

from matching import User, Skill, Interest, compute_match_score, embed_user


def test_basic_skill_overlap():
    u1 = User(
        id=1,
        gradYear=2028,
        level=3,
        xp=100,
        bio="Backend dev",
        skills=[Skill(1, "python"), Skill(2, "django")],
        interests=[Interest(1, "ai"), Interest(2, "ml")]
    )

    u2 = User(
        id=2,
        gradYear=2027,
        level=2,
        xp=50,
        bio="Fullstack dev",
        skills=[Skill(1, "python"), Skill(3, "react")],
        interests=[Interest(1, "ai"), Interest(3, "web")]
    )
    u1=embed_user(u1)
    u2=embed_user(u2)

    score = compute_match_score(u1, u2)
    print("Score:", score)



def test_no_overlap():
    u1 = User(
        id=1,
        gradYear=2027,
        level=1,
        xp=10,
        bio="person1",
        skills=[Skill(1, "c++")],
        interests=[Interest(1, "security")]
    )

    u2 = User(
        id=2,
        gradYear=2029,
        level=10,
        xp=300,
        bio="person2",
        skills=[Skill(2, "javascript")],
        interests=[Interest(2, "design")]
    )

    u1=embed_user(u1)
    u2=embed_user(u2)

    score = compute_match_score(u1, u2)
    print("Score:", score)


def test_full_overlap():
    shared_skills = [Skill(1, "python"), Skill(2, "django")]
    shared_interests = [Interest(1, "ai"), Interest(2, "ml")]

    u1 = User(
        id=1,
        gradYear=2028,
        level=5,
        xp=200,
        bio="bio",
        skills=shared_skills,
        interests=shared_interests
    )

    u2 = User(
        id=2,
        gradYear=2028,
        level=5,
        xp=200,
        bio="same bio",
        skills=shared_skills,
        interests=shared_interests
    )

    u1=embed_user(u1)
    u2=embed_user(u2)

    score = compute_match_score(u1, u2)
    print("Score:", score)


if __name__ == "__main__":
    test_basic_skill_overlap()
    test_no_overlap()
    test_full_overlap()