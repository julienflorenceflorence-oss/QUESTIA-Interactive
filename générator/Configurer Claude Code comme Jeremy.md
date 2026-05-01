# **Configurer Claude Code comme Jeremy**

Guide complet pour repliquer la configuration Claude Code de Jeremy : reglages, MCP servers, skills, agents SEO, bonnes pratiques, et workflows.

---

## **1\. Reglages Claude Code (`~/.claude/settings.json`)**

Cree ou edite `~/.claude/settings.json` :

{  
  "permissions": {  
    "allow": \[  
      "Bash(claude mcp add:\*)",  
      "Bash(claude mcp list:\*)",  
      "Bash(claude config:\*)",  
      "Bash(git clone:\*)",  
      "Bash(npm install:\*)",  
      "Bash(npm run:\*)",  
      "Bash(mkdir:\*)",  
      "Bash(curl:\*)",  
      "Bash(ls:\*)"  
    \],  
    "deny": \[\],  
    "defaultMode": "bypassPermissions"  
  },  
  "language": "French",  
  "alwaysThinkingEnabled": true,  
  "effortLevel": "high",  
  "voiceEnabled": true,  
  "providerPriority": \[  
    "claude",  
    "gemini",  
    "codex",  
    "openai"  
  \],  
  "enabledPlugins": {  
    "context7@claude-plugins-official": true,  
    "ralph-loop@claude-plugins-official": true,  
    "frontend-design@claude-plugins-official": true  
  },  
  "statusLine": {  
    "type": "command",  
    "command": "npx \-y ccstatusline@latest"  
  },  
  "mcpServers": {}  
}

### **Explication des reglages cles**

| Reglage | Valeur | Pourquoi |
| ----- | ----- | ----- |
| `language` | `"French"` | Claude repond toujours en francais |
| `alwaysThinkingEnabled` | `true` | Claude reflechit avant chaque reponse (meilleure qualite) |
| `effortLevel` | `"high"` | Reponses plus completes et approfondies |
| `voiceEnabled` | `true` | Mode vocal dispo (maintenir Espace pour parler) |
| `defaultMode` | `"bypassPermissions"` | Claude execute sans demander confirmation a chaque fois |
| `providerPriority` | claude en premier | Utilise Claude en priorite, fallback sur d'autres |

### **Plugins actives**

| Plugin | Usage |
| ----- | ----- |
| **context7** | Documentation a jour pour n'importe quelle librairie |
| **ralph-loop** | Boucle de monitoring recurrente |
| **frontend-design** | Generation d'interfaces frontend avec design soigne |

---

## **2\. MCP Servers (Model Context Protocol)**

Les MCP servers donnent a Claude des super-pouvoirs : acces a des APIs, bases de donnees, outils externes.

### **MCP essentiels a installer**

Ajoute dans la section `mcpServers` de `~/.claude/settings.json` :

#### **Filesystem (acces fichiers locaux)**

"filesystem": {  
  "command": "npx",  
  "args": \[  
    "-y",  
    "@modelcontextprotocol/server-filesystem",  
    "/Users/TON\_USER/Desktop",  
    "/Users/TON\_USER/Downloads",  
    "/Users/TON\_USER/obsidian-vault"  
  \]  
}

#### **Google Search Console**

"gsc": {  
  "command": "npx",  
  "args": \["-y", "mcp-server-gsc"\],  
  "env": {  
    "GOOGLE\_APPLICATION\_CREDENTIALS": "/chemin/vers/ton/service-account.json"  
  }  
}

Pour configurer GSC :

1. Cree un projet Google Cloud  
2. Active l'API Search Console  
3. Cree un Service Account avec acces en lecture  
4. Telecharge le JSON de credentials  
5. Ajoute le Service Account comme utilisateur dans GSC

#### **Google Drive**

