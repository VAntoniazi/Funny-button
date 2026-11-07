#!/usr/bin/env python3
"""Audit 250-day GitHub commit gaps and optionally create transparent retrospective notes.

Requires Python 3.9+, Git, and an authenticated GitHub CLI (gh).
Dry run by default. --apply creates local commits; --push sends them to main.
"""

import argparse
import calendar
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

LOGIN = "VAntoniazi"
REPO = "VAntoniazi/Funny-button"
TZ = ZoneInfo("America/Argentina/Buenos_Aires")
QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      commitContributionsByRepository(maxRepositories: 100) {
        repository { nameWithOwner }
        contributions(first: 100) {
          nodes { occurredAt commitCount }
          pageInfo { hasNextPage }
        }
      }
    }
  }
}
"""


def run(*args, env=None):
    return subprocess.run(
        args, check=True, text=True, capture_output=True, env=env
    ).stdout.strip()


def monthly_ranges(first, last):
    cursor = first
    while cursor <= last:
        final_day = calendar.monthrange(cursor.year, cursor.month)[1]
        end = min(last, date(cursor.year, cursor.month, final_day))
        yield cursor, end
        cursor = end + timedelta(days=1)


def audit(first, last):
    days, repos = set(), {}
    for start, end in monthly_ranges(first, last):
        raw = run(
            "gh", "api", "graphql",
            "-f", f"query={QUERY}", "-f", f"login={LOGIN}",
            "-f", f"from={start}T00:00:00Z",
            "-f", f"to={end}T23:59:59Z",
        )
        data = json.loads(raw)
        if data.get("errors"):
            raise RuntimeError(f"Falha GraphQL: {data['errors']}")
        user = (data.get("data") or {}).get("user")
        if not user:
            raise RuntimeError("Usuario nao encontrado ou inacessivel")
        group = user["contributionsCollection"]
        total = 0
        for item in group["commitContributionsByRepository"]:
            repo = item["repository"]["nameWithOwner"]
            connection = item["contributions"]
            if connection["pageInfo"]["hasNextPage"]:
                raise RuntimeError(f"Dados paginados em {repo}; abortando")
            for entry in connection["nodes"]:
                if not entry:
                    continue
                amount = entry["commitCount"]
                total += amount
                day = date.fromisoformat(entry["occurredAt"][:10])
                if amount > 0 and start <= day <= end:
                    days.add(day)
                    repos[repo] = repos.get(repo, 0) + amount
        expected = group["totalCommitContributions"]
        if total != expected:
            raise RuntimeError(
                f"Dados incompletos {start}..{end}: total={expected}, "
                f"detalhado={total}. Nenhum commit sera criado."
            )
    return days, repos


def check_checkout():
    if run("git", "rev-parse", "--is-inside-work-tree") != "true":
        raise RuntimeError("Execute dentro de um clone Git")
    if run("git", "branch", "--show-current") != "main":
        raise RuntimeError("A branch ativa deve ser main")
    remote = run("git", "remote", "get-url", "origin")
    normalized = remote.rstrip("/").removesuffix(".git").replace(
        "github.com:", "github.com/"
    )
    if not normalized.endswith("github.com/" + REPO):
        raise RuntimeError(f"Origin incorreta: {remote}")
    if run("git", "status", "--porcelain"):
        raise RuntimeError("O repositorio deve estar limpo")
    if not run("git", "config", "user.email"):
        raise RuntimeError("Configure um git user.email vinculado ao GitHub")
    run("git", "fetch", "--quiet", "origin", "main")
    if run("git", "rev-parse", "HEAD") != run(
        "git", "rev-parse", "refs/remotes/origin/main"
    ):
        raise RuntimeError("main local diverge de origin/main")


def apply(missing, generated_at, push):
    check_checkout()
    folder = Path("docs/retrospective-gaps")
    paths = [(day, folder / f"{day}.md") for day in missing]
    for day, path in paths:
        if path.exists():
            raise RuntimeError(f"Arquivo ja existe: {path}")
    for day, path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"# Registro retrospectivo: {day}\n\n"
            f"- **Data de referencia:** {day}\n"
            f"- **Data real de producao:** {generated_at}\n"
            f"- **Fonte:** GraphQL contributionsCollection / usuario {LOGIN}.\n"
            "- **Criterio:** nenhum commit contabilizado pelo perfil GitHub "
            "nos repositorios agregados na data de referencia.\n\n"
            "Este arquivo foi criado **retrospectivamente**. Nao afirma "
            "que houve trabalho, desenvolvimento ou entrega na data de referencia. "
            "A data historica do commit e usada para classificar o registro, "
            "nao como evidencia de atividade naquele dia.\n",
            encoding="utf-8",
        )
        stamp = f"{day}T12:00:00-03:00"
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = stamp
        env["GIT_COMMITTER_DATE"] = stamp
        run("git", "add", "--", str(path))
        run("git", "commit", "-m",
            f"docs(retrospective): register historical gap {day}", env=env)
    print(f"{len(paths)} commits criados localmente na main, sem reescrever historico.")
    if push and paths:
        run("git", "push", "origin", "main")
        print("Push concluido para origin/main.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=250)
    parser.add_argument("--end-date", type=date.fromisoformat,
                        default=datetime.now(TZ).date())
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.days <= 365:
        parser.error("--days deve estar entre 1 e 365")
    if args.push and not args.apply:
        parser.error("--push exige --apply")
    if args.end_date > datetime.now(TZ).date():
        parser.error("--end-date nao pode ser futura")
    start = args.end_date - timedelta(days=args.days - 1)
    present, repos = audit(start, args.end_date)
    missing = [
        start + timedelta(days=i)
        for i in range(args.days)
        if start + timedelta(days=i) not in present
    ]
    print(json.dumps({
        "usuario": LOGIN, "destino": REPO,
        "inicio": str(start), "fim": str(args.end_date),
        "dias_analisados": args.days, "dias_com_commit": len(present),
        "dias_sem_commit": len(missing),
        "repositorios_com_commits": len(repos),
        "datas_sem_commit": [str(d) for d in missing]
    }, ensure_ascii=False, indent=2))
    if args.apply and missing:
        generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
        apply(missing, generated, args.push)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, subprocess.CalledProcessError, ValueError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        sys.exit(1)
