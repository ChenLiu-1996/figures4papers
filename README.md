<div align="center">

<h1><code>Figures for Papers</code></h1>

[![oosmetrics](https://api.oosmetrics.com/api/v1/badge/achievement/9cb2283a-461d-44fd-bd2d-83d82f53fd17.svg)](https://oosmetrics.com/repo/ChenLiu-1996/figures4papers)
<br>[![LinkedIn](https://img.shields.io/badge/LinkedIn-Chen-blue)](https://www.linkedin.com/in/chenliu1996/)
[![Twitter Follow](https://img.shields.io/twitter/follow/Chen.svg?style=social)](https://x.com/ChenLiu_1996)
[![Google Scholar](https://img.shields.io/badge/Google_Scholar-Chen-4a86cf?logo=google-scholar&logoColor=white)](https://scholar.google.com/citations?user=3rDjnykAAAAJ&sortby=pubdate)

</div>

I am [Chen Liu](https://chenliu-1996.github.io/) (刘晨), a Computer Science PhD Candidate at Yale University.

This is a centralized repository of my own **Python scripts for high-quality figures**.

These figures are published at top venues, including ***Nature Machine Intelligence***, ***ICML***, ***NeurIPS***, ***ECCV***, etc. &#127881; 

Please feel free to cite any of these papers if you find them relevant or helpful. &#127891; 
<br>在**符合学术规范的前提**下，欢迎大家狠狠引用。 &#127891; 

<br>

### Bar plots for quantitative comparison
<img src="figure_ImmunoStruct/figures/bars_comparison_IEDB.png" width="800">

### Bar plots for composition breakdown
<img src="figure_Brainteaser/figures/brute_force.png" width="800">


### 3D spheres
<img src="figure_Dispersion/figures/illustration.png" width="800">

<div align="center">

<h3 align="left">Radar plots &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Line plots</h3>

<p align="left">
<img align="left" src="figure_VIGIL/figures/comparison_radar.png" width="400" alt="Radar comparison">
<img align="left" src="figure_VIGIL/figures/comparison_posttraining.png" width="350" alt="Post-training comparison">
<br clear="all">
</p>

</div>

### Concept plots
<img src="figure_VIGIL/figures/concept.png" width="800">

### Trend plots
<img src="figure_ophthal_review/figures/trend_by_month.png" width="800">

### Miscellaneous: figures not made end-to-end in Python
These figures were made partially in Python. I included them to acknowledge the time and efforts I spent on them.

<img src="assets/ImmunoStruct_schematic.png" width="400"><img src="assets/ImmunoStruct_contrastive.png" width="400">
<br><img src="assets/ImmunoStruct_results_IEDB.png" width="400"><img src="assets/ImmunoStruct_results_CEDAR.png" width="400">
<br><img src="assets/VIGIL_teaser.png" width="400"><img src="assets/RNAGenScape_schematic.png" width="400">
<br><img src="assets/RNAGenScape_teaser.png" width="400"><img src="assets/Dispersion_motivation.png" width="400">
<br><img src="assets/Dispersion_observation.png" width="400"><img src="assets/Dispersion_observation_distillation.png" width="400">

<br>

## LLM skill integration
I want to show appreciation to my friend [Shan Chen](https://shanchen.dev/) who suggested doing this.

The **scientific figure making** skill lives in `scientific-figure-making/`. Demo figures live in `assets/`. Project-specific scripts and outputs live in `figure_*/`.

### Skill folder hierarchy

```
scientific-figure-making/
├── SKILL.md                              # Quick reference: metadata, when to use, patterns, links
└── references/
    ├── api.md                            # API/conventions to implement (palette, helpers, export)
    ├── common-patterns.md                # Reusable figure patterns
    ├── demos.md                          # Real-world figure_* projects (with URLs)
    ├── design-theory.md                  # Style rationale and design principles
    └── tutorials.md                      # Step-by-step guides
```

### Using this skill in an AI coding agent

<details>
<summary><strong>No installation (path-based)</strong></summary>

You can use this skill **without installing anything**: open this repo in your AI coding agent (e.g. [Cursor](https://cursor.com), Claude Code, etc.) and reference the skill by path in your prompts. The agent reads `scientific-figure-making/SKILL.md` and the `references/` files from the repo—no symlinks or plugins required.

**Simple AI workflow**

1. Open this repository in your AI coding agent (e.g. Cursor).
2. Ask the AI to create or update a plotting script in your target folder (for example `figure_PROJECT_NAME/`).
3. In your prompt, explicitly ask it to follow `scientific-figure-making/SKILL.md` and `scientific-figure-making/references/design-theory.md`.
4. Run the generated script and check the exported figure.

**Prompt template (copy/paste)**

```text
Create a publication-quality figure script at <target_path>.
Use the Scientific Figure Making skill conventions from:
- scientific-figure-making/SKILL.md
- scientific-figure-making/references/design-theory.md
- scientific-figure-making/references/api.md (palette, helpers, export)

Implement or adapt the patterns (apply_publication_style, make_* helpers, finalize_figure). See figure_* folders for reference scripts.
Input data: <describe your data or paste arrays>.
Output files: <name>.png and <name>.pdf.
Keep the style consistent with this repository.
```

</details>

<details>
<summary><strong>Install as a skill (symlink)</strong></summary>

From the repository root, run:

| Agent       | Commands |
|------------|----------|
| **Cursor** | `mkdir -p ~/.cursor/skills` then `ln -s "$(pwd)/scientific-figure-making" ~/.cursor/skills/scientific-figure-making` |
| **Claude Code** | `mkdir -p ~/.claude/skills` then `ln -s "$(pwd)/scientific-figure-making" ~/.claude/skills/scientific-figure-making` |
| **Codex**  | `mkdir -p ~/.codex/skills` then `ln -s "$(pwd)/scientific-figure-making" ~/.codex/skills/scientific-figure-making` |

Restart the agent (or refresh its skill list) after linking. You can then invoke or cite the skill by name in addition to using path-based references when the repo is open.

</details>

## Related Papers
<details>
<summary>ImmunoStruct (Nature Machine Intelligence 2026)</summary>

[![nature](https://img.shields.io/badge/nature-machine_intelligence-gold)](https://www.nature.com/articles/s42256-025-01163-y)
[![PDF](https://img.shields.io/badge/PDF-DADBDD)](https://www.nature.com/articles/s42256-025-01163-y.pdf)
[![Huggingface](https://img.shields.io/badge/Dataset-ImmunoStruct-orange)](https://huggingface.co/datasets/ChenLiu1996/ImmunoStruct)
[![Huggingface](https://img.shields.io/badge/Model-ImmunoStruct-orange)](https://huggingface.co/ChenLiu1996/ImmunoStruct)
[![GitHub Stars](https://img.shields.io/github/stars/KrishnaswamyLab/ImmunoStruct.svg?style=social\&label=Stars)](https://github.com/KrishnaswamyLab/ImmunoStruct)
```bibtex
@article{givechian2026immunostruct,
  title={ImmunoStruct enables multimodal deep learning for immunogenicity prediction},
  author={Givechian, Kevin Bijan and Rocha, Jo{\~a}o Felipe and Liu, Chen and Yang, Edward and Tyagi, Sidharth and Greene, Kerrie and Ying, Rex and Caron, Etienne and Iwasaki, Akiko and Krishnaswamy, Smita},
  journal={Nature Machine Intelligence},
  volume={8},
  pages={70--83},
  year={2026},
  publisher={Nature Publishing Group UK London}
}
```

</details>
<details>
<summary>LM-Dispersion (ICML 2026)</summary>

[![OpenReview](https://img.shields.io/badge/OpenReview-eeeeee)](https://openreview.net/forum?id=pd6A7jB5D6)
[![ICML 2026](https://img.shields.io/badge/ICML_2026-purple)](https://icml.cc/virtual/2026/poster/61492)
[![Project Page](https://img.shields.io/badge/Project_Page-B9DEF1)](https://chenliu-1996.github.io/projects/LM-Dispersion/)
[![arXiv](https://img.shields.io/badge/arXiv-Dispersion-firebrick)](https://arxiv.org/abs/2602.00217)
[![PDF](https://img.shields.io/badge/PDF-DADBDD)](https://arxiv.org/pdf/2602.00217)
[![GitHub Stars](https://img.shields.io/github/stars/ChenLiu-1996/LM-Dispersion.svg?style=social\&label=Stars)](https://github.com/ChenLiu-1996/LM-Dispersion)
```bibtex
@inproceedings{liu2026dispersion,
  title={Dispersion loss counteracts embedding condensation and improves generalization in small language models},
  author={Liu, Chen and Sun, Xingzhi and Xiao, Xi and Van Tassel, Alexandre and Xu, Ke and Reimann, Kristof and Liao, Danqi and Gerstein, Mark and Wang, Tianyang and Wang, Xiao and Krishnaswamy, Smita},
  booktitle={International Conference on Machine Learning},
  year={2026},
  organization={PMLR}
}
```

</details>
<details>
<summary>VIGIL (ECCV 2026)</summary>

[![OpenReview](https://img.shields.io/badge/OpenReview-eeeeee)](https://openreview.net/forum?id=p9Zb9F0V71)
[![Project Page](https://img.shields.io/badge/Project_Page-B9DEF1)](https://xixiaouab.github.io/VIGIL/)
[![arXiv](https://img.shields.io/badge/arXiv-VIGIL-firebrick)](https://arxiv.org/abs/2606.26387)
[![PDF](https://img.shields.io/badge/PDF-DADBDD)](https://arxiv.org/pdf/2606.26387)
```bibtex
@inproceedings{xiao2026vigil,
  title={Staying VIGILant: Mitigating Visual Laziness via Counterfactual Visual Alignment in MLLMs},
  author={Xiao, Xi and Liu, Chen and Liao, Chih-Ting and Zhang, Yunbei and Lan, Qizhen and Wei, Yuxiang and Zhao, Lin and Wang, Janet and Gu, Jianyang and Ye, Muchao and Wang, Tianyang and Xu, Hao},
  booktitle={European Conference on Computer Vision},
  year={2026},
  organization={Springer}
}
```

</details>
<details>
<summary>RNAGenScape</summary>

[![arXiv](https://img.shields.io/badge/arXiv-RNAGenScape-firebrick)](https://arxiv.org/abs/2510.24736)
[![PDF](https://img.shields.io/badge/PDF-DADBDD)](https://arxiv.org/pdf/2510.24736)
```bibtex
@article{liao2025rnagenscape,
  title={RNAGenScape: Property-Guided, Optimized Generation of mRNA Sequences with Manifold Langevin Dynamics},
  author={Liao, Danqi and Liu, Chen and Sun, Xingzhi and Tang, Di{\'e} and Wang, Haochen and Youlten, Scott and Gopinath, Srikar Krishna and Lee, Haejeong and Strayer, Ethan C and Giraldez, Antonio J and Krishnaswamy, Smita},
  journal={arXiv preprint arXiv:2510.24736},
  year={2025}
}
```

</details>
<details>
<summary>Brainteaser (NeurIPS 2025)</summary>

[![OpenReview](https://img.shields.io/badge/OpenReview-eeeeee)](https://openreview.net/forum?id=3oQDkmW72a)
[![NeurIPS 2025](https://img.shields.io/badge/NeurIPS_2025-purple)](https://neurips.cc/virtual/2025/loc/san-diego/poster/120001)
[![HuggingFace Dataset](https://img.shields.io/badge/Dataset-Brainteaser-orange)](https://huggingface.co/datasets/ChenLiu1996/Brainteaser)
[![arXiv](https://img.shields.io/badge/arXiv-Brainteaser-firebrick)](https://arxiv.org/abs/2505.10844)
[![PDF](https://img.shields.io/badge/PDF-DADBDD)](https://arxiv.org/pdf/2505.10844)
[![GitHub Stars](https://img.shields.io/github/stars/stephenxia1/brainteasers.svg?style=social\&label=Stars)](https://github.com/stephenxia1/brainteasers)
```bibtex
@inproceedings{han2025creativity,
  title={Creativity or brute force? using brainteasers as a window into the problem-solving abilities of large language models},
  author={Han, Sophia and Dai, Howard and Xia, Stephen and Zhang, Grant and Liu, Chen and Chen, Lichang and Nguyen, Hoang H and Mei, Hongyuan and Mao, Jiayuan and McCoy, R Thomas},
  journal={Advances in Neural Information Processing Systems},
  volume={38},
  pages={146950--147004},
  year={2025}
}
```

</details>
