# WiseDrama 一致性保持技术调研与实施方案

## 阶段一：Prompt 锁死 + 参考图垫图 (Image-to-Video 接力)
**状态**：进行中 (2026-03-11)
**目标**：以最低成本、最快速度提升多镜头的角色与场景一致性。

### 核心机制

1.  **全局特征锁死 (Global Prompt Locking)**
    *   **剧本解析阶段**：提取主要角色（如主角 A）的外貌特征、服装描述，以及核心场景的细节。
    *   **字典维护**：将这些特征固化为标准的 Prompt 字符串（例如 `[CHARACTER_A_PROMPT]` = "A 25-year-old Asian man, short black hair, wearing a white t-shirt and blue jeans, cinematic lighting"）。
    *   **Prompt 注入**：在后续生成每个分镜的视频时，强制将该标准 Prompt 拼接到分镜动作描述的前面。

2.  **角色/场景参考图生成 (Text-to-Image Reference)**
    *   在视频生成前，先调用高质量的 T2I 模型（如 Flux, Midjourney, DALL-E 3）生成一张角色的**标准定妆照**或**场景概念图**。
    *   这张图将作为整个短剧的视觉锚点。

3.  **图生视频 (Image-to-Video 垫图)**
    *   **API 切换**：将目前的纯文本生视频（Text-to-Video）流程，升级为**图文生视频**（Image+Text-to-Video）。
    *   将第 2 步生成的参考图，作为首帧或风格参考图输入给 Veo 3 / Hailuo AI 的 I2V 接口。
    *   确保动作 Prompt (例如 "walking forward, looking at the camera") 结合固定的参考图，从而生成连贯且外貌一致的视频片段。

### 实施路径 (Action Items)

1.  **数据结构更新**：在 `Job` 或 `Story` 模型中增加 `character_profiles` 和 `reference_images` 字段。
2.  **Agent 升级**：新增一个 `ArtDirectorAgent`（美术指导 Agent），专职负责生成定妆照和提取锁死 Prompt。
3.  **生成引擎适配**：修改视频生成服务（如 `hailuo_client.py` 或 `veo_client.py`），使其支持接收 `image_url` 作为输入参数，调用图生视频接口。
