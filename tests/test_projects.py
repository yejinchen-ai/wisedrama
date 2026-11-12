import asyncio

from api import projects


def test_project_workspace_create_edit_and_branch(tmp_path, monkeypatch):
    monkeypatch.setattr(projects, "PROJECTS_DIR", tmp_path)

    created = asyncio.run(
        projects.create_project(
            projects.ProjectCreate(
                title="Neon Story",
                prompt="A detective follows a signal.",
                model="hailuo-h3",
                resolution="2k",
            ),
            username="alice",
        )
    )
    created["shots"] = [
        {
            "shot_number": 1,
            "scene_description": "The detective enters the alley.",
            "video_prompt": "Wide shot",
        }
    ]
    projects.save_project(created)

    renamed = asyncio.run(
        projects.patch_project(
            created["id"], projects.ProjectUpdate(title="  New title  "), username="alice"
        )
    )
    assert renamed["title"] == "New title"

    edited = asyncio.run(
        projects.patch_shot(
            created["id"],
            1,
            projects.ShotUpdate(video_prompt="Slow tracking shot"),
            username="alice",
        )
    )
    assert edited["shots"][0]["video_prompt"] == "Slow tracking shot"
    assert edited["shots"][0]["prompt"] == "Slow tracking shot"
    assert edited["shots"][0]["edited_by_user"] is True

    added = asyncio.run(
        projects.create_shot(
            created["id"],
            projects.ShotCreate(after_shot_number=1, video_prompt="Close-up", duration=4),
            username="alice",
        )
    )
    assert [shot["shot_number"] for shot in added["shots"]] == [1, 2]
    assert added["shots"][1]["duration"] == 4

    reordered = asyncio.run(
        projects.reorder_shots(
            created["id"], projects.ShotReorder(shot_numbers=[2, 1]), username="alice"
        )
    )
    assert reordered["shots"][0]["video_prompt"] == "Close-up"
    assert [shot["shot_number"] for shot in reordered["shots"]] == [1, 2]

    deleted = asyncio.run(projects.delete_shot(created["id"], 1, username="alice"))
    assert len(deleted["shots"]) == 1
    assert deleted["shots"][0]["shot_number"] == 1

    branch = asyncio.run(projects.branch_project(created["id"], username="alice"))
    assert branch["id"] != created["id"]
    assert branch["parent_project_id"] == created["id"]
    assert branch["status"] == "draft"
