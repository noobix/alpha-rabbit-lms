---
Author: Kelvin Kabute
Last-updated: 2026-05-06
---

# Semantic Versioning Release Workflow Specification

_Based on `build.md` requirements for Alpha Rabbit LMS_

---

## 🎯 CORE REQUIREMENTS

### 1. Build Number System (Lightweight Tags)

- **Format**: `[YY***]` where `YY` = last 2 digits of year (2026 → `26`)
- **Range**: `[261]` to `[26999]` (5-digit maximum)
- **Continuity**: Sequential across sprints (Sprint 3 ends at `[2645]` → Sprint 4 starts at `[2646]`)
- **Binding**: Each build number tied to specific commit hash via lightweight tag
- **Purpose**: Internal tracking only (not part of semantic version)

### 2. Semantic Versioning Structure

- **Format**: `MAJOR.MINOR.PATCH`
- **Patch Increment**: Every PR merge → +1 PATCH version
- **Minor Increment**: Complete sprint cycle → +1 MINOR version
- **Major Increment**: Significant architecture changes → +1 MAJOR version
- **Build Numbers**: Never in version string; only in annotated tag descriptions

### 3. Annotated Tag Content Requirements

Each annotated tag must contain:

```markdown
Build #[261]
Changes:

- [Issue Description] eg: "Set up PouchDB with SQLite adapter for offline storage"
- [Additional PR acceptance criteria paraphrased]

[Full PR description content]
```

---

## 🔧 AUTOMATION WORKFLOW

### Phase 1: PR Merge → Patch Release

**Trigger**: PR merged to `testing-main` branch  
**Actions**:

1. Extract PR number and build number from branch name (`LMS-101/implement-sha256-hashing...` → `LMS-101`)
2. Increment PATCH version: `1.0.0` → `1.0.1`
3. Create lightweight tag: `git tag [261] <commit-hash>`
4. Create annotated tag:

   ```bash
   git tag -a v1.0.1 -m "Build #[261]
   Changes:
   - LMS-101: Implement SHA-256 hashing for Ghana Card ID storage

   [PR description content]"
   ```

5. Push tags: `git push origin [261] v1.0.1`

### Phase 2: Sprint Completion → Minor Release

**Trigger**: All sprint tickets completed + PR merged with `[minor-release]` label  
**Actions**:

1. Aggregate all build numbers from current MINOR cycle
2. Increment MINOR version: `1.0.0` → `1.1.0`
3. Create comprehensive annotated tag:

   ```markdown
   Minor Release v1.1.0
   Builds Included: [261], [262], [263]...[287]

   Sprint 1 Completed:

   - LMS-101: SHA-256 hashing implementation
   - LMS-102: Incremental backup with WhatsApp compression
   - LMS-103: 30-second auto-save for power outages
   - [All sprint ticket summaries]

   [Comprehensive release notes]
   ```

### Phase 3: Production Deployment

**Trigger**: Annotated tag pushed to `main` branch  
**Actions**:

1. CI/CD builds production artifact
2. Deploys to Vercel/GitHub Pages
3. Updates release documentation
4. Notifies stakeholders

---

## 🤖 CI/CD PIPELINE REQUIREMENTS

### GitHub Actions Workflow (`release.yml`)

