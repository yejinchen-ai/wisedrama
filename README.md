# WiseDrama (wisedrama.com) 🎬

WiseDrama is an advanced **Agentic AI Video Generation Pipeline** designed to convert human ideas into high-quality, multi-shot short dramas (5 to 30 minutes in length). 

Instead of generating isolated 5-second video clips like traditional wrappers, WiseDrama acts as a fully autonomous film studio—writing the script, planning camera angles, maintaining character consistency, and prompting state-of-the-art video models (like Hailuo, Kling, and VideoInu APIs) to produce cohesive short films.

## 🚀 Features

- **Brain-to-Video**: Enter a single-line idea, and the pipeline outputs a complete, shot-by-shot storyboard.
- **Agentic Workflow**:
  - 🧠 **Screenwriter Agent (Powered by Kimi K3)**: Expands ideas into a cohesive narrative, forcing strict physical character descriptions across shots to maintain character consistency.
  - 🎬 **Storyboard Agent (Powered by Kimi K3)**: Converts the script into production-ready, continuity-aware prompts tailored for AI video models.
  - 🎬 **Director Agents**: Dispatch optimized prompts to Seedance 2.0, Kling 3.0, MiniMax H3/Hailuo 2.3, Google Veo 3.1, Alibaba HappyHorse 1.1, PixVerse, and other video APIs, then poll for MP4 generation.
- **Self-Healing Architecture**: Built-in `loguru` crash reporter that allows AI assistants (like OpenClaw) to auto-debug and auto-patch code when exceptions occur in production.

## 🛠 Tech Stack

- **Language:** Python 3.10+
- **Creative Agent LLM:** Kimi K3 through its OpenAI-compatible API (`langchain-openai`)
- **Orchestration:** LangChain, Pydantic
- **Video Models:** Seedance 2.0, Kling 3.0, MiniMax H3 (2K with native audio), MiniMax Hailuo 2.3, Google Veo 3.1, Alibaba HappyHorse 1.1, PixVerse V5.6, Runway, and Sora
- **Testing & Tooling:** Pytest, Loguru

## ⚙️ Setup & Installation

1. Clone the repository:
   ```bash
   git clone git@github.com-wisevision:wisevisioninc/wisedrama.git
   cd wisedrama
   ```

2. Set up the virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure Environment Variables:
   Create a `.env` file in the root directory and add your API keys:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   KIMI_API_KEY=your_kimi_code_api_key_here
   KIMI_BASE_URL=https://api.kimi.com/coding/v1
   KIMI_MODEL=k3
   VEO3_API_KEY=your_google_veo_key_here
   HAILUO_API_KEY=your_hailuo_api_key_here
   SEEDANCE_API_KEY=your_volcengine_ark_key_here
   KLING_ACCESS_KEY=your_kling_access_key_here
   KLING_SECRET_KEY=your_kling_secret_key_here
   HAPPYHORSE_API_KEY=your_alibaba_model_studio_key_here
   ```

   Optional model and endpoint overrides:

   ```env
   VEO_MODEL=veo-3.1-generate-preview
   HAILUO_MODEL=MiniMax-Hailuo-2.3
   HAILUO_H3_MODEL=MiniMax-H3
   SEEDANCE_MODEL=doubao-seedance-2-0-260128
   KLING_MODEL=kling-v3
   HAPPYHORSE_T2V_MODEL=happyhorse-1.1-t2v
   HAPPYHORSE_I2V_MODEL=happyhorse-1.1-i2v
   HAPPYHORSE_BASE_URL=https://dashscope-intl.aliyuncs.com
   ```

## 🎯 Usage

To run the MVP pipeline (which currently runs the Screenwriter and Prompter agents):

```bash
python src/main.py
```

Check the `logs/` directory for detailed execution logs and crash reports (if any).

## 🛡️ Auto-Debug Protocol

This project is monitored by the OpenClaw AI system. If the pipeline crashes, a `crash_report.json` is generated in `logs/`. The AI assistant will automatically read the traceback, patch the code in `src/`, run `pytest`, and push the fix directly to GitHub.

---
*Created by WiseVision Inc. for wisedrama.com*
