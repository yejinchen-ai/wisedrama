# WiseDrama vs. Flova product and workflow analysis

Research date: 2026-08-05

## Product workflow

Flova is organized around a durable creative project rather than a one-shot generation request:

1. Start from a prompt, existing script/shot list, reference media, an individual media task,
   a reusable Skill, or a published example.
2. The Agent creates a Final Video Spec containing duration, aspect ratio, language, style,
   and production constraints.
3. It plans the script, key elements, shots, and audio layers as an editable storyboard.
4. Images, videos, and audio are generated into versioned assets, then bound to storyboard
   cards with semantic roles such as reference image, keyframe, or final video.
5. Selected media is assembled into an editable timeline.
6. Users can edit directly while the Agent works, regenerate a selected scope, restore a
   previous state, branch a project, and export video or project files.

The defining interaction is “direct from the right, view and edit on the left”: Agent chat is
the control plane; storyboard, media, documents, preview, and timeline are the shared project
state.

## Capability gap and implementation status

| Capability | Previous WiseDrama | Current implementation | Remaining work |
| --- | --- | --- | --- |
| Persistent projects | Job JSON only | Project JSON with ownership and active job | Database migration, archival |
| Final Video Spec | Request parameters | Editable spec in Studio | Templates and validation per model |
| Script/storyboard | Generated then hidden | Persisted and editable shot cards | Reorder/add/delete operations |
| Key elements | Character profiles | Visible project elements | Scene, prop, voice identity assets |
| Media space | Final URLs on shots | Project media index with semantic purpose | Version groups, likes, uploads, drag binding |
| Timeline | Automatic stitching | Persistent timeline and preview | Trim, reorder, multi-track audio editor |
| Agent visibility | Coarse progress bar | Event stream in right-side Agent panel | Streaming reasoning/tool events |
| Local regeneration | Whole project only | Manual shot prompt editing | Per-shot generation endpoint and version selection |
| Branching | None | Clone project from current state | Snapshot-at-message and merge/conflicts |
| Export | MP4 only | Final MP4 | Premiere/OTIO/project bundle |
| Parallel work | Sequential render loop | Durable state supports independent edits | Worker queue and optimistic conflict control |
| Skills | None | — | Versioned workflow recipes and marketplace |

## WiseDrama target architecture

```text
Project / Final Video Spec
          |
          v
Planner Agent (Kimi K3)
          |
   +------+------+----------------+
   |             |                |
Script Agent  Storyboard Agent  Asset/Art Agent
   |             |                |
   +-------> Shot Graph <---------+
                  |
          Generation Dispatcher
     (H3 / Seedance / Kling / Veo / ...)
                  |
          Versioned Media Assets
                  |
          Timeline Assembly/Edit
                  |
             Export Pipeline
```

The Shot Graph should be the canonical intermediate representation. Each shot references
characters, scenes, props, source assets, generated versions, dialogue, duration, camera
language, and continuity edges to the previous and next shots. Generation jobs are derived
from this graph; they must not replace it.

## Delivery phases

### Phase 1 — project workspace (implemented in this change)

- Persistent project and Final Video Spec.
- Three-column Studio: storyboard/media/docs, preview/timeline, Agent chat.
- Pipeline-to-project state synchronization.
- Editable shot prompts and project specifications.
- Project branching and authenticated project/job reads.

### Phase 2 — controllable generation

- Generate, cancel, or regenerate a single shot.
- Media asset/version tables and upload API.
- Bind an asset to multiple shots with a purpose.
- Generate only script/storyboard and wait for approval.
- Background worker queue instead of a single sequential FastAPI task.

### Phase 3 — editing and memory

- Multi-track timeline with trim/reorder/volume and audio layers.
- Immutable snapshots, restore-to-message, and branch from snapshot.
- Optimistic revisions and conflict resolution for parallel Agent/manual edits.
- Project memory retrieval and versioned Skills.

### Phase 4 — production parity

- Voice, music, sound effects, lip sync, captioning, and localization.
- Reference-video analysis, keyframe extraction, and structural recreation.
- OTIO/Premiere-style export, complete project bundle, collaboration and sharing.

## Sources

- [What Is Flova](https://www.flova.ai/docs/en)
- [Flova Quick Start](https://www.flova.ai/docs/en/introduction/quick-start)
- [Flova Agent workflow](https://www.flova.ai/docs/en/features/agent)
- [Flova Media Space and project editing](https://www.flova.ai/docs/en/features/project-content-editing)
