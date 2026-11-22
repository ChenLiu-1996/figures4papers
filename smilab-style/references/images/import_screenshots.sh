#!/usr/bin/env bash
# Copy the 33 reference screenshots (macOS screencapture temp files) into this folder
# with descriptive names. Run from anywhere:
#   bash smilab-style/references/images/import_screenshots.sh
set -u
DEST="$(cd "$(dirname "$0")" && pwd)"
T=/var/folders/9j/g3j9kcwd43q_3qvzr6mpt_wr0000gn/T/TemporaryItems

copy() { # $1 = temp dir id, $2 = time stamp, $3 = destination name
  local src="$T/NSIRD_screencaptureui_$1/Screenshot 2026-11-23 at $2.png"
  if cp "$src" "$DEST/$3.png" 2>/dev/null; then echo "ok   $3"; else echo "MISS $3  ($src)"; fi
}

copy aCrRHG 2.58.48 01_fmri-decoding_overview
copy q3dz0Y 2.58.56 02_bis5_architecture
copy eWO18B 2.59.09 03_brain-roi_comparison
copy 8cP4SV 2.59.31 04_flow-ssm_architecture
copy v6L35t 2.59.56 05_abmamba_scatter-bleu-throughput
copy lH5IGs 3.00.08 06_abmamba_overview
copy 5u7H4X 3.00.17 07_abmamba_ahbs-scan
copy whFM38 3.00.41 08_elsa_teaser
copy iUMlrR 3.00.49 09_elsa_pipeline
copy MSTQ32 3.01.00 10_elsa_lineplot-kendall
copy K1jnwB 3.01.06 11_elsa_hist-sankey
copy HLKcgT 3.01.23 12_candle_method
copy HvyFe0 3.01.36 13_candle_simulator
copy OhvsvY 3.01.45 14_candle_synthetic-results
copy YSRsxu 3.01.54 15_candle_spes-results
copy s29NrC 3.02.02 16_candle_epilepsy-results
copy WDnvfb 3.02.18 17_candle_ablation-hbar
copy VwPzGc 3.02.50 18_flowasflow_teaser
copy 8DzpCZ 3.03.03 19_flowasflow_architecture
copy W4jlkG 3.04.01 20_motion-llm_teaser
copy wLuNTi 3.04.11 21_motion-llm_architecture
copy Y5FsyL 3.05.20 22_rigel_teaser
copy 4I54pH 3.05.30 23_rigel_method
copy MuDd2V 3.06.02 24_phi-score_pipeline
copy PsML0c 3.06.22 25_nail_teaser
copy mugZpG 3.06.34 26_nail_architecture
copy wKCtLR 3.06.52 27_nail_cij-examples
copy 7XirLC 3.08.40 28_discode_teaser
copy XNw0V3 3.08.50 29_discode_method
copy 9Rlm9Y 3.08.58 30_discode_bargrid
copy iO1ZSl 3.09.18 31_caption-metric_architecture
copy Di09TY 3.10.30 32_hallucination_three-step
copy jeKv45 3.10.52 33_hallucination_scatter-latency
