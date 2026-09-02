# Data and model sources

Access dates below describe the frozen study inputs. Raw molecular tables and third-party source trees are not bundled in this repository.

## B-XAIC

- Source: `https://huggingface.co/datasets/mproszewska/B-XAIC`
- Frozen revision: `c963b9ee34862b4115dccf7941ba55c9bee16ad0`
- License reported by the dataset card: CC BY-SA 4.0
- Accessed for this study: 2026-08-04
- Expected files and SHA-256:
  - `data.csv`: `14853568ECE75E5C5666C7190E6402CE8D24B3DD3DB171460E668C82C06344FC`
  - `explanations.sdf`: `83C86A6366AFF1DB12A3E439CEAB9A4F275508FAF1BEB5E1B8ADB261465E70AA`
- Role: public molecular-property tasks and atom-rationale annotations used in the benchmark and calibration audits.
- Redistribution: omitted from this package; retrieve the exact revision and comply with CC BY-SA 4.0.

## Graph Attribution

- Source: `https://github.com/google-research/graph-attribution`
- Frozen commit: `03e7495379df26a21395b25c6a14d92dc27fc3b0`
- Repository license: Apache License 2.0
- Accessed for this study: 2026-08-04
- Role: the benzene and logic7/logic8/logic10 benchmark families and their rationale masks.
- Redistribution: the upstream source/data copy is omitted. Retrieve the frozen commit and follow its LICENSE/NOTICE plus the upstream terms for any underlying molecule collection.

## Polaris HCLint

- Benchmark artifact: `polaris/adme-fang-hclint-1`
- Dataset artifact: `polaris/adme-fang-1`
- Source page: `https://polarishub.io/benchmarks/polaris/adme-fang-hclint-1`
- Dataset source cited by Polaris: `https://doi.org/10.1021/acs.jcim.3c00160`
- Dataset license reported by Polaris 0.13.0: CC BY 4.0
- Accessed and frozen: 2026-09-01
- Benchmark MD5: `42af137e8e493bd313071c720f26205c`
- Official split: 2,229 train and 575 hidden-test molecules; target `LOG_HLM_CLint`.
- Materialized CSV SHA-256:
  - train: `8f2936a7ccf2d80110dff05bc9bf7ea115b076684e47e3c37d47fa09c4998f44`
  - test: `60d55038d3d95ccb34a7be441ae1fbed7cb588e1d93c5843461f43aad98a1052`
- Retrieval: install `polaris-lib==0.13.0` and run `python scripts/polaris/polaris_hclint.py prepare --out-dir data`.
- Evaluation boundary: the official Polaris evaluator was used; hidden test targets were not directly accessed. HCLint supplies no atom-level rationale label, so this dataset tests predictivity and explainer compatibility, not rationale coverage.

## CheMeleon foundation checkpoint

- Record: `https://doi.org/10.5281/zenodo.15460715` (version v2)
- File: `chemeleon_mp.pt`, 34,859,448 bytes
- SHA-256: `c376624d3407204e780a0ed13a9ac097cc9bb1c13ef89cdbc633c1715c183651`
- Direct file used: `https://zenodo.org/records/15460715/files/chemeleon_mp.pt`
- Role: Chemprop 2.2.4 foundation initialization for three fixed fine-tuning seeds (42, 123, 2026).
- Redistribution: not bundled. The Zenodo record displayed no license value at package preparation time; users must confirm the record and linked repository terms before reuse.

## Related source audits

The study inspected the following public repositories while selecting the ADME benchmark route; their source trees are not dependencies bundled here:

- Computational-ADME, commit `b00df003de117ce9e5b381afd886095c5f2af2d5`, MIT: `https://github.com/molecularinformatics/Computational-ADME`
- OpenADMET models, commit `55dd001549885f8d8095af14733d61f36fc046c0`, Apache-2.0: `https://github.com/OpenADMET/openadmet-models`
- Optimus Prime, commit `7e095630c33c92b86914ccbcb31459ce3827309f`, Apache-2.0: `https://github.com/OpenADMET/optimus-prime`

These references document route selection and provenance; their licenses do not change the license of this repository and do not authorize redistribution of unrelated upstream assets.
