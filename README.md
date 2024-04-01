# pr-agent-wiki-conf
Community version of [PR-Agent Wiki configuration file](https://pr-agent-docs.codium.ai/usage-guide/configuration_options/#wiki-configuration-file)

# Why?
[PR-Agent Wiki configuration file](https://pr-agent-docs.codium.ai/usage-guide/configuration_options/#wiki-configuration-file) feature is currently only available in the paid version ([PR-Agent Pro](https://www.codium.ai/pricing/))

# How does it work
Note: current support is `extra_instructions` config only

1. Load `.pr_agent.toml` configuration from Wiki page
1. Add `common_instructions` into each extra_instructions configs
1. Set each extra_instructions to environment variables

# How to Use
- See details [GitHub Actions](https://github.com/idubnori/pr-agent-wiki-conf/actions)
- Example of [.pr_agent.toml](https://github.com/idubnori/pr-agent-wiki-conf/wiki/.pr_agent.toml)
```yaml
on:
  pull_request:
    types: [opened, reopened, ready_for_review]
  issue_comment:
jobs:
  pr_agent_job:
    if: ${{ github.event.sender.type != 'Bot' }}
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write
      contents: write
    steps:
      - name: PR-Agent Wiki Configuration
        uses: idubnori/pr-agent-wiki-conf@main
        env:
          common_instructions: >-
            - Please use Japanese in descriptions.
      - name: PR Agent action step
        id: pragent
        uses: Codium-ai/pr-agent@main
        env:
          OPENAI_KEY: ${{ secrets.OPENAI_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```