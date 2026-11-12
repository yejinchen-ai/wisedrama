# MiniMax H3 integration notes

Research date: 2026-08-05

## Confirmed API capabilities

- Official model ID: `MiniMax-H3`.
- Create endpoint: `POST https://api.minimax.io/v2/video_generation`.
- Query endpoint: `GET https://api.minimax.io/v2/query/video_generation/{task_id}`.
- Inputs use a multimodal `content` array containing text, image, video, or audio items.
- Text-to-video, first/last-frame image-to-video, and multimodal reference-to-video are supported.
- Output resolution is `768P` or `2K`; duration is an integer from 4 through 15 seconds.
- H3 output includes native audio. A succeeded task exposes the temporary download URL at
  `task.content.url`.
- Text-to-video requires a concrete aspect ratio. Image-to-video derives its ratio from the
  input image and uses `adaptive`.

## WiseDrama mapping

WiseDrama exposes the model as `hailuo-h3` (with `h3` as a backend alias). Existing
`hailuo-2.3` behavior remains unchanged.

| WiseDrama setting | H3 API value |
| --- | --- |
| `720p` | `768P` |
| `1080p`, `2k`, `4k` | `2K` |
| No reference image | text-to-video, ratio `16:9` |
| Reference image | first-frame image-to-video, ratio `adaptive` |

The pipeline currently requests six seconds per shot, which is within H3's supported
4–15 second range.

## Official sources

- [MiniMax documentation index](https://platform.minimax.io/docs/llms.txt)
- [Create Video Generation Task V2](https://platform.minimax.io/docs/api-reference/video-generation-v2-create)
- [Query Video Generation Task V2](https://platform.minimax.io/docs/api-reference/video-generation-v2-query)
- [Video Generation V2 OpenAPI specification](https://platform.minimax.io/docs/api-reference/video/generation/api/v2-video-generation.json)
- [H3 feature highlights](https://platform.minimax.io/docs/guides/video-prompt)
