"""Selection windows, mass fits, cutflow and purity presentation."""
from __future__ import annotations
import json
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from config import (COLOR_COMMON_LAMBDA, COLOR_MC, COLOR_NO_BACKGROUND, COLOR_WITH_BACKGROUND, FIT_MASS_HIGH, FIT_MASS_LOW, FIT_PI0_HIGH, FIT_PI0_LOW, MIN_FIT_ENTRIES, MLSIGMA, MPSIGMA, M_LAMBDA, M_PI0, PLOT_FULL_DATA_RANGE, THETA_GG_MAX_MRAD, THETA_GG_MIN_MRAD, THETA_LAMBDA_MAX_MRAD, THETA_LAMBDA_MIN_MRAD, TMAX, XL_MAX, Z_LAMBDA_MAX_M, Z_LAMBDA_MIN_M)
from plotting import finite, _percent_weights, _style_hist_axes, plot_stairs, _square_figure
from root_io import write_rows_csv



def pass_t(r):
    """None disables cut completely, including the -t >= 0 requirement."""
    return TMAX is None or (np.isfinite(r.get('minus_t', np.nan)) and 0 <= r['minus_t'] < TMAX)


def pass_xl(r):
    """Check the xl selection criterion."""
    return XL_MAX is None or (np.isfinite(r.get('xL', np.nan)) and 0 <= r['xL'] < XL_MAX)


def pass_lambda_mass(r, fit):
    """Check the lambda mass selection criterion."""
    if MLSIGMA is None:
        return True
    return bool(fit is not None and np.isfinite(r.get('mass', np.nan)) and
                fit['window_low_GeV'] <= r['mass'] <= fit['window_high_GeV'])


def pass_pi0(event, pairs, fit):
    """Check the pi0 selection criterion."""
    if MPSIGMA is None:
        return True
    if fit is None or not (0 <= event < len(pairs)):
        return False
    pair = pairs[event]
    return bool(pair is not None and np.isfinite(pair['mass']) and
                fit['window_low_GeV'] <= pair['mass'] <= fit['window_high_GeV'])


def pass_core(r, fit, pi0_fit, pi0_pairs):
    """Check the core selection criterion."""
    return (pass_t(r) and pass_xl(r) and pass_lambda_mass(r, fit)
            and pass_pi0(r['event'], pi0_pairs, pi0_fit))


def fit_lambda_mass(rows, folder):
    """Gaussian-core mass fit after the |t| cut. No mass selection if fit fails."""
    from scipy.optimize import curve_fit
    folder.mkdir(parents=True, exist_ok=True)
    values = np.array([r['mass'] for r in rows if np.isfinite(r['mass'])], float)
    core = values[(values >= FIT_MASS_LOW) & (values <= FIT_MASS_HIGH)]
    if core.size < 12:
        print(f'[POST-CUT WARNING] Only {core.size} masses in fit window; cannot fit Gaussian.')
        return None
    edges = np.linspace(FIT_MASS_LOW, FIT_MASS_HIGH, 31)
    hist, _ = np.histogram(core, bins=edges)
    centers = 0.5 * (edges[1:] + edges[:-1])
    def gauss(x, A, mu, sigma, C):
        """Compute gauss for the analysis."""
        return A * np.exp(-0.5 * ((x - mu) / sigma)**2) + C
    try:
        popt, cov = curve_fit(
            gauss, centers, hist, p0=[max(1., float(hist.max())), M_LAMBDA, 0.008, 0.],
            bounds=([0., M_LAMBDA - 0.015, 0.001, 0.],
                    [np.inf, M_LAMBDA + 0.015, 0.04, np.inf]),
            sigma=np.sqrt(np.maximum(hist, 1)), absolute_sigma=True, maxfev=30000)
        A, mu, sigma, C = map(float, popt)
        fit_valid = np.all(np.isfinite(popt)) and A > 0 and 0.001 < sigma < 0.04
        if not fit_valid: raise ValueError(f'Fit not valid: {popt}')
    except (RuntimeError, ValueError) as exc:
        print(f'[POST-CUT WARNING] Gaussian mass fit failed: {exc}')
        return None
    low, high = mu - MLSIGMA * sigma, mu + MLSIGMA * sigma
    fig, ax = plt.subplots(figsize=(6.0, 6.0))
    plot_stairs(ax, values, np.arange(1.04, 1.190001, 0.002), color='black', label='Reco after |t| cut')
    x = np.linspace(FIT_MASS_LOW, FIT_MASS_HIGH, 400)
    # Fit is in 2-MeV bins; plot density converted to the histogram bin width.
    ax.plot(x, gauss(x, *popt), color='#1f77b4', label=rf'Gaussian + constant: $\mu={mu:.5f}$, $\sigma={sigma*1000:.1f}$ MeV')
    ax.axvline(M_LAMBDA, color='gray', linestyle=':', label='PDG mass')
    ax.axvspan(low, high, color='tab:orange', alpha=0.16, label=rf'$\mu\pm {MLSIGMA:g}\sigma$')
    ax.set(xlabel=r'$m_{n\gamma\gamma}$ [GeV]', ylabel='Counts / 2 MeV', title='Lambda mass fit after |t| cut')
    _style_hist_axes(ax, values=values, xlabel='mass'); ax.legend(fontsize=13)
    fig.tight_layout(); fig.savefig(folder/'mass_gaussian_fit.png'); plt.close(fig)
    return {'fit_mean_GeV':mu, 'fit_sigma_GeV':sigma, 'fit_constant':C,
            'fit_amplitude':A, 'window_low_GeV':low, 'window_high_GeV':high,
            'n_fit_window':int(core.size), 'n_sigma':MLSIGMA}


