# Meson Structure — Post-analysis

Analysis tools for pion and kaon structure-function studies using the Sullivan process at the EIC, based on ePIC simulation campaigns.

## Analysis channels

| Directory | Description |
|---|---|
| [`eg-x/`](pion-neutron/) | Event generator post analysis |
| [`pion-neutron/`](pion-neutron/) | Neutron reconstruction and pion structure-function projections |
| [`kaon-lambda/`](kaon-lambda/) | $\Lambda$ reconstruction and kaon structure-function projections |
| `common/` | Shared utilities |

## Getting started

Navigate to the relevant channel directory:

```bash
cd pion-neutron/
# or
cd kaon-lambda/
```

Run the reconstruction or projection analysis:

```bash
python run_reconstruction.py --help
python run_projection.py --help
```

Both scripts accept input ROOT files and output directories through command-line arguments.

See the channel-specific README for complete examples and configuration details:

- [Pion–neutron analysis](pion-neutron/README.md)
- [Kaon–Lambda analysis](kaon-lambda/README.md)

## Outputs

Results are organized under each channel's `outputs/` directory. Figures are saved as PNG files, alongside the CSV tables required for uncertainty projections.

Analysis settings, selection cuts, model parameters, and detector-specific configurations are defined in each channel's `config.py`.