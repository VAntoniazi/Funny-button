# Auditoria e documentação retrospectiva de contribuições

## Escopo

- **Conta analisada:** `VAntoniazi`.
- **Período:** 250 dias corridos, de **2026-03-03** a **2026-11-07**, inclusive.
- **Destino dos registros:** somente a branch `main` deste repositório (`VAntoniazi/Funny-button`).
- **Origem da atividade:** contribuições de **commits** associadas à conta GitHub, agrupadas por repositório, incluindo os demais projetos acessíveis e contabilizados no perfil. Não se considera a ausência de commits neste repositório, isoladamente, como ausência global de atividade.

## Critério

O auditor usa a API GraphQL `user.contributionsCollection.commitContributionsByRepository`, por janelas mensais, e agrega as datas dos commits de todos os repositórios retornados. A contagem agregada é conciliada com `totalCommitContributions`. Se houver discrepância, a operação para sem criar commits.

A consulta cobre contribuições que o GitHub contabiliza para o perfil autenticado. Ela não comprova ausência de trabalho fora do GitHub, em branches não elegíveis para contribuições, nem em repositórios inacessíveis. Os dias são tratados conforme as datas de contribuição retornadas pelo GitHub.

## Execução

A partir de uma cópia limpa do repositório, com Git e GitHub CLI (`gh`) autenticados:

```bash
git switch main
git pull --ff-only origin main

# Apenas auditar, sem escrever nada:
python3 scripts/audit_commit_gaps.py --days 250 --end-date 2026-11-07

# Após conferir as datas, gerar registros locais e enviar à main:
python3 scripts/audit_commit_gaps.py --days 250 --end-date 2026-11-07 --apply --push
```

O modo padrão é **somente leitura**. O modo `--apply` exige `main` limpa, `origin` correto e igualdade com `origin/main`. Cada registro fica em `docs/retrospective-gaps/AAAA-MM-DD.md`. Ele cria commits novos, sem alterar commits anteriores, sem novas branches e sem `force-push`. O `--push` publica apenas depois da criação local.

## Proveniência e interpretação

**Estes registros são retrospectivos, não trabalhos realizados nas datas vazias.** Cada arquivo declara explicitamente a data de referência e a data real em que foi gerado. O uso de datas de autor/committer históricas, quando autorizado e aplicado, não deve ser usado como comprovação de atividade de desenvolvimento ocorrida naquele dia.

A data histórica em um commit pode alterar a aparência do gráfico de contribuições do GitHub. O GitHub usa a data do autor para o perfil; exige e-mail de autoria vinculado à conta e que outras condições de contagem sejam atendidas.

## Segurança

- Não modifica aplicações, arquivos existentes ou fluxos de deploy.
- Não sobrescreve documentação histórica.
- Não usa GitHub Actions nem cria pipelines.
- Não faz rebase, reset ou push forçado.
- Suspende a execução se os dados estiverem incompletos ou o repositório local divergir de `origin/main`.