def fit_pi0_mass(masses, folder):
    """Fit signal-only best-pair pi0 peak; use identical window for background.

    The best pair is chosen closest to PDG mass, so the fitted width is
    selection-biased, not a truth-matched detector resolution.
    Fit Gaussian + non-negative constant pedestal. Fit failure -> no pi0
    post-cut candidates: never silently skip the requested mass cut.
    """
    from scipy.optimize import curve_fit
    if folder is not None:
        folder.mkdir(parents=True, exist_ok=True)
    arr = finite(masses)
    core = arr[(arr>=FIT_PI0_LOW)&(arr<=FIT_PI0_HIGH)]
    if len(core) < MIN_FIT_ENTRIES:
        print(f'[PI0 WARNING] Only {len(core)} entries in fit range; pi0 cut unavailable.')
        return None
    edges=np.linspace(FIT_PI0_LOW,FIT_PI0_HIGH,57)
    hist,_=np.histogram(core,bins=edges)
    xc=(edges[1:]+edges[:-1])/2
    def model(x,A,mu,sigma,C):
        """Compute model for the analysis."""
        return A*np.exp(-0.5*((x-mu)/sigma)**2)+C
    try:
        fit,_=curve_fit(model,xc,hist,
            p0=[max(1.,float(hist.max())),M_PI0,0.015,max(0.,float(np.median(hist)))],
            bounds=([0.,M_PI0-0.05,0.002,0.],[np.inf,M_PI0+0.05,0.075,np.inf]),
            sigma=np.sqrt(np.maximum(hist,1)),absolute_sigma=True,maxfev=30000)
        A,mu,sigma,C=map(float,fit)
        if not (np.all(np.isfinite(fit)) and A>0 and 0.002<sigma<0.075):
            raise ValueError(f'Fit parameters invalid: {fit}')
    except (ValueError,RuntimeError) as exc:
        print(f'[PI0 WARNING] Gaussian fit failed: {exc}')
        return None
    lo,hi=mu-MPSIGMA*sigma,mu+MPSIGMA*sigma
    if folder is not None:
        fig,ax=plt.subplots(figsize=(6,6))
        plot_stairs(ax,arr,edges,weights=_percent_weights(arr),
                linewidth=2,color=COLOR_NO_BACKGROUND,label=r'Best $\gamma\gamma$ pair / event (signal, pre-cut)')
        xx=np.linspace(FIT_PI0_LOW,FIT_PI0_HIGH,400)
        ax.plot(xx,model(xx,*fit)*100./len(arr),color=COLOR_COMMON_LAMBDA,
                label=rf'Fit $\mu={mu:.4f}$ GeV, $\sigma={sigma*1000:.1f}$ MeV')
        ax.axvline(M_PI0,color=COLOR_MC,ls=':',label=r'PDG $m_{\pi^0}$')
        ax.axvspan(lo,hi,color=COLOR_WITH_BACKGROUND,alpha=.15,
                   label=rf'$\pm {MPSIGMA:g}\sigma$ selection')
        ax.set(xlabel=r'$m_{\gamma\gamma}$ [GeV]',ylabel='Fraction of selected pairs [%]')
        _style_hist_axes(ax)
        ax.legend()
        fig.tight_layout();fig.savefig(folder/'pi0_mass_gaussian_fit.png');plt.close(fig)
    return {'fit_mean_GeV':mu,'fit_sigma_GeV':sigma,'fit_amplitude':A,
            'fit_constant':C,'window_low_GeV':lo,'window_high_GeV':hi,
            'n_fit_window':len(core),'n_sigma':MPSIGMA,
            'sample_definition':'best gamma-gamma pair per event, before mass cuts; signal only'}


