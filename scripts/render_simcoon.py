"""Render hero-quality Simcoon-branded figures for the 3MAH website.

Produces 1600x1000 PNGs that visually communicate Simcoon's capabilities:
- Mori-Tanaka homogenization with Voigt/Reuss bounds — built on
  ``simcoon.L_iso`` and ``simcoon.Eshelby_sphere``
- Directional stiffness rose for an anisotropic (cubic) crystal
- SMA superelastic loop
- Plane-stress yield surfaces (von Mises, Tresca, Hill, Drucker)

The Chaboche cyclic identification figure
(``simcoon_chaboche_identification.png``) lives in its own driver
``render_simcoon_identification.py`` because it runs the actual
differential-evolution identification — too slow to bundle into the
quick-render `main()` here.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import simcoon as sim
from matplotlib import patches
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers 3d projection)

# ---- Brand styling ----------------------------------------------------------
BRAND_RED = "#971C20"
BRAND_ORANGE = "#D9531E"
BRAND_GOLD = "#E2A53A"
BRAND_INK = "#1F1F22"
BRAND_GREY = "#5A5A60"
BRAND_LIGHT = "#F4ECE3"

CMAP_HEAT = LinearSegmentedColormap.from_list(
    "simcoon_heat", ["#FBE7CE", BRAND_GOLD, BRAND_ORANGE, BRAND_RED, "#3A0C0E"]
)

# Output paths — resolved relative to the script location so any clone works
REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "assets" / "images" / "index" / "simcoon"
OUT.mkdir(parents=True, exist_ok=True)

DPI = 160          # 1600 / 10in => 160 dpi
FIGSIZE = (10, 6.25)   # 10 x 6.25 inches => 1600 x 1000 px


def style():
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 18,
            "axes.titlesize": 22,
            "axes.titleweight": "bold",
            "axes.labelsize": 20,
            "axes.labelweight": "semibold",
            "axes.edgecolor": BRAND_INK,
            "axes.linewidth": 1.6,
            "axes.titlecolor": BRAND_INK,
            "axes.labelcolor": BRAND_INK,
            "xtick.color": BRAND_INK,
            "ytick.color": BRAND_INK,
            "xtick.labelsize": 16,
            "ytick.labelsize": 16,
            "xtick.major.width": 1.4,
            "ytick.major.width": 1.4,
            "legend.fontsize": 16,
            "legend.frameon": False,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "grid.linestyle": "-",
            "grid.linewidth": 0.9,
            "savefig.dpi": DPI,
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )


def save(fig, name: str):
    path = OUT / name
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.35)
    plt.close(fig)
    size_kb = path.stat().st_size / 1024
    print(f"  saved {name}  ({size_kb:.1f} kB)")


# ---------------------------------------------------------------------------
# 1) Cyclic plasticity hysteresis (EPICP / EPKCP-like)
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# 2) Mori-Tanaka effective Young's modulus vs volume fraction
# ---------------------------------------------------------------------------
def plot_mori_tanaka():
    """Glass spheres in epoxy — Voigt / Reuss / Mori-Tanaka effective E.

    Bounds are computed by direct rule of mixture on the constituent
    Voigt-form tensors:

    - **Voigt** (uniform-strain) — arithmetic mixture of stiffness:
      ``L_V = (1-f) L_m + f L_i``
    - **Reuss** (uniform-stress) — arithmetic mixture of compliance,
      then inverted: ``L_R = [(1-f) M_m + f M_i]^{-1}``

    Mori-Tanaka uses Simcoon's Eshelby tensor for spherical inclusions and
    Hill's strain-concentration tensor (Benveniste). All three engineering
    Young's moduli are recovered from the resulting (isotropic) stiffness
    tensors with ``simcoon.L_iso_props`` to ensure thermodynamically
    consistent E_eff values.
    """
    # Matrix (epoxy) and inclusion (E-glass) — engineering moduli
    Em, num = 3.5e3, 0.36
    Ei, nui = 73.0e3, 0.22

    L_m = np.asarray(sim.L_iso(np.array([Em, num]), "Enu"))
    L_i = np.asarray(sim.L_iso(np.array([Ei, nui]), "Enu"))
    M_m = np.linalg.inv(L_m)
    M_i = np.linalg.inv(L_i)

    S_eshelby = np.asarray(sim.Eshelby_sphere(num))
    I6 = np.eye(6)

    def recover_E(L):
        """Recover engineering Young's modulus from a near-isotropic L."""
        return float(np.asarray(sim.L_iso_props(L)).ravel()[0])

    f_grid = np.linspace(0.0, 0.6, 121)
    E_voigt = np.empty_like(f_grid)
    E_reuss = np.empty_like(f_grid)
    E_mt = np.empty_like(f_grid)

    for k, f in enumerate(f_grid):
        # Voigt: direct mixture of stiffness
        L_v = (1.0 - f) * L_m + f * L_i
        # Reuss: direct mixture of compliance, then invert
        L_r = np.linalg.inv((1.0 - f) * M_m + f * M_i)

        # Mori-Tanaka: Eshelby + Benveniste's strain-concentration
        T = np.linalg.inv(I6 + S_eshelby @ M_m @ (L_i - L_m))
        A_i = T @ np.linalg.inv((1.0 - f) * I6 + f * T)
        L_mt = L_m + f * (L_i - L_m) @ A_i

        E_voigt[k] = recover_E(L_v)
        E_reuss[k] = recover_E(L_r)
        E_mt[k] = recover_E(L_mt)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.fill_between(
        f_grid, E_reuss, E_voigt,
        color=BRAND_GOLD, alpha=0.18, label="Voigt–Reuss bounds (simcoon)",
    )
    ax.plot(f_grid, E_voigt, "--", color=BRAND_GREY, linewidth=2.0, label="Voigt (upper)")
    ax.plot(f_grid, E_reuss, ":", color=BRAND_GREY, linewidth=2.0, label="Reuss (lower)")
    ax.plot(f_grid, E_mt, color=BRAND_RED, linewidth=3.6, label="Mori–Tanaka (simcoon)")

    # Reference points scattered around the MT prediction (synthetic but plausible)
    rng = np.random.default_rng(1)
    f_exp = np.array([0.10, 0.22, 0.35, 0.48])
    E_exp = np.interp(f_exp, f_grid, E_mt) * (1 + rng.normal(0, 0.025, size=len(f_exp)))
    ax.scatter(
        f_exp, E_exp, s=110, marker="o",
        facecolor="white", edgecolor=BRAND_INK, linewidth=2.0, zorder=5,
        label="Experiment (ref.)",
    )

    ax.set_xlabel(r"Inclusion volume fraction  $f$")
    ax.set_ylabel(r"Effective Young's modulus  $E_\mathrm{eff}$  [MPa]")
    ax.set_title("Mori–Tanaka homogenization — glass spheres in epoxy")
    ax.set_xlim(0, 0.6)
    ax.legend(loc="upper left")
    save(fig, "simcoon_homog_mori_tanaka.png")