```yaml
name: Semantic Release

on:
  pull_request:
    types: [closed]
    branches: [testing-main]
  push:
    tags:
      - "v*.*.*"

jobs:
  patch-release:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0 # Required for tag operations

      - name: Extract PR info
        id: pr_info
        run: |
          BRANCH="${{ github.head_ref }}"
          ISSUE=$(echo "$BRANCH" | cut -d'/' -f1)
          echo "issue=$ISSUE" >> $GITHUB_OUTPUT
          # Get next build number from file
          echo "build_num=$(cat .build_counter)" >> $GITHUB_OUTPUT

      - name: Increment patch version
        id: version
        run: |
          # Read current version from package.json
          CURRENT=$(npm pkg get version --json | tr -d '"')
          # Increment patch: 1.0.0 → 1.0.1
          NEW=$(echo $CURRENT | awk -F. '{$NF = $NF + 1;} 1' | sed 's/ /./g')
          echo "new_version=$NEW" >> $GITHUB_OUTPUT

      - name: Create lightweight tag
        run: |
          git config --global user.name 'CI Bot'
          git config --global user.email 'ci@alpharabbit.dev'
          git tag "[${{ steps.pr_info.outputs.build_num }}]" HEAD

      - name: Create annotated tag
        run: |
          PR_DESC=$(gh pr view ${{ github.event.pull_request.number }} --json body --jq '.body')
          ISSUE_TITLE=$(gh issue view ${{ steps.pr_info.outputs.issue }} --json title --jq '.title')
          TAG_MSG="Build #[${{ steps.pr_info.outputs.build_num }}]
          Changes:
          - ${{ steps.pr_info.outputs.issue }}: $ISSUE_TITLE

          $PR_DESC"
          echo "$TAG_MSG" > tag_message.txt
          git tag -a "v${{ steps.version.outputs.new_version }}" -F tag_message.txt

      - name: Push tags
        run: |
          git push origin "[${{ steps.pr_info.outputs.build_num }}]" "v${{ steps.version.outputs.new_version }}"

      - name: Update build counter
        run: |
          echo $(( ${{ steps.pr_info.outputs.build_num }} + 1 )) > .build_counter
          git add .build_counter
          git commit -m "chore: increment build counter to $(( ${{ steps.pr_info.outputs.build_num }} + 1 ))"
          git push origin testing-main

  minor-release:
    if: contains(github.event.head_commit.message, '[minor-release]')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Generate minor release tag
        run: |
          # Aggregate all builds since last minor release
          # Create comprehensive annotated tag
          # Push to main branch
```

### Required Repository Files

1. **`.build_counter`** (tracked in repo):

   ```
   261
   ```

2. **`package.json`** (version tracking):

   ```json
   {
     "name": "alpha-rabbit-lms",
     "version": "1.0.0",
     "scripts": {
       "release:patch": "node scripts/release-patch.js",
       "release:minor": "node scripts/release-minor.js"
     }
   }
   ```

3. **`scripts/release-patch.js`** (local dev helper):
   ```javascript
   // Automates patch release process for local development
   // Reads .build_counter, creates tags, updates counter
   ```

---

## 📋 VALIDATION CHECKLIST

### Pre-Implementation

- [ ] Confirm build number starting point (`261` for 2026)
- [ ] Verify PR description format matches requirements
- [ ] Establish initial version baseline (`1.0.0`)
- [ ] Create `.build_counter` file with starting number

### Post-Implementation

- [ ] Lightweight tags created: `[261]`, `[262]`, etc.
- [ ] Annotated tags contain build numbers + PR content
- [ ] Semantic versions follow `MAJOR.MINOR.PATCH` strictly
- [ ] Minor releases aggregate all builds from sprint cycle
- [ ] CI pipeline handles both patch and minor release triggers
- [ ] Build counter increments automatically after each PR merge

### Compliance Verification

- [ ] No build numbers in semantic version strings (`v1.0.1` not `v1.0.1-261`)
- [ ] All PR acceptance criteria paraphrased in tag descriptions
- [ ] Branch names never appear in annotated tag content
- [ ] Commit hash properly linked to build number via lightweight tag

---

## ⚠️ CRITICAL CONSIDERATIONS

### Build Number Management

- **Atomic Operations**: Build counter updates must be atomic to prevent conflicts
- **Conflict Resolution**: Handle simultaneous PR merges gracefully
- **Backup Strategy**: Maintain build counter history for audit purposes

### PR Description Requirements

- **Mandatory Format**: PR descriptions must contain acceptance criteria paraphrase
- **Validation**: CI should fail if PR description is empty/incomplete
- **Template Enforcement**: Use PR templates to ensure consistency

### Historical Backlog Handling

- **Initial State**: First minor release will contain extensive build list (`[261]` to `[287]`)
- **Performance**: Tag creation must handle large build aggregations efficiently
- **Documentation**: Provide clear migration path for existing repositories

### Security Considerations

- **Tag Signing**: Implement GPG signing for production releases
- **Permission Controls**: Restrict tag creation to authorized maintainers
- **Audit Trail**: Log all version operations for compliance

---

## 🚀 DEPLOYMENT READINESS

This workflow enables:
✅ **Traceable Releases**: Every build number maps to specific functionality  
✅ **Automated Compliance**: PR content automatically included in release notes  
✅ **Sprint Alignment**: Minor releases correspond to completed sprint cycles  
✅ **Scalable Growth**: Handles both rapid patch releases and structured minor releases

The system accommodates the initial backlog while establishing sustainable release practices for future development cycles.