"gdrive": {  
  "command": "npx",  
  "args": \["-y", "@modelcontextprotocol/server-gdrive"\],  
  "env": {  
    "GOOGLE\_CLIENT\_ID": "ton-client-id.apps.googleusercontent.com",  
    "GOOGLE\_CLIENT\_SECRET": "GOCSPX-xxx",  
    "GOOGLE\_REDIRECT\_URI": "http://localhost:4000/oauth2callback"  
  }  
}

#### **Chrome DevTools (automatisation navigateur)**

"chrome-devtools": {  
  "command": "npx",  
  "args": \["-y", "chrome-devtools-mcp@latest", "--no-usage-statistics"\]  
}

#### **GitLab**

"gitlab": {  
  "command": "npx",  
  "args": \["-y", "@modelcontextprotocol/server-gitlab"\],  
  "env": {  
    "GITLAB\_URL": "https://gitlab.com",  
    "GITLAB\_TOKEN": "glpat-ton-token-ici"  
  }  
}

Pour creer le token : GitLab → Settings → Access Tokens → scope `api`.

#### **Haloscan (SEO France)**

"haloscan": {  
  "type": "stdio",  
  "command": "npx",  
  "args": \["@occirank/haloscan-mcp-claude-code"\],  
  "env": {  
    "HALOSCAN\_API\_KEY": "ton-api-key"  
  }  
}

