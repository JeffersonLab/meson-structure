"""Shared presentation and uncertainty plotting for pion and kaon models."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colormaps
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from .model_dse import evaluate as dse_evaluate
from .model_jam import evaluate as jam_evaluate, reweight_f2, load_replicas, weighted_statistics

STYLE = {'font.family': 'serif', 'mathtext.fontset': 'stix', 'font.size': 15,
         'axes.labelsize': 20, 'axes.linewidth': 1.4,
         'xtick.direction': 'in', 'ytick.direction': 'in',
         'xtick.top': True, 'ytick.right': True, 'xtick.major.size': 7,
         'ytick.major.size': 7, 'xtick.minor.size': 4, 'ytick.minor.size': 4,
         'xtick.major.width': 1.2, 'ytick.major.width': 1.2,
         'legend.fontsize': 11}
YLIMS_DSE = {'pion': {'valence': (.0, .75), 'glue': (.0, 3.)},
             'kaon': {'valence': (.0, .50), 'glue': (.0, 1.90)}}
YLIMS_JAM = {'pion': {'valence': (.0, .34), 'glue': (.0, 5.)},
             'kaon': {'valence': (.0, .5), 'glue': (.0, 5.)}}

@dataclass(frozen=True)
class Scenario:
    """Model figure scenario: label, flux fraction, and luminosities (fb^-1)."""
    name: str
    mode: str
    flux: float
    luminosities: tuple[float, ...]

SCENARIOS = (
    Scenario('early', 'experimental', 0., (1., 2.5, 10.)),
    Scenario('design', 'experimental', 0., (50., 100.)),
)


def read_uq(csv_dir, channel, beam, luminosity):
    """Load x and fractional statistical error from one Q2-integrated UQ CSV.

    Args:
        csv_dir, channel, beam, luminosity: Inputs and configuration for this operation.
    Returns:
        Computed data or saved file paths, as described above.
    """
    tag = f'{channel}_stat_uq_{beam}_L{luminosity:g}fb'.replace('L0.', 'L0p')
    path = Path(csv_dir) / f'{tag}.csv'
    if not path.is_file():
        return None
    data = np.genfromtxt(path, delimiter=',', names=True, ndmin=1)
    x, stat = np.asarray(data['x'], float), np.asarray(data['stat_rel'], float)
    mask = np.isfinite(x) & (x > 0) & (x < 1) & np.isfinite(stat) & (stat > 0)
    return x[mask], stat[mask]


def scenario_label(scenario, p2p):
    """Return legend caption and filename suffix for one uncertainty scenario.

    Args:
        scenario, p2p: Inputs and configuration for this operation.
    Returns:
        Computed data or saved file paths, as described above.
    """
    exp = 100 * p2p
    if scenario.mode == 'experimental':
        return (rf'{scenario.name.title()}: exp. syst. $\pm {exp:g}\%$',
                f'experimental{exp:g}pct'.replace('.', 'p'))
    flux = 100 * scenario.flux
    return (rf'{scenario.name.title()}: flux $\pm {flux:g}\%$, exp. $\pm {exp:g}\%$',
            f'flux{flux:g}pct'.replace('.', 'p'))


def _axes(pion_inset):
    """Create an 8-inch square publication plot and optional low-x inset.

    Args:
        pion_inset: Inputs and configuration for this operation.
    Returns:
        Computed data or saved file paths, as described above.
    """
    plt.rcParams.update(STYLE)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.minorticks_on()
    ax.grid(False)
    inset = None
    if pion_inset:
        inset = inset_axes(ax, width='42%', height='35%', loc='upper left',
                           bbox_to_anchor=(.05, 0., 1., 1.), bbox_transform=ax.transAxes,
                           borderpad=1.2)
        inset.set_xscale('log')
        inset.set_xlim(.001, .1)
        inset.minorticks_on()
        inset.grid(False)
        inset.tick_params(axis='both', which='major', labelsize=9, length=4)
        inset.tick_params(axis='both', which='minor', length=2)
    return fig, ax, inset


def _save(fig, folder, name):
    """Write PDF and 300-dpi PNG into folder; return saved paths.

    Args:
        fig, folder, name: Inputs and configuration for this operation.
    Returns:
        Computed data or saved file paths, as described above.
    """
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    file = folder / f'{name}.png'
    fig.subplots_adjust(left=.13, right=.96, bottom=.12, top=.96)
    fig.savefig(file, dpi=300, bbox_inches='tight')
    plt.close(fig)
    return (file,)


def _band(ax, x, central, error, color, label=None, alpha=.25):
    """Draw one uncertainty envelope and return Matplotlib artist.

    Args:
        ax, x, central, error, color, label, alpha: Inputs and configuration for this operation.
    Returns:
        Computed data or saved file paths, as described above.
    """
    return ax.fill_between(x, central - error, central + error,
                           color=color, alpha=alpha, linewidth=0, label=label)


def plot_dse(channel, beam, component, scenario, uq_dir, outdir, *, p2p=.025,
             e615_file=None):
    """Plot original DSE SCI/CSM curves and EIC uncertainty envelopes; return paths.

    Args:
        channel, beam, component, scenario, uq_dir, outdir, p2p, e615_file: Inputs and configuration for this operation.
    Returns:
        Computed data or saved file paths, as described above.
    """
    curves_x = np.arange(.001, 1., .001)
    sci, csm, mean = dse_evaluate(channel, component, curves_x)
    fig, ax, inset = _axes(pion_inset=(channel == 'pion'))
    colors = colormaps['Blues'](np.linspace(.35, .95, len(scenario.luminosities)))
    legend, suffix = scenario_label(scenario, p2p)
    found = 0
    for lumi, color in zip(scenario.luminosities, colors):
        uq = read_uq(uq_dir, channel, beam, lumi)
        if uq is None or not uq[0].size:
            continue
        x, stat = uq
        y_sci, y_csm, central = dse_evaluate(channel, component, x)
        _ = y_sci, y_csm
        err = abs(central) * np.sqrt(stat ** 2 + p2p ** 2 + scenario.flux ** 2)
        label = rf'Projection {beam} GeV : {lumi:g} fb$^{{-1}}$'
        _band(ax, x, central, err, color, label)
        if inset is not None:
            mask = x <= .1
            _band(inset, x[mask], central[mask], err[mask], color)
        found += 1
    if not found:
        plt.close(fig)
        return ()
    if channel == 'pion' and component == 'valence' and e615_file and Path(e615_file).is_file():
        x, y, dy = np.loadtxt(e615_file, unpack=True)
        ax.errorbar(x, y, yerr=dy, fmt='s', color='black', label='E615-A')
    if channel == 'pion':
        ax.plot(curves_x, mean, ':', color='black', linewidth=1.8, label='Mean(SCI, CSM)')
    ax.plot(curves_x, sci, '--', color='green', linewidth=2, label='DSE-SCI')
    ax.plot(curves_x, csm, '-', color='purple', linewidth=2, label='DSE-CSM')
    if inset is not None:
        inset.plot(curves_x, sci, '--', color='green', linewidth=1.5)
        inset.plot(curves_x, csm, '-', color='purple', linewidth=1.5)
        inset.plot(curves_x, mean, ':', color='black', linewidth=1.2)
    meson = r'\pi' if channel == 'pion' else 'K'
    label = ('u_v' if component == 'valence' else 'g')
    xlabel = rf'$x_{{{meson}}}$'
    ylabel = (rf'$x_{{{meson}}} {label}^{{{meson}}}(x)$ : valence'
              if component == 'valence' else
              rf'$x_{{{meson}}} g^{{{meson}}}(x;\zeta_5)\times(10x_{{{meson}}})^2$ : glue')
    ax.set(xlim=(0 if channel == 'pion' else .0001, 1),
           ylim=YLIMS_DSE[channel][component], xlabel=xlabel, ylabel=ylabel)
    ax.legend(
        frameon=False,
        title=legend,
        loc='best',
        fontsize=11,
    )
    return _save(fig, outdir, f'{channel}sf_proj_{beam}_CraigDSE_{component}_{scenario.name}_{suffix}')


def plot_jam(channel, beam, component, scenario, uq_dir, outdir, *, set_name,
             q2=5.2 ** 2, p2p=.025, lhapdf_path=None):
    """Plot JAM relative prior/posterior uncertainties around zero.

    Args:
        channel, beam, component: Meson, beam energy, and PDF observable.
        scenario: Luminosities and systematic assumptions.
        uq_dir, outdir: Statistical input CSV and output figure directories.
        set_name, q2, p2p, lhapdf_path: LHAPDF set, scale, pointwise error, and path.
    Returns:
        Tuple containing the saved PNG path, or empty tuple if no data exist.
    """
    replicas = load_replicas(set_name, lhapdf_path)
    xgrid = np.logspace(-3, np.log10(.95), 250)
    obs = jam_evaluate(replicas, xgrid, 'total', q2)
    prior_mean = obs.mean(axis=0)
    prior_std = obs.std(axis=0, ddof=1)
    valid_mean = np.isfinite(prior_mean) & (np.abs(prior_mean) > 1e-12)
    denominator = np.where(valid_mean, np.abs(prior_mean), np.nan)
    relative_prior = prior_std / denominator

    fig, ax, _ = _axes(pion_inset=False)
    ax.set_xscale('log')
    colors = colormaps['Blues'](np.linspace(.45, .90, len(scenario.luminosities)))
    legend, suffix = scenario_label(scenario, p2p)
    zero = np.zeros_like(xgrid)
    _band(ax, xgrid, zero, relative_prior, '0.65', r'JAM prior $\pm1\sigma$', .35)

    found = 0
    for lumi, color in zip(scenario.luminosities, colors):
        uq = read_uq(uq_dir, channel, beam, lumi)
        if uq is None or not uq[0].size:
            continue
        x, stat = uq
        f2 = jam_evaluate(replicas, x, 'total', q2)
        weights, neff = reweight_f2(f2, stat, p2p, scenario.flux)
        _, post_std = weighted_statistics(obs, weights)
        relative_post = post_std / denominator
        label = rf'After EIC {beam} GeV: {lumi:g} fb$^{{-1}}$'
        _band(ax, xgrid, zero, relative_post, color, label, .45)
        print(f'[{channel} {beam} JAM {component} {lumi:g}fb] N_eff replicas={neff:.1f}')
        found += 1

    if not found:
        plt.close(fig)
        return ()
    ax.axhline(0., color='black', linewidth=1.8, label=f'{set_name} mean')
    meson = r'\pi' if channel == 'pion' else 'K'
    ylabel = (
        rf'$(F_2^{{{meson}}} - \langle F_2^{{{meson}}}\rangle_{{\rm prior}})'
        rf'/|\langle F_2^{{{meson}}}\rangle_{{\rm prior}}|$'
    )
    ax.legend(frameon=False, loc='best', fontsize=11,
              title=legend + '\n' + rf'{set_name}, $Q^2={q2:.1f}\,\mathrm{{GeV}}^2$')
    return _save(fig, outdir,
                 f'{channel}sf_proj_{beam}_{set_name}_{component}_{scenario.name}_{suffix}')


def plot_all_models(channel, beam, uq_dir, outdir, *, models=('DSE', 'JAM'),
                    components=('valence', 'glue'), scenarios=SCENARIOS, p2p=.025,
                    jam_set=None, q2=5.2 ** 2, lhapdf_path=None, e615_file=None):
    """Create all requested model figures from existing uncertainty CSV; return paths.

    Args:
        channel, beam, uq_dir, outdir, models, components, scenarios, p2p, jam_set, q2, lhapdf_path, e615_file: Inputs and configuration for this operation.
    Returns:
        Computed data or saved file paths, as described above.
    """
    saved = []
    for model in models:
        model_components = ('total',) if model == 'JAM' else components
        for component in model_components:
            for scenario in scenarios:
                folder = Path(outdir) / 'models' / model.lower()
                if model == 'DSE':
                    paths = plot_dse(channel, beam, component, scenario, uq_dir, folder,
                                     p2p=p2p, e615_file=e615_file)
                elif model == 'JAM':
                    if jam_set is None:
                        raise ValueError('JAM plots require a configured LHAPDF set')
                    paths = plot_jam(channel, beam, component, scenario, uq_dir, folder,
                                     set_name=jam_set, q2=q2, p2p=p2p,
                                     lhapdf_path=lhapdf_path)
                else:
                    raise ValueError(f'Unknown model: {model}')
                saved.extend(paths)
    return saved