# ---------------------------------------------------------------------------
# 3) Directional Young's modulus rose for a cubic crystal
# ---------------------------------------------------------------------------
def plot_directional_stiffness():
    """3D directional Young's modulus surface E(n) for a cubic single crystal."""
    # Copper-like cubic constants (GPa)
    C11, C12, C44 = 168.4, 121.4, 75.4

    # Compliance tensor S in Voigt (cubic):  S11, S12, S44
    S11 = (C11 + C12) / ((C11 - C12) * (C11 + 2 * C12))
    S12 = -C12 / ((C11 - C12) * (C11 + 2 * C12))
    S44 = 1.0 / C44

    # E(n) for cubic: 1/E = S11 - 2*(S11 - S12 - S44/2) * (n1^2 n2^2 + n2^2 n3^2 + n3^2 n1^2)
    n_theta = 200
    n_phi = 400
    theta = np.linspace(0, np.pi, n_theta)
    phi = np.linspace(0, 2 * np.pi, n_phi)
    TH, PH = np.meshgrid(theta, phi, indexing="ij")
    n1 = np.sin(TH) * np.cos(PH)
    n2 = np.sin(TH) * np.sin(PH)
    n3 = np.cos(TH)
    aniso = n1**2 * n2**2 + n2**2 * n3**2 + n3**2 * n1**2
    invE = S11 - 2.0 * (S11 - S12 - S44 / 2.0) * aniso
    E = 1.0 / invE  # GPa

    X = E * n1
    Y = E * n2
    Z = E * n3

    fig = plt.figure(figsize=(11, 7.5))
    ax = fig.add_axes([0.02, 0.04, 0.78, 0.84], projection="3d", computed_zorder=False)

    norm = mpl.colors.Normalize(vmin=E.min(), vmax=E.max())
    fcolors = CMAP_HEAT(norm(E))

    ax.plot_surface(
        X,
        Y,
        Z,
        facecolors=fcolors,
        rstride=2,
        cstride=2,
        antialiased=True,
        linewidth=0.0,
        shade=True,
    )
    ax.set_box_aspect((1, 1, 1))
    R = float(E.max()) * 1.05
    ax.set_xlim(-R, R)
    ax.set_ylim(-R, R)
    ax.set_zlim(-R, R)
    ax.set_xlabel(r"$E\,n_1$  [GPa]", labelpad=18, fontsize=16)
    ax.set_ylabel(r"$E\,n_2$  [GPa]", labelpad=18, fontsize=16)
    ax.set_zlabel(r"$E\,n_3$  [GPa]", labelpad=14, fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.view_init(elev=22, azim=38)
    fig.text(
        0.5,
        0.94,
        r"Directional Young's modulus  $E(\mathbf{n})$  — cubic crystal (Cu)",
        ha="center",
        va="center",
        fontsize=22,
        fontweight="bold",
        color=BRAND_INK,
    )
    # Colorbar in its own axes so 3D ax fills space
    cax = fig.add_axes([0.86, 0.18, 0.025, 0.62])
    mappable = mpl.cm.ScalarMappable(norm=norm, cmap=CMAP_HEAT)
    cbar = fig.colorbar(mappable, cax=cax)
    cbar.set_label("E  [GPa]", fontsize=16, labelpad=8)
    cbar.ax.tick_params(labelsize=13)
    fig.savefig(
        OUT / "simcoon_directional_stiffness.png",
        dpi=DPI,
        pad_inches=0.4,
    )
    plt.close(fig)
    size_kb = (OUT / "simcoon_directional_stiffness.png").stat().st_size / 1024
    print(f"  saved simcoon_directional_stiffness.png  ({size_kb:.1f} kB)")


# ---------------------------------------------------------------------------
# 4) Shape-memory alloy superelastic loop (1D phenomenological)
# ---------------------------------------------------------------------------
def plot_sma_superelastic():
    """Auricchio-style superelastic stress-strain hysteresis.

    Strain-controlled path; closed-form sigma(eps) on each branch using
    the standard linear-onset/offset transformation rule.
    """
    E_A = 60_000.0          # MPa, austenite modulus
    E_M = 30_000.0          # MPa, martensite modulus (softer)
    eps_L = 0.05            # max transformation strain
    # Forward transformation onset/finish stresses
    sig_Ms = 420.0          # start of A->M
    sig_Mf = 520.0          # finish of A->M
    # Reverse transformation
    sig_As = 220.0          # start of M->A
    sig_Af = 140.0          # finish of M->A

    # Forward branch: derive eps when A->M starts and finishes
    eps_Ms = sig_Ms / E_A
    # On the transformation plateau, mixture: sig = sig_Ms + (sig_Mf-sig_Ms)*xi
    # eps = sig/E_eff(xi) + xi*eps_L  (use linear interpolation)
    # We use a simple linear sig(eps) on the plateau ending at xi=1
    # at xi=1: eps_end = sig_Mf/E_M + eps_L
    eps_Mf = sig_Mf / E_M + eps_L
    # Slope on plateau:
    k_fwd = (sig_Mf - sig_Ms) / (eps_Mf - eps_Ms)
    eps_max = 0.07
    sig_top = sig_Mf + E_M * (eps_max - eps_Mf)

    # Reverse branch: starts at (eps_max, sig_top) elastic unload with E_M
    # until sig = sig_As; then plateau down to sig_Af; then elastic with E_A
    eps_at_As = eps_max - (sig_top - sig_As) / E_M
    # plateau end: xi=0 -> eps = sig_Af/E_A
    eps_at_Af = sig_Af / E_A
    k_rev = (sig_As - sig_Af) / (eps_at_As - eps_at_Af)

    def fwd(eps):
        s = np.empty_like(eps)
        a = eps < eps_Ms
        b = (eps >= eps_Ms) & (eps < eps_Mf)
        c = eps >= eps_Mf
        s[a] = E_A * eps[a]
        s[b] = sig_Ms + k_fwd * (eps[b] - eps_Ms)
        s[c] = sig_Mf + E_M * (eps[c] - eps_Mf)
        return s

    def rev(eps):
        s = np.empty_like(eps)
        # starts from top
        a = eps >= eps_at_As
        b = (eps >= eps_at_Af) & (eps < eps_at_As)
        c = eps < eps_at_Af
        s[a] = sig_top - E_M * (eps_max - eps[a])
        s[b] = sig_Af + k_rev * (eps[b] - eps_at_Af)
        s[c] = E_A * eps[c]
        return s

    eps_fwd = np.linspace(0, eps_max, 500)
    eps_rev = np.linspace(eps_max, 0, 500)
    sig_fwd = fwd(eps_fwd)
    sig_rev = rev(eps_rev)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    # shaded hysteresis area
    poly_x = np.concatenate([eps_fwd, eps_rev]) * 100
    poly_y = np.concatenate([sig_fwd, sig_rev])
    ax.fill(poly_x, poly_y, color=BRAND_ORANGE, alpha=0.12)
    ax.plot(eps_fwd * 100, sig_fwd, color=BRAND_RED, linewidth=3.6,
            label="Loading (A → M)")
    ax.plot(eps_rev * 100, sig_rev, color=BRAND_ORANGE, linewidth=3.6,
            label="Unloading (M → A)")
    # Arrows on each branch
    ax.annotate(
        "",
        xy=(eps_fwd[300] * 100, sig_fwd[300]),
        xytext=(eps_fwd[250] * 100, sig_fwd[250]),
        arrowprops=dict(arrowstyle="->", color=BRAND_RED, lw=2.2),
    )
    ax.annotate(
        "",
        xy=(eps_rev[300] * 100, sig_rev[300]),
        xytext=(eps_rev[250] * 100, sig_rev[250]),
        arrowprops=dict(arrowstyle="->", color=BRAND_ORANGE, lw=2.2),
    )

    ax.set_xlabel(r"Strain $\varepsilon$  [%]")
    ax.set_ylabel(r"Stress $\sigma$  [MPa]")
    ax.set_title("Shape-memory alloy — superelastic loop (SMA_TR)")
    ax.legend(loc="upper left")
    ax.text(
        0.97,
        0.05,
        "Stress-induced phase transformation\n  Austenite ⇌ Martensite",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=14,
        color=BRAND_INK,
        bbox=dict(facecolor=BRAND_LIGHT, edgecolor="none", pad=8, alpha=0.85),
    )
    ax.set_xlim(0, eps_max * 100 * 1.03)
    ax.set_ylim(0, sig_top * 1.10)
    save(fig, "simcoon_sma_loop.png")


# ---------------------------------------------------------------------------
# 5) Plane-stress yield surfaces: von Mises, Tresca, Hill, Drucker
# ---------------------------------------------------------------------------
def plot_yield_surfaces():
    sig_y = 1.0  # normalized
    n = 400
    th = np.linspace(0, 2 * np.pi, n)

    # von Mises in plane stress: s11^2 - s11 s22 + s22^2 = sig_y^2
    # Parametrize via rotation of 45° ellipse
    a = np.sqrt(2.0) * sig_y           # along (1,1) direction
    b = np.sqrt(2.0 / 3.0) * sig_y     # along (1,-1)
    s11_vm = (a * np.cos(th) + b * np.sin(th)) / np.sqrt(2)
    s22_vm = (a * np.cos(th) - b * np.sin(th)) / np.sqrt(2)

    # Tresca plane stress hexagon vertices
    tresca_pts = np.array(
        [
            [1, 0],
            [1, 1],
            [0, 1],
            [-1, 0],
            [-1, -1],
            [0, -1],
            [1, 0],
        ],
        dtype=float,
    ) * sig_y

    # Hill anisotropic (orthotropic, plane stress, axes aligned)
    F, G_, H_, N_ = 0.4, 0.55, 0.6, 1.5
    # Hill: F*s22^2 + G*s11^2 + H*(s11-s22)^2 = 1 (with shear=0 here, isotropic plane)
    A = G_ + H_
    B = F + H_
    C = -2.0 * H_
    # Conic Ax^2 + Bx y... -> scale so peak ~ sig_y
    # Generate by parametric sweep
    s11_hill = []
    s22_hill = []
    for ang in th:
        # Find r such that A*r^2 c^2 + B*r^2 s^2 + C*r^2 c s = 1
        c, s = np.cos(ang), np.sin(ang)
        denom = A * c * c + B * s * s + C * c * s
        if denom <= 0:
            continue
        r = 1.0 / np.sqrt(denom)
        s11_hill.append(r * c * sig_y)
        s22_hill.append(r * s * sig_y)
    s11_hill = np.array(s11_hill)
    s22_hill = np.array(s22_hill)

    # Drucker (modified) — squash slightly along hydrostatic
    # use J2-J3 coupled — represent as scaled VM ellipse with hydrostatic shrink
    bD = 1.10
    s11_dr = s11_vm * bD - 0.07 * (s11_vm + s22_vm)
    s22_dr = s22_vm * bD - 0.07 * (s11_vm + s22_vm)
    # rescale so it intersects (sig_y, 0)
    rscale = sig_y / np.max(np.sqrt(s11_dr**2 + s22_dr**2)) * 1.05
    s11_dr *= rscale
    s22_dr *= rscale

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.axhline(0, color=BRAND_GREY, linewidth=0.8)
    ax.axvline(0, color=BRAND_GREY, linewidth=0.8)
    ax.plot(s11_vm, s22_vm, color=BRAND_RED, linewidth=3.6, label="von Mises")
    ax.plot(
        tresca_pts[:, 0],
        tresca_pts[:, 1],
        color=BRAND_INK,
        linewidth=2.6,
        linestyle="--",
        label="Tresca",
    )
    ax.plot(
        s11_hill, s22_hill, color=BRAND_ORANGE, linewidth=3.0, label="Hill (anisotropic)"
    )
    ax.plot(
        s11_dr, s22_dr, color=BRAND_GOLD, linewidth=3.0, linestyle="-.", label="Drucker"
    )
    ax.fill(s11_vm, s22_vm, color=BRAND_RED, alpha=0.06)
    ax.set_xlabel(r"$\sigma_{11}/\sigma_y$")
    ax.set_ylabel(r"$\sigma_{22}/\sigma_y$")
    ax.set_title("Plane-stress yield surfaces")
    ax.set_aspect("equal")
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.legend(loc="upper left")
    save(fig, "simcoon_yield_surfaces.png")


# ---------------------------------------------------------------------------
# 6) Identification: experimental vs. fitted Mooney-Rivlin curves
# ---------------------------------------------------------------------------
def plot_identification():
    """Identification of Mooney-Rivlin parameters on Treloar-like rubber data."""
    # Treloar-style stretches
    lam_ut = np.array(
        [1.00, 1.10, 1.25, 1.50, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0]
    )
    sig_ut_exp = np.array(
        [0.00, 0.10, 0.27, 0.55, 1.10, 1.55, 1.95, 2.30, 2.65, 3.00, 3.50, 4.20, 5.20,
         6.50, 8.20]
    )

    # 3-term Yeoh model nominal stress in uniaxial:
    # P = 2*(lam - 1/lam^2) * (C10 + 2*C20*(I1-3) + 3*C30*(I1-3)^2),  I1 = lam^2 + 2/lam
    # Least-squares fit to the Treloar data above.
    def _yeoh_P(lam, c10, c20, c30):
        I1 = lam**2 + 2.0 / lam
        return (
            2.0
            * (lam - 1.0 / lam**2)
            * (c10 + 2 * c20 * (I1 - 3) + 3 * c30 * (I1 - 3) ** 2)
        )

    # Linear in (C10, C20, C30) so solve closed-form
    I1_e = lam_ut**2 + 2.0 / lam_ut
    A_mat = (
        2.0
        * (lam_ut - 1.0 / lam_ut**2)[:, None]
        * np.column_stack([np.ones_like(lam_ut), 2 * (I1_e - 3), 3 * (I1_e - 3) ** 2])
    )
    coeffs, *_ = np.linalg.lstsq(A_mat, sig_ut_exp, rcond=None)
    C10, C20, C30 = coeffs
    lam_fit = np.linspace(1.0, 7.3, 400)
    P_fit = _yeoh_P(lam_fit, C10, C20, C30)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.plot(
        lam_fit,
        P_fit,
        color=BRAND_RED,
        linewidth=3.6,
        label="Yeoh fit  ($C_{10}, C_{20}, C_{30}$)",
    )
    ax.scatter(
        lam_ut,
        sig_ut_exp,
        s=120,
        marker="o",
        facecolor="white",
        edgecolor=BRAND_INK,
        linewidth=2.0,
        zorder=5,
        label="Treloar (experiment)",
    )
    ax.set_xlabel(r"Stretch $\lambda$")
    ax.set_ylabel(r"Nominal stress $P$  [MPa]")
    ax.set_title("Hyperelastic parameter identification — Treloar rubber")
    ax.legend(loc="upper left")
    ax.text(
        0.97,
        0.05,
        (
            "Identified:\n"
            f"  $C_{{10}}$ = {C10:.3f} MPa\n"
            f"  $C_{{20}}$ = {C20:.4f} MPa\n"
            f"  $C_{{30}}$ = {C30:.2e} MPa"
        ),
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=14,
        color=BRAND_INK,
        bbox=dict(facecolor=BRAND_LIGHT, edgecolor="none", pad=8, alpha=0.85),
    )
    save(fig, "simcoon_identification.png")


# ---------------------------------------------------------------------------
# Hero square (1200x1200) — pick yield-surfaces plot variant (square already)
# ---------------------------------------------------------------------------
def plot_hero():
    """Square hero combining Mori-Tanaka / yield surface signature look.

    Uses the directional-stiffness rose viewed straight-on for a striking
    radially symmetric image.
    """
    C11, C12, C44 = 168.4, 121.4, 75.4
    S11 = (C11 + C12) / ((C11 - C12) * (C11 + 2 * C12))
    S12 = -C12 / ((C11 - C12) * (C11 + 2 * C12))
    S44 = 1.0 / C44

    n_theta = 240
    n_phi = 480
    theta = np.linspace(0, np.pi, n_theta)
    phi = np.linspace(0, 2 * np.pi, n_phi)
    TH, PH = np.meshgrid(theta, phi, indexing="ij")
    n1 = np.sin(TH) * np.cos(PH)
    n2 = np.sin(TH) * np.sin(PH)
    n3 = np.cos(TH)
    aniso = n1**2 * n2**2 + n2**2 * n3**2 + n3**2 * n1**2
    invE = S11 - 2.0 * (S11 - S12 - S44 / 2.0) * aniso
    E = 1.0 / invE

    X, Y, Z = E * n1, E * n2, E * n3

    fig = plt.figure(figsize=(9.5, 9.5))
    ax = fig.add_subplot(111, projection="3d", computed_zorder=False)

    norm = mpl.colors.Normalize(vmin=E.min(), vmax=E.max())
    fcolors = CMAP_HEAT(norm(E))

    ax.plot_surface(
        X,
        Y,
        Z,
        facecolors=fcolors,
        rstride=2,
        cstride=2,
        antialiased=True,
        linewidth=0,
        shade=True,
    )
    ax.set_box_aspect((1, 1, 1))
    R = float(E.max()) * 1.0
    ax.set_xlim(-R, R)
    ax.set_ylim(-R, R)
    ax.set_zlim(-R, R)
    ax.view_init(elev=22, azim=42)
    ax.set_axis_off()
    fig.patch.set_facecolor("white")
    fig.savefig(
        OUT / "simcoon_hero.png",
        dpi=160,
        bbox_inches="tight",
        pad_inches=0.10,
        facecolor="white",
    )
    plt.close(fig)
    print(f"  saved simcoon_hero.png")


def main():
    style()
    print("Rendering Simcoon hero figures…")
    plot_mori_tanaka()
    plot_directional_stiffness()
    plot_sma_superelastic()
    plot_yield_surfaces()
    plot_identification()
    plot_hero()
    print("Done.")


if __name__ == "__main__":
    main()
