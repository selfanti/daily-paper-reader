from pathlib import Path


SYNC_WORKFLOW = Path(".github/workflows/sync.yml")


def test_sync_workflow_runs_daily_and_manually():
    text = SYNC_WORKFLOW.read_text(encoding="utf-8")

    assert "workflow_dispatch:" in text
    assert "schedule:" in text
    assert 'cron: "0 0 * * *"' in text
    assert "github.event_name == 'schedule'" not in text
    assert "shuf -i" not in text
    assert "timeout-minutes: 30" in text


def test_sync_workflow_uses_repository_deploy_key():
    text = SYNC_WORKFLOW.read_text(encoding="utf-8")

    assert "ssh-key: ${{ secrets.UPSTREAM_SYNC_DEPLOY_KEY }}" in text
    assert "git push origin HEAD:main" in text
    assert "aormsby/Fork-Sync-With-Upstream-action" not in text
    assert "target_repo_token" not in text


def test_sync_workflow_does_not_request_pages_rebuild():
    text = SYNC_WORKFLOW.read_text(encoding="utf-8")

    assert "pages: write" not in text
    assert "Request GitHub Pages rebuild" not in text
    assert "/pages/builds" not in text