def _binary_class(truth):
    """Compute binary class for the analysis."""
    if truth is None:
        return 'unclassified'
    return truth.get('binary_class', 'unclassified')


def _binary_histogram(ax, rows, field, edges, denominator):
    """Compute binary histogram for the analysis."""
    for name, color in [('signal', '#2e8b57'), ('combinatorial', '#5b6573')]:
        vals = finite([r[field] for r in rows if r['binary_class'] == name])
        if len(vals):
            plot_stairs(ax, vals, edges, linewidth=2.1, color=color,
                    weights=np.full(len(vals), 100. / max(1, denominator)),
                    label=f'{name.capitalize()} (N={len(vals)})')


def _binary_class_counts(rows):
    """Compute binary class counts for the analysis."""
    c = Counter(r.get('binary_class', 'unclassified') for r in rows)
    n = len(rows)
    known = c['signal'] + c['combinatorial']
    return dict(total=n, signal=c['signal'], combinatorial=c['combinatorial'],
                unclassified=n-known,
                signal_fraction=c['signal']/known if known else np.nan,
                signal_fraction_all=c['signal']/n if n else np.nan,
                signal_efficiency_raw=np.nan)


def _within(value, low=None, high=None):
    """Compute within for the analysis."""
    if low is None and high is None:
        return True
    return bool(np.isfinite(value) and (low is None or value >= low)
                and (high is None or value <= high))


def _all_cut_definitions(lambda_fit, pion_fit):
    """All selections independent of ordering and evaluated on the SAME candidate."""
    return [
        ('minus_t', r'$-t$ [GeV$^2$]', lambda r: pass_t(r),
         TMAX is not None, (0.,TMAX)),
        ('xL', r'$x_L$', lambda r: pass_xl(r),
         XL_MAX is not None, (0.,XL_MAX)),
        ('lambda_mass', r'$M_{n\gamma\gamma}$ [GeV]',
         lambda r: pass_lambda_mass(r,lambda_fit),
         MLSIGMA is not None, ((lambda_fit or {}).get('window_low_GeV'),
                              (lambda_fit or {}).get('window_high_GeV'))),
        ('pi0_mass', r'$M_{\gamma\gamma}$ [GeV] (Lambda daughters)',
         lambda r: _within(r['pi0_daughter_mass_GeV'],
                           (pion_fit or {}).get('window_low_GeV'),
                           (pion_fit or {}).get('window_high_GeV')) if MPSIGMA is not None and pion_fit is not None
                           else MPSIGMA is None,
         MPSIGMA is not None, ((pion_fit or {}).get('window_low_GeV'),
                              (pion_fit or {}).get('window_high_GeV'))),
        ('theta_gg', r'$\theta_{\gamma\gamma}$ [mrad]',
         lambda r: _within(r['theta_gg_mrad'],THETA_GG_MIN_MRAD,THETA_GG_MAX_MRAD),
         THETA_GG_MIN_MRAD is not None or THETA_GG_MAX_MRAD is not None,
         (THETA_GG_MIN_MRAD,THETA_GG_MAX_MRAD)),
        ('theta_lambda', r'$\theta_\Lambda$ [mrad]',
         lambda r: _within(r['theta_lambda_mrad'],THETA_LAMBDA_MIN_MRAD,THETA_LAMBDA_MAX_MRAD),
         THETA_LAMBDA_MIN_MRAD is not None or THETA_LAMBDA_MAX_MRAD is not None,
         (THETA_LAMBDA_MIN_MRAD,THETA_LAMBDA_MAX_MRAD)),
        ('z_vertex', r'$z_\Lambda$ [m] (pointing hypothesis)',
         lambda r: _within(r['z_lambda_reco_m'],Z_LAMBDA_MIN_M,Z_LAMBDA_MAX_M),
         Z_LAMBDA_MIN_M is not None or Z_LAMBDA_MAX_M is not None,
         (Z_LAMBDA_MIN_M,Z_LAMBDA_MAX_M)),
    ]


