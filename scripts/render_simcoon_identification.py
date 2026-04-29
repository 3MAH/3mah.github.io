"""Run the new Simcoon Chaboche cyclic identification and render a
brand-styled experiment-vs-fit plot for the homepage.

Mirrors ``simcoon/examples/identification/chaboche_cyclic_identification.py``
(merged into master April 2026). Identifies seven EPCHA parameters
(``sigma_y``, ``Q``, ``b``, ``C_1``, ``D_1``, ``C_2``, ``D_2``) from three
cyclic uniaxial tests via differential evolution.

Output:
    assets/images/index/simcoon/simcoon_chaboche_identification.png

The pure-Python ``identify.py`` and ``parameter.py`` modules are loaded
straight from the local Simcoon source tree because the released
conda-forge wheel does not ship them yet. ``sim.solver`` (compiled C++)
is taken from the conda env. Set ``SIMCOON_REPO`` if you keep your
checkout somewhere other than ``~/Documents/GitHub/simcoon``.
"""

from __future__ import annotations

import importlib.util
import os
import sys
import types
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "assets" / "images" / "index" / "simcoon"
OUT.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT / "simcoon_chaboche_identification.png"
OUT_VIDEO = OUT / "simcoon_chaboche_identification.mp4"

# Brand palette matching the rest of render_simcoon.py
BRAND_RED = "#971C20"
BRAND_ORANGE = "#D9531E"
BRAND_GOLD = "#E2A53A"
BRAND_INK = "#1F1F22"
BRAND_GREY = "#5A5A60"
BRAND_LIGHT = "#F4ECE3"

# Three brand-tinted hues for the three tests (deeper → lighter)
TEST_COLORS = ["#971C20", "#D9531E", "#E2A53A"]

DPI = 160
FIGSIZE = (14, 6.5)


def find_simcoon_repo() -> Path:
    env = os.environ.get("SIMCOON_REPO")
    if env:
        p = Path(env).expanduser().resolve()
        if (p / "examples" / "identification").is_dir():
            return p
        raise SystemExit(f"SIMCOON_REPO={env} does not look like a simcoon checkout")
    # Default: sibling to this repo, in ~/Documents/GitHub/simcoon
    default = Path.home() / "Documents" / "GitHub" / "simcoon"
    if (default / "examples" / "identification").is_dir():
        return default
    raise SystemExit(
        "could not locate simcoon source tree.\n"
        "  set SIMCOON_REPO=/path/to/simcoon (the one that contains "
        "examples/identification/chaboche_cyclic_identification.py)"
    )


def load_module(name: str, path: Path) -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def style_axes(ax):
    ax.set_facecolor("white")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(BRAND_INK)
        ax.spines[s].set_linewidth(1.2)
    ax.tick_params(colors=BRAND_INK, length=4, width=1.0)
    ax.grid(True, color=BRAND_GREY, alpha=0.18, linewidth=0.7)


