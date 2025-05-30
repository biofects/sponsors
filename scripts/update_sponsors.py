from github import Github
import os

TOKEN = os.getenv("GH_TOKEN")
if not TOKEN:
    raise Exception("Missing GH_TOKEN in environment")

g = Github(TOKEN)
user = g.get_user()
sponsorships = user.get_sponsorships_received()

monthly = []
one_time = []

for s in sponsorships:
    if s.privacy_level != "PUBLIC":
        continue

    sponsor = s.sponsor
    data = {
        "login": sponsor.login,
        "url": sponsor.html_url,
        "avatar": sponsor.avatar_url,
        "is_monthly": s.tier.monthly_price_in_dollars > 0,
    }

    (monthly if data["is_monthly"] else one_time).append(data)

with open("shoutouts.md", "w") as f:
    f.write("# 🏆 Sponsor Shout-Outs\n\n")

    f.write("## 🌟 Monthly Sponsors\n\n")
    if monthly:
        for s in monthly:
            f.write(f"[<img src=\"{s['avatar']}\" width=\"64\" title=\"{s['login']}\"/>]({s['url']}) ")
        f.write("\n\n")
    else:
        f.write("_No monthly sponsors yet — be the first!_\n\n")

    f.write("---\n\n## 💖 One-Time Sponsors\n\n")
    if one_time:
        for s in one_time:
            f.write(f"- [{s['login']}]({s['url']})\n")
    else:
        f.write("_No one-time sponsors yet — be the first!_\n")