def unified_cut_study(records,candidates,out,sample,lambda_fit,pion_fit,n_generated):
    """One uniform pass for cutflow, single-cut studies, N-1 and publications plots."""
    folder=out/'reconstruction'/'purity'
    folder.mkdir(parents=True,exist_ok=True)
    truth={(int(r['event']),int(r['lambda_index'])):r for r in records}
    joined=[]
    for r in candidates:
        t=truth.get((int(r['event']),int(r.get('_lambda_index',0))))
        if t is None: continue
        joined.append(dict(event=int(r['event']),lambda_index=int(r['_lambda_index']),
            binary_class=_binary_class(t), detailed_category=t.get('category','unknown'),
            minus_t=r.get('minus_t',np.nan),xL=r.get('xL',np.nan),
            mass=r.get('mass',np.nan),
            pi0_daughter_mass_GeV=t.get('pi0_daughter_mass_GeV',np.nan),
            theta_gg_mrad=t.get('theta_gg_mrad',np.nan),
            theta_lambda_mrad=r.get('theta_mrad',np.nan),
            z_lambda_reco_m=t.get('z_lambda_reco_m',np.nan),
            z_lambda_method=t.get('z_lambda_method','unavailable'),
            E=r.get('E',np.nan),p=r.get('p',np.nan),pt=r.get('pt',np.nan),
            pz=r.get('pz',np.nan),eta=r.get('eta',np.nan)))
    definitions=_all_cut_definitions(lambda_fit,pion_fit)
    for key,label,test,enabled,bounds in definitions:
        for r in joined:
            r['pass_'+key]=bool(test(r))
    for r in joined:
        r['pass_all']=all(r['pass_'+k] for k,_,_,_,_ in definitions)
    base_signal=sum(r['binary_class']=='signal' for r in joined)
    def metric(stage,subset,active=None):
        """Compute metric for the analysis."""
        row=dict(stage=stage,active=active,**_binary_class_counts(subset))
        row['signal_efficiency_raw']=row['signal']/base_signal if base_signal else np.nan
        return row
    stages=[metric('raw',joined)]
    current=joined
    for key,label,test,enabled,bounds in definitions:
        current=[r for r in current if r['pass_'+key]]
        stages.append(metric(key+'_cut',current,enabled))
    final=[r for r in joined if r['pass_all']]
    assert {(r['event'],r['lambda_index']) for r in current} == {(r['event'],r['lambda_index']) for r in final}
    # PUBLICATION CUT-FLOW: xL and Lambda mass form the mandatory reference.
    # Only additional enabled cuts appear as subsequent columns. The original
    # all-cut truth_cutflow CSV is intentionally kept intact below.
    if not n_generated or n_generated <= 0:
        raise ValueError('Normalized cutflow requires a positive MC Lambda denominator')
    baseline_keys = ('xL', 'lambda_mass')
    reference = [r for r in joined if all(r['pass_'+key] for key in baseline_keys)]
    visual_stages = [metric('baseline_xL_lambda_mass', reference, True)]
    visual_current = reference
    # Ordering is explicit and independent of the order of the physical cuts.
    optional_keys = ('minus_t', 'pi0_mass', 'theta_gg', 'theta_lambda', 'z_vertex')
    definitions_by_key = {d[0]: d for d in definitions}
    plot_labels = {
        'baseline_xL_lambda_mass': r'$x_L$ + $M_\Lambda$ (baseline)',
        'minus_t': r'$-t$', 'pi0_mass': r'$M_{\pi^0}$',
        'theta_gg': r'$\theta_{\gamma\gamma}$',
        'theta_lambda': r'$\theta_\Lambda$',
        'z_vertex': r'$z_\Lambda$',
    }
    for key in optional_keys:
        enabled = definitions_by_key[key][3]
        if not enabled:
            continue  # disabled optional cuts must not generate redundant bars
        visual_current = [r for r in visual_current if r['pass_'+key]]
        visual_stages.append(metric(key+'_cut', visual_current, True))
    assert {(r['event'], r['lambda_index']) for r in visual_current} == {
        (r['event'], r['lambda_index']) for r in final
    }, 'The plotted optional-cut flow must match the full selection'

    for r in visual_stages:
        r['n_generated_lambda'] = int(n_generated)
        r['candidate_yield_per_generated_lambda'] = r['total']/n_generated
        r['signal_yield_per_generated_lambda'] = r['signal']/n_generated
        r['combinatorial_yield_per_generated_lambda'] = r['combinatorial']/n_generated
    pass  # No intermediate data export.

    fig_width = max(6.4, 1.35*len(visual_stages)+2.0)
    fig,ax=plt.subplots(figsize=(fig_width,6.4))
    xx=np.arange(len(visual_stages))
    bottom=np.zeros(len(visual_stages), dtype=float)
    for cls,color in [('signal','#2e8b57'),('combinatorial','#5b6573')]:#,