def main():
    simcoon_repo = find_simcoon_repo()
    example_dir = simcoon_repo / "examples" / "identification"
    sources = simcoon_repo / "python-setup" / "simcoon"

    # Vendor the new pure-Python helpers from the source tree
    parameter_mod = load_module("simcoon_parameter_local", sources / "parameter.py")
    identify_mod  = load_module("simcoon_identify_local",  sources / "identify.py")
    Parameter      = parameter_mod.Parameter
    identification = identify_mod.identification
    calc_cost      = identify_mod.calc_cost

    import simcoon as sim  # compiled extension from the conda env

    # ----- example mirror ----------------------------------------------------
    TESTS = [
        ("test1", "path_id_1.txt", "tab_file_1.txt",  "exp_file_1.txt"),
        ("test2", "path_id_2.txt", "tab_file_15.txt", "exp_file_15.txt"),
        ("test3", "path_id_3.txt", "tab_file_2.txt",  "exp_file_2.txt"),
    ]
    UMAT_NAME, NSTATEV = "EPCHA", 33
    SOLVER_TYPE, CORATE_TYPE = 0, 2
    E_FIXED, NU_FIXED, ALPHA_FIXED = 140000.0, 0.3, 1.0e-6
    PARAMS = [
        Parameter(1, bounds=(50,    300),    key="@1p"),  # sigmaY
        Parameter(2, bounds=(100,   10000),  key="@2p"),  # Q
        Parameter(3, bounds=(0.01,  10.0),   key="@3p"),  # b
        Parameter(4, bounds=(1000,  100000), key="@4p"),  # C_1
        Parameter(5, bounds=(10,    1000),   key="@5p"),  # D_1
        Parameter(6, bounds=(10000, 1.0e6),  key="@6p"),  # C_2
        Parameter(7, bounds=(10,    10000),  key="@7p"),  # D_2
    ]
    PARAM_NAMES = ["sigmaY", "Q", "b", "C_1", "D_1", "C_2", "D_2"]
    SIGMA11_COL = 14

    def build_props(x):
        return np.array([E_FIXED, NU_FIXED, ALPHA_FIXED, *x])

    def run_one(props, pathfile, outputfile, path_data, path_results):
        sim.solver(
            UMAT_NAME, props, NSTATEV, 0.0, 0.0, 0.0,
            SOLVER_TYPE, CORATE_TYPE, path_data, path_results,
            pathfile, outputfile,
        )
        base = outputfile[:-4] if outputfile.endswith(".txt") else outputfile
        out = np.loadtxt(os.path.join(path_results, f"{base}_global-0.txt"))
        return out[:, SIGMA11_COL]

    def cost(x, exp_stresses, path_data, path_results):
        props = build_props(x)
        y_num = []
        for name, pathfile, _tab, _exp in TESTS:
            try:
                sigma11 = run_one(props, pathfile, f"sim_{name}.txt",
                                  path_data, path_results)
            except Exception:
                return 1e12
            y_num.append(sigma11.reshape(-1, 1))
        return calc_cost(exp_stresses, y_num, metric="nmse_per_response")

    # sim.solver reads/writes relative to cwd
    cwd = os.getcwd()
    os.chdir(example_dir)
    try:
        path_data, path_results, path_exp = "data", "results", "exp_data"
        os.makedirs(path_results, exist_ok=True)
        exp_stresses = []
        for _, _, _, expfile in TESTS:
            exp = np.loadtxt(os.path.join(path_exp, expfile))
            exp_stresses.append(exp[:, 3].reshape(-1, 1))

        # Capture best-of-generation parameter vectors so we can replay
        # the convergence as an animation after the optimisation finishes.
        history: list[np.ndarray] = []

        def _de_callback(xk, convergence=None):
            history.append(np.asarray(xk).copy())
            return False

        print(" Chaboche cyclic identification — running differential evolution …")
        result = identification(
            cost, PARAMS,
            args=(exp_stresses, path_data, path_results),
            seed=42, popsize=15, maxiter=80, tol=1e-6, disp=False,
            callback=_de_callback,
        )
        print(f"   final cost = {result.fun:.4e}   ({len(history)} generations)")

        final_props = build_props(np.array([p.value for p in PARAMS]))

        # ----- branded plot ------------------------------------------------
        mpl.rcParams.update({
            "font.family": "DejaVu Sans",
            "font.size": 18,
            "axes.titlesize": 22,
            "axes.titleweight": "bold",
            "axes.labelsize": 19,
            "axes.titlecolor": BRAND_INK,
            "axes.labelcolor": BRAND_INK,
            "axes.edgecolor": BRAND_INK,
            "savefig.dpi": DPI,
        })
        fig, ax = plt.subplots(figsize=FIGSIZE)
        style_axes(ax)
        for (name, pathfile, _tab, expfile), color in zip(TESTS, TEST_COLORS):
            exp = np.loadtxt(os.path.join(path_exp, expfile))
            sigma_num = run_one(
                final_props, pathfile, f"sim_{name}_final.txt",
                path_data, path_results,
            )
            ax.plot(exp[:, 2] * 100, exp[:, 3], color=color, linestyle="--",
                    linewidth=1.4, alpha=0.55, label=f"{name} — experiment")
            ax.plot(exp[:, 2] * 100, sigma_num, color=color, linestyle="-",
                    linewidth=2.4, label=f"{name} — identified")
        ax.set_xlabel(r"strain $\varepsilon_{11}$  [%]")
        ax.set_ylabel(r"stress $\sigma_{11}$  [MPa]")
        ax.set_title("Chaboche cyclic identification — 7 parameters from 3 tests")

        # Legend with two columns: dashed (experiment) and solid (fit)
        ax.legend(loc="lower right", framealpha=0.92, ncol=2,
                  fontsize=14, edgecolor=BRAND_GREY)

        # Identified parameters as a small annotation box
        param_lines = ["Identified (EPCHA, E = 140 GPa, ν = 0.3):"]
        for n, p in zip(PARAM_NAMES, PARAMS):
            param_lines.append(f"  {n} = {p.value:.3g}")
        ax.text(0.02, 0.98, "\n".join(param_lines), transform=ax.transAxes,
                ha="left", va="top", fontsize=13, color=BRAND_INK,
                family="DejaVu Sans Mono",
                bbox=dict(facecolor=BRAND_LIGHT, edgecolor="none",
                          pad=8, alpha=0.92))
        fig.tight_layout()
        fig.savefig(OUT_PATH, dpi=DPI, bbox_inches="tight", pad_inches=0.35)
        plt.close(fig)
        print(f"   wrote {OUT_PATH} ({OUT_PATH.stat().st_size / 1024:.0f} KB)")

        # ----- convergence animation (MP4) ---------------------------------
        if history:
            print(f" Replaying {len(history)} generations into an MP4 …")
            import imageio.v2 as iio
            # Sub-sample to ~25 frames so replay stays under a minute.
            n_anim = min(25, len(history))
            sample_idx = np.linspace(0, len(history) - 1, n_anim).astype(int)

            # Pre-compute experiment arrays once
            exp_data = {}
            for _, _, _, expfile in TESTS:
                exp_data[expfile] = np.loadtxt(os.path.join(path_exp, expfile))
            # Stable axis limits across the animation
            all_exp_strain = np.concatenate(
                [exp_data[expfile][:, 2] for *_, expfile in TESTS]
            ) * 100.0
            all_exp_stress = np.concatenate(
                [exp_data[expfile][:, 3] for *_, expfile in TESTS]
            )
            xlim = (1.05 * all_exp_strain.min(), 1.05 * all_exp_strain.max())
            ylim = (1.10 * all_exp_stress.min(), 1.10 * all_exp_stress.max())

            frames = []
            for k, gen_idx in enumerate(sample_idx):
                xk = history[gen_idx]
                props_k = build_props(xk)
                fig, ax = plt.subplots(figsize=FIGSIZE)
                style_axes(ax)
                ax.set_xlim(xlim)
                ax.set_ylim(ylim)
                for (name, pathfile, _tab, expfile), color in zip(TESTS, TEST_COLORS):
                    exp = exp_data[expfile]
                    try:
                        sigma_num = run_one(
                            props_k, pathfile, f"sim_anim_{name}.txt",
                            path_data, path_results,
                        )
                    except Exception:
                        continue
                    ax.plot(exp[:, 2] * 100, exp[:, 3], color=color,
                            linestyle="--", linewidth=1.4, alpha=0.55,
                            label=f"{name} — experiment")
                    ax.plot(exp[:, 2] * 100, sigma_num, color=color,
                            linestyle="-", linewidth=2.4,
                            label=f"{name} — current fit")
                ax.set_xlabel(r"strain $\varepsilon_{11}$  [%]")
                ax.set_ylabel(r"stress $\sigma_{11}$  [MPa]")
                ax.set_title(
                    f"Differential-evolution generation "
                    f"{gen_idx + 1} / {len(history)}"
                )
                ax.legend(loc="lower right", framealpha=0.92, ncol=2,
                          fontsize=12, edgecolor=BRAND_GREY)
                fig.tight_layout()
                fig.canvas.draw()
                w, h = fig.canvas.get_width_height()
                # Even dimensions for libx264 / yuv420p
                rgba = np.asarray(fig.canvas.buffer_rgba())
                rgb = rgba[..., :3]
                if rgb.shape[1] % 2 == 1:
                    rgb = rgb[:, :-1, :]
                if rgb.shape[0] % 2 == 1:
                    rgb = rgb[:-1, :, :]
                frames.append(rgb)
                plt.close(fig)
                print(f"   frame {k+1}/{n_anim}  (gen {gen_idx+1})")

            # Hold the final frame for ~1.5 s
            for _ in range(6):
                frames.append(frames[-1])

            iio.mimsave(
                OUT_VIDEO, frames, fps=4,
                codec="libx264", quality=7, pixelformat="yuv420p",
            )
            print(f"   wrote {OUT_VIDEO} ({OUT_VIDEO.stat().st_size / 1024:.0f} KB)")
    finally:
        os.chdir(cwd)


if __name__ == "__main__":
    main()