Inscription : [https://haloscan.com](https://haloscan.com) — API key dans les parametres du compte.

#### **CrazySERP (analyse SERP)**

"crazyserp": {  
  "command": "npx",  
  "args": \["-y", "@anthropic/mcp-crazyserp"\],  
  "env": {  
    "CRAZYSERP\_API\_KEY": "sk\_xxx"  
  }  
}

#### **NeuronWriter (optimisation contenu NLP)**

Pour celui-ci il faut un MCP custom. Voir la section "MCP servers custom" plus bas.

#### **WiseWand (generation contenu SEO)**

MCP custom Python :

"wisewand": {  
  "command": "/chemin/vers/wisewand-mcp/.venv/bin/wisewand-mcp",  
  "env": {  
    "WISEWAND\_API\_KEY": "sk\_live\_xxx"  
  }  
}

### **MCP servers custom (a builder soi-meme)**

Jeremy stocke ses MCP custom dans `~/projects/claude/mcp-servers/`. Structure type :

mcp-servers/  
├── contabo-mcp/          \# Gestion VPS Contabo  
├── cpanel-mcp/           \# Administration cPanel/o2switch  
├── internetbs-mcp/       \# Gestion DNS et domaines  
├── neuronwriter-mcp/     \# Optimisation NLP  
├── wisewand-mcp/         \# Generation contenu  
└── gnewsalyzer-mcp/      \# Analyse Google News

Pour creer un nouveau MCP server :

mkdir \~/projects/claude/mcp-servers/mon-mcp  
cd \~/projects/claude/mcp-servers/mon-mcp  
npm init \-y  
npm install @modelcontextprotocol/sdk zod  
\# Coder dans src/index.ts, puis build

---

## **3\. Skills (commandes slash specialisees)**

Les skills sont des prompts spcialises declenches par `/nom-du-skill`.

### **Installer les skills**

Les skills se placent dans `~/.claude/skills/`. Chaque skill est un dossier avec un fichier `skill.md` :

\~/.claude/skills/  
├── humanizer/               \# Desindexer les traces d'IA dans le texte  
├── prompt-generator/        \# Crafting de prompts production-grade  
├── product-manager-toolkit/  \# RICE, interviews, PRD, discovery  
├── reverse-engineering/     \# Scraping, reverse API, analyse trafic  
├── wayback-rebuilder/       \# Reconstruire un site depuis Wayback Machine  
├── link-analyzer/           \# Analyse liens internes/externes  
├── seo-wordpress-manager/   \# MAJ Yoast SEO en batch via GraphQL  
├── gitlab-workflow/         \# Workflow GitLab complet (issues, MR, wiki)  
├── agentation/              \# Feedback visuel navigateur → agent IA  
├── agentation-self-driving/ \# Critique design autonome via navigateur  
├── wordpress-router/        \# Classification auto de projets WordPress  
├── wp-block-development/    \# Dev blocks Gutenberg  
├── wp-block-themes/         \# Dev themes bloc  
├── wp-plugin-development/   \# Dev plugins WordPress  
├── wp-performance/          \# Optimisation perf WordPress  
├── wp-rest-api/             \# Dev REST API WordPress  
├── wp-wpcli-and-ops/        \# WP-CLI et operations  
├── wp-phpstan/              \# PHPStan pour WordPress  
├── wp-interactivity-api/    \# Interactivity API WordPress  
├── wp-playground/           \# WordPress Playground  
├── wp-project-triage/       \# Inspection et classification repo WP  
├── wp-abilities-api/        \# WordPress Abilities API  
├── wpds/                    \# WordPress Design System  
├── astro-cta-injector/      \# Injection CTA dans sites Astro  
├── n8n-code-javascript/     \# Code JavaScript dans n8n  
├── n8n-code-python/         \# Code Python dans n8n  
├── n8n-expression-syntax/   \# Expressions n8n  
├── n8n-mcp-tools-expert/    \# Outils MCP n8n  
├── n8n-node-configuration/  \# Configuration nodes n8n  
├── n8n-validation-expert/   \# Validation workflows n8n  
└── n8n-workflow-patterns/   \# Patterns d'architecture n8n

### **Sources des skills**

* **Plugins officiels** : [https://github.com/anthropics/claude-code-plugins](https://github.com/anthropics/claude-code-plugins) (cloner dans `~/.claude/agents/`)  
* **Skills custom** : ecrits a la main, un `skill.md` par dossier  
* **WordPress skills** : [https://github.com/developer-jeremysantos/wordpress-claude-skills](https://github.com/developer-jeremysantos/wordpress-claude-skills) (a adapter)

### **Structure d'un skill**

mon-skill/  
└── skill.md

Contenu de `skill.md` :

\---  
description: Description courte du skill (affichee dans la liste)  
\---

\# Nom du Skill

Instructions detaillees pour Claude quand le skill est active...

---

## **4\. Agents SEO (systeme complet)**

Jeremy utilise un systeme de 14 agents SEO specialises \+ 3 agents marketing.

### **Installation**

cd \~/.claude  
git clone https://github.com/wshobson/agents agents

Cela installe 68 plugins d'agents dans `~/.claude/agents/plugins/`.

### **Agents SEO disponibles (via `/seo`)**

| Agent | Role |
| ----- | ----- |
| **seo-pre-audit** | Pre-audit SEO complet et automatise |
| **seo-content-writer** | Redaction contenu optimise SEO |
| **seo-content-auditor** | Audit qualite \+ E-E-A-T |
| **seo-content-planner** | Topic clusters \+ calendrier editorial |
| **seo-meta-optimizer** | Titles, meta descriptions, URLs |
| **seo-keyword-strategist** | Strategie mots-cles \+ LSI |
| **seo-structure-architect** | Structure Hn \+ schema markup \+ maillage |
| **seo-snippet-hunter** | Optimisation featured snippets |
| **seo-content-refresher** | Mise a jour contenu vieillissant |
| **seo-cannibalization-detector** | Detection cannibalisation KW |
| **seo-authority-builder** | Signaux E-E-A-T \+ autorite |
| **content-marketer** | Marketing multicanal |
| **search-specialist** | Recherche web avancee |
| **sales-automator** | Emails, propositions, outreach |

### **Commande slash `/seo`**

Cree `~/.claude/commands/seo.md` avec le prompt de l'orchestrateur (demande-le a Jeremy ou copie depuis son setup).

---

## **5\. Commandes slash custom (`~/.claude/commands/`)**

Jeremy a 4 commandes custom :

| Commande | Fichier | Usage |
| ----- | ----- | ----- |
| `/seo` | `seo.md` | Orchestrateur 14 agents SEO |
| `/audit` | `audit.md` | Pre-audit technique (SEO, perf, securite) |
| `/n8n` | `n8n.md` | Assistant creation/debug workflows n8n |
| `/mcp` | `mcp.md` | Gestionnaire MCP servers (status, debug, ajout) |

Pour les creer, place un fichier `.md` dans `~/.claude/commands/` :

\---  
description: Description affichee dans le menu  
\---

\# Titre

Instructions pour Claude quand la commande est activee...

---

## **6\. CLAUDE.md global (`~/.claude/CLAUDE.md`)**

C'est le fichier le plus important. Il definit le comportement de Claude dans TOUS les projets.

Cree `~/.claude/CLAUDE.md` avec ces sections :

\# Directives de developpement

\#\# Framework Spec-Kit (OBLIGATOIRE)

Avant chaque tache de developpement, suivre l'approche Specification-Driven Development :  
1\. Constitution → Principes directeurs  
2\. Specify → Requirements SANS prescrire la tech  
3\. Plan → Strategie d'implementation  
4\. Tasks → Liste de taches actionnables  
5\. Implement → Execution

Commandes : /speckit.constitution, /speckit.specify, /speckit.plan, /speckit.tasks, /speckit.implement

Installation : uv tool install specify-cli \--from git+https://github.com/github/spec-kit.git

Regles :  
\- TOUJOURS separer le "quoi" du "comment"  
\- Les specs definissent l'intention AVANT les details  
\- Utiliser /speckit.clarify en cas de doute

\---

\#\# Obsidian Vault — Second cerveau (OBLIGATOIRE)

Le vault \~/obsidian-vault/ est la memoire persistante partagee.

\#\#\# Debut de session (TOUJOURS)  
1\. Lire \~/obsidian-vault/Memory/INDEX.md  
2\. Si un projet est identifie, lire \~/obsidian-vault/Memory/projects/\[nom\].md  
3\. Lire la note du jour \~/obsidian-vault/Daily/YYYY-MM-DD.md (la creer si absente)

\#\#\# Pendant le travail  
\- Pieges, patterns, faits importants → \~/obsidian-vault/Memory/patterns/  
\- Decisions d'architecture → \~/obsidian-vault/Memory/decisions/YYYY-MM-DD-titre.md  
\- Mettre a jour \~/obsidian-vault/Memory/INDEX.md a chaque nouvelle entree

\#\#\# Fin de session  
\- Resume dans \~/obsidian-vault/Memory/sessions/YYYY-MM-DD-sujet.md  
\- Mettre a jour la note du jour

\#\#\# Regles  
\- Wikilinks \[\[note\]\] dans le vault  
\- Frontmatter YAML avec date et tags  
\- Ne PAS modifier les fichiers dans \~/obsidian-vault/.claude/skills/

\---

\#\# Workflow Orchestration

\#\#\# Plan Mode (toute tache non-triviale)  
\- Entrer en mode plan pour toute tache de 3+ etapes  
\- Si l'approche derape : STOP immediat, re-planifier  
\- Ne pas s'enteter sur une approche qui ne fonctionne pas

\#\#\# Strategie Subagents  
\- Utiliser les subagents pour garder le contexte principal propre  
\- Un sujet par subagent  
\- Paralleliser quand possible

\#\#\# Boucle d'apprentissage  
\- Apres toute correction : ecrire la lecon dans \~/obsidian-vault/Memory/patterns/lessons.md  
\- Formuler la regle qui empeche de refaire l'erreur  
\- Ne jamais marquer une tache terminee sans prouver qu'elle fonctionne

\---

\#\# Bonnes pratiques projet

\#\#\# Documentation en 3 tiers  
\- Tier 1 (.claude/docs/) : Quick references, toujours chargees (\~1000 lignes max)  
\- Tier 2 (docs externes) : Doc complete, accedee par grep cible  
\- Tier 3 (catalogues) : Fichiers volumineux, grep only, JAMAIS lire en entier

\#\#\# Verification des APIs externes  
Avant de coder contre une API tierce :  
1\. Verifier les signatures reelles  
2\. Documenter dans .claude/docs/verified-apis.md  
3\. Noter les ecarts entre doc officielle et comportement reel

\#\#\# Hygiene du CLAUDE.md projet  
\- Le CLAUDE.md projet doit rester court (\<100 lignes)  
\- Deplacer architecture et exemples dans .claude/docs/  
\- Ne jamais melanger "quoi faire" et "comment c'est construit"

---

## **7\. Library (playbooks, prompts, templates)**

Jeremy a une bibliotheque de references dans `~/.claude/library/` :

\~/.claude/library/  
├── playbooks/  
│   ├── gitlab-workflow.md      \# Workflow GitLab complet  
│   ├── new-mcp-server.md       \# Comment creer un MCP server  
│   ├── project-setup.md        \# Setup d'un nouveau projet  
│   └── seo-workflow.md         \# Workflow SEO  
├── prompts/  
│   ├── code-review.md          \# Prompt pour review de code  
│   ├── content-brief.md        \# Brief de contenu SEO  
│   └── seo-audit.md            \# Prompt d'audit SEO  
└── templates/  
    ├── mcp-server-claude.md    \# Template CLAUDE.md pour MCP servers  
    ├── n8n-workflow-claude.md   \# Template CLAUDE.md pour workflows n8n  
    └── wordpress-project-claude.md \# Template CLAUDE.md pour projets WP

### **Playbook : Setup d'un nouveau projet**

\# 1\. Creer le dossier  
mkdir \~/projects/{categorie}/{nom-projet}  
cd \~/projects/{categorie}/{nom-projet}  
git init

\# Categories : claude, wordpress, seo, automation, web, learning, clients, crypto

\# 2\. Initialiser Claude Code  
mkdir \-p .claude  
cp \~/.claude/library/templates/{type}-project-claude.md .claude/CLAUDE.md

\# 3\. Spec-Kit (si projet de dev)  
specify init {NOM\_PROJET} \--ai claude

\# 4\. GitLab (si applicable)  
\# Via MCP gitlab : create\_issue → dev → create\_merge\_request → merge

---

## **8\. Hooks (automatisations)**

Les hooks executent des commandes automatiquement a certains moments.

Cree `~/.claude/hooks.json` :

{  
  "hooks": {  
    "SessionStart": \[  
      {  
        "matcher": "startup|clear|compact",  
        "hooks": \[  
          {  
            "type": "command",  
            "command": "echo 'Session demarree'",  
            "timeout": 30  
          }  
        \]  
      }  
    \]  
  }  
}

Jeremy utilise le plugin **thedotmack** qui ajoute des hooks avances (smart-install, worker-service, contexte automatique, resume de session). Pour l'installer :

cd \~/.claude/plugins/marketplaces  
git clone https://github.com/thedotmack/claude-code-plugin thedotmack

---

## **9\. Checklist d'installation rapide**

\# 1\. Installer Claude Code  
npm i \-g @anthropic-ai/claude-code

\# 2\. Creer la structure  
mkdir \-p \~/.claude/{skills,commands,agents,library/{playbooks,prompts,templates},mcp-servers}  
mkdir \-p \~/projects/claude/mcp-servers  
mkdir \-p \~/obsidian-vault/Memory/{projects,decisions,patterns,sessions}  
mkdir \-p \~/obsidian-vault/{Daily,Templates,Guides}

\# 3\. Copier les fichiers de config  
\# \- \~/.claude/settings.json (reglages \+ MCP)  
\# \- \~/.claude/CLAUDE.md (directives globales)  
\# \- \~/.claude/commands/\*.md (commandes slash)

\# 4\. Installer les agents SEO  
cd \~/.claude && git clone https://github.com/wshobson/agents agents

\# 5\. Installer les skills (copier depuis un zip ou repo)  
\# Chaque skill \= un dossier dans \~/.claude/skills/ avec un skill.md

\# 6\. Installer Spec-Kit  
uv tool install specify-cli \--from git+https://github.com/github/spec-kit.git

\# 7\. Installer la statusline  
npx \-y ccstatusline@latest

\# 8\. Installer les plugins officiels Claude  
\# context7, ralph-loop, frontend-design sont actives dans settings.json

\# 9\. Configurer les MCP servers  
\# Ajouter chaque MCP dans settings.json avec les API keys

\# 10\. Creer le vault Obsidian et configurer Syncthing  
\# Voir le guide : Guides/partager-obsidian-claude-code-openclaw.md

---

## **10\. Arborescence complete de reference**

\~/.claude/  
├── CLAUDE.md                    \# Directives globales (le plus important)  
├── settings.json                \# Reglages \+ MCP servers \+ plugins  
├── settings.local.json          \# Overrides locaux  
├── hooks.json                   \# Automatisations  
├── commands/                    \# Commandes slash custom  
│   ├── seo.md                   \#   /seo \- orchestrateur SEO  
│   ├── audit.md                 \#   /audit \- pre-audit technique  
│   ├── n8n.md                   \#   /n8n \- assistant workflows  
│   └── mcp.md                   \#   /mcp \- gestion MCP servers  
├── skills/                      \# Skills (prompts specialises)  
│   ├── humanizer/  
│   ├── prompt-generator/  
│   ├── reverse-engineering/  
│   ├── wordpress-router/  
│   ├── wp-\*/                    \# 12 skills WordPress  
│   ├── n8n-\*/                   \# 7 skills n8n  
│   └── ...  
├── agents/                      \# Agents SEO (wshobson/agents)  
│   ├── plugins/  
│   │   ├── seo-pre-audit/  
│   │   ├── seo-content-creation/  
│   │   ├── seo-technical-optimization/  
│   │   ├── seo-analysis-monitoring/  
│   │   └── content-marketing/  
│   └── docs/  
├── library/                     \# Bibliotheque de references  
│   ├── playbooks/               \# Guides pas-a-pas  
│   ├── prompts/                 \# Prompts reutilisables  
│   └── templates/               \# Templates CLAUDE.md par type de projet  
├── mcp-servers/                 \# MCP servers custom locaux  
│   └── mcp-gitlab/  
├── plugins/                     \# Plugins  
│   └── marketplaces/  
│       ├── anthropic-agent-skills/  
│       ├── claude-plugins-official/  
│       └── thedotmack/  
└── projects/                    \# Memoire par projet (auto)  
    └── \-/  
        └── memory/  
            └── MEMORY.md

\~/projects/claude/mcp-servers/   \# MCP servers custom (code source)  
├── contabo-mcp/  
├── cpanel-mcp/  
├── gsc-mcp/  
├── internetbs-mcp/  
├── neuronwriter-mcp/  
├── wisewand-mcp/  
└── ...

\~/obsidian-vault/                \# Vault Obsidian (memoire partagee)  
├── Memory/  
│   ├── INDEX.md  
│   ├── projects/  
│   ├── decisions/  
│   ├── patterns/  
│   └── sessions/  
├── Daily/  
└── ...

---

## **Recap : ce qui fait la difference**

1. **CLAUDE.md global** : definit le comportement de Claude partout  
2. **Spec-Kit** : workflow specification-driven pour chaque feature  
3. **Obsidian Vault** : memoire persistante partagee entre sessions et machines  
4. **14 agents SEO** : systeme complet d'optimisation SEO  
5. **MCP servers** : Claude accede directement aux APIs (GSC, Haloscan, GitLab, Drive...)  
6. **Skills specialises** : prompts optimises pour WordPress, n8n, SEO, etc.  
7. **Plan Mode** : toujours planifier avant d'implementer  
8. **Boucle d'apprentissage** : documenter chaque lecon pour ne pas repeter les erreurs  
9. **Documentation 3 tiers** : optimiser l'utilisation du contexte  
10. **Subagents** : paralleliser et garder le contexte propre