#                      ('unclassified','#aaaaaa')]:
        counts=np.asarray([r[cls] for r in visual_stages], dtype=float)
        values=100.0*counts/n_generated
        if not np.any(values):
            continue
        ax.bar(xx,values,bottom=bottom,label=cls.capitalize(),color=color,
               width=.70,edgecolor='white',linewidth=.6)
        for j,v in enumerate(values):
            fraction=100.*counts[j]/visual_stages[j]['total'] if visual_stages[j]['total'] else 0.
            if v>=2.2 and fraction>=4.0:
                ax.text(xx[j],bottom[j]+v/2.,f'{fraction:.1f}%',
                        ha='center',va='center',fontsize=13,color='white',fontweight='bold')
        bottom+=values
    for j, r in enumerate(visual_stages):
        purity = 100. * r['signal_fraction'] if np.isfinite(r['signal_fraction']) else np.nan
        purity_text = f'{purity:.1f}%' if np.isfinite(purity) else 'n/a'
        n_classified = r['signal'] + r['combinatorial']
        classified_yield = 100. * n_classified / n_generated
        ax.annotate(
            f'P = {purity_text}\n'
            f'N = {n_classified:,} ({classified_yield:.1f}%)',
            (xx[j], classified_yield),
            xytext=(0, 6),
            textcoords='offset points',
            ha='center',
            va='bottom',
            fontsize=13
        )
    visual_labels=[plot_labels[r['stage'].removesuffix('_cut')]
                   if r['stage'].endswith('_cut') else plot_labels[r['stage']]
                   for r in visual_stages]
    ax.set_xticks(xx,visual_labels,rotation=22,ha='right')
    ax.set_ylabel(r'Reconstructed $\Lambda$ candidates / generated $\Lambda$ [\%]')
    ax.set_ylim(0,max(1.,float(np.max(bottom))*1.28))
    ax.legend(fontsize=13,ncol=3,loc='upper right')
    ax.set_title(r'Candidate yield and signal purity after mandatory $x_L$ and $M_\Lambda$ selection')
    ax.text(.01,.99,'P = signal / (signal + combinatorial)',transform=ax.transAxes,
            ha='left',va='top',fontsize=13)
    fig.tight_layout()
    fig.savefig(folder/f'truth_cutflow_{sample}.png');plt.close(fig)
    # Include plot denominator and yield in CSV for reproducible figures.
    for r in stages:
        r['n_generated_lambda']=int(n_generated)
        r['candidate_yield_per_generated_lambda']=r['total']/n_generated
        r['signal_yield_per_generated_lambda']=r['signal']/n_generated
        r['combinatorial_yield_per_generated_lambda']=r['combinatorial']/n_generated
    pass  # No intermediate data export.
    print('[UNIFIED CUTS]',sample,stages,flush=True)
    return joined,final,stages


def plot_pstar_cutflow(signal_rows, mixed_rows, out, n_generated):
    """Plot Lambda purity and reconstruction yield from the mixed (bkg_4) file.

    S: mixed-file candidates with at least one daughter tagged Sullivan (source 0).
    B: ALL other mixed-file candidates, including unresolved daughter origins.
    P* = S / (S + B); epsilon = S / generated Sullivan Lambdas.
    This operational source-tag measure is not strict decay truth matching.
    """
    folder = out / 'reconstruction' / 'purity'
    definitions = _all_cut_definitions(None, None)
    # Only the keys and enabled flags are needed: pass_* fields were already
    # evaluated, using the same fitted mass windows, by unified_cut_study.
    enabled = {key: active for key, _, _, active, _ in definitions}
    stages = [('baseline', ('xL', 'lambda_mass'))]
    active_keys = ['xL', 'lambda_mass']
    for key in ('minus_t', 'pi0_mass', 'theta_gg', 'theta_lambda', 'z_vertex'):
        if enabled[key]:
            active_keys.append(key)
            stages.append((key, tuple(active_keys)))

    labels = {'baseline': r'$x_L$ + $M_\Lambda$ (baseline)',
              'minus_t': r'$-t$', 'pi0_mass': r'$M_{\pi^0}$',
              'theta_gg': r'$\theta_{\gamma\gamma}$',
              'theta_lambda': r'$\theta_\Lambda$',
              'z_vertex': r'$z_\Lambda$'}
    signal_counts = []
    background_counts = []
    for _, required in stages:
        passes = lambda r: all(r['pass_' + cut] for cut in required)
        signal_counts.append(sum(passes(r) and r['binary_class'] == 'signal'
                                 for r in mixed_rows))
        background_counts.append(sum(passes(r) and r['binary_class'] != 'signal'
                                     for r in mixed_rows))
    S = np.array(signal_counts, dtype=float)
    B = np.array(background_counts, dtype=float)
    total = S + B
    purity = np.divide(S, total, out=np.full(len(S), np.nan), where=total > 0)
    xx = np.arange(len(stages))
    signal_y = 100. * S / n_generated
    bkg_y = 100. * B / n_generated
    heights = signal_y + bkg_y

    fig_width = max(6.4, 1.35 * len(stages) + 2.)
    fig, ax = plt.subplots(figsize=(fig_width, 6.4))
    ax.bar(xx, signal_y, width=.70, color='#2e8b57', edgecolor='white',
           linewidth=.6, label='Signal')
    ax.bar(xx, bkg_y, bottom=signal_y, width=.70, color='#5b6573',
           edgecolor='white', linewidth=.6,
           label='Background')
    for j in range(len(stages)):
        if signal_y[j] >= 2.2:
            ax.text(xx[j], signal_y[j] / 2.,
                    f'{100. * S[j] / total[j]:.1f}%' if total[j] else 'n/a',
                    ha='center', va='center', fontsize=13,
                    color='white', fontweight='bold')
        if bkg_y[j] >= 2.2:
            ax.text(xx[j], signal_y[j] + bkg_y[j] / 2.,
                    f'{100. * B[j] / total[j]:.1f}%' if total[j] else 'n/a',
                    ha='center', va='center', fontsize=13,
                    color='white', fontweight='bold')
        ptxt = f'{100. * purity[j]:.1f}%' if np.isfinite(purity[j]) else 'n/a'
        epsilon = 100. * S[j] / n_generated
        ax.annotate(f'ε = {epsilon:.1f}%\nP* = {ptxt}\nS = {int(S[j]):,}, B = {int(B[j]):,}',
                    (xx[j], heights[j]), xytext=(0, 6),
                    textcoords='offset points', ha='center', va='bottom',
                    fontsize=13)
    ax.set_xticks(xx, [labels[key] for key, _ in stages], rotation=22, ha='right')
    ax.set_ylabel(r'Reconstructed $\Lambda$ (\%)')
    ax.set_ylim(0, max(1., float(np.max(heights)) * 1.55))
    ax.legend(fontsize=13, ncol=2, loc='upper right')
    ax.set_title(r'Efficiency-purity trade-off studies (neutral decay channel)')
    fig.tight_layout()
    fig.savefig(folder / 'truth_cutflow_mixed.png')
    plt.close(fig)
    print('[P* CUT-FLOW] S (mixed, >=1 signal daughter):', signal_counts,
          'B (mixed, no signal daughter):', background_counts, flush=True)

