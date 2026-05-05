"""
PersonaPath - Unified Gradio Dashboard
Phases 1 & 2: Literacy Coach + Presentation Pro

Clean, minimal UI matching the target design (light theme, sidebar, card layout)
"""

import gradio as gr
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import sys
import os
from PIL import Image
from io import BytesIO
from starlette.templating import Jinja2Templates

# ============================================================================
# STARLETTE 1.0 COMPATIBILITY PATCH
# ============================================================================
# Gradio 4.x calls TemplateResponse as:
#   TemplateResponse(name, context, ...)
# but Starlette 1.0 expects:
#   TemplateResponse(request, name, context, ...)
# This shim rewrites old-style calls so homepage rendering doesn't crash.
_template_response_orig = Jinja2Templates.TemplateResponse

if not getattr(Jinja2Templates.TemplateResponse, "_personapath_compat_patch", False):
    def _template_response_compat(self, *args, **kwargs):
        # Old Gradio call style
        if len(args) >= 2 and isinstance(args[0], str) and isinstance(args[1], dict):
            name = args[0]
            context = args[1]
            request = kwargs.pop("request", None) or context.get("request")
            if request is None:
                raise TypeError("TemplateResponse compatibility patch: request missing from context.")
            remaining = args[2:]
            return _template_response_orig(self, request, name, context, *remaining, **kwargs)
        # New style / default path
        return _template_response_orig(self, *args, **kwargs)

    _template_response_compat._personapath_compat_patch = True  # type: ignore[attr-defined]
    Jinja2Templates.TemplateResponse = _template_response_compat

# Add services to path
sys.path.insert(0, str(Path(__file__).parent))

from services import (
    get_config,
    BackendMode,
    Phase1Result,
    Phase2Result,
)

CONFIG = get_config(BackendMode.MOCK)

# ============================================================================
# CUSTOM CSS — Clean, light, professional UI
# ============================================================================

CUSTOM_CSS = """
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

/* ── Reset & Base ── */
* { box-sizing: border-box; }

body, .gradio-container {
    font-family: 'DM Sans', sans-serif !important;
    background: #f5f6fa !important;
    color: #1a1d2e !important;
}

/* Hide Gradio footer */
footer { display: none !important; }

/* ── Top Navbar ── */
.navbar {
    background: #ffffff;
    border-bottom: 1px solid #e8eaf0;
    padding: 0 32px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
}

.navbar-brand {
    font-family: 'DM Serif Display', serif !important;
    font-size: 22px !important;
    font-weight: 400 !important;
    color: #1a1d2e !important;
    letter-spacing: -0.3px;
}

.navbar-actions {
    display: flex;
    gap: 16px;
    align-items: center;
    color: #6b7280;
    font-size: 18px;
}

/* ── Layout: Sidebar + Main ── */
.layout-wrapper {
    display: flex;
    min-height: calc(100vh - 64px);
}

.sidebar {
    width: 220px;
    background: #ffffff;
    border-right: 1px solid #e8eaf0;
    padding: 24px 0;
    flex-shrink: 0;
}

.sidebar-section-label {
    padding: 8px 20px 4px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #9ca3af;
}

.sidebar-item {
    padding: 10px 20px;
    font-size: 13.5px;
    font-weight: 400;
    color: #6b7280;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
    border-left: 3px solid transparent;
    transition: all 0.15s;
}

.sidebar-item:hover { background: #f5f6fa; color: #1a1d2e; }
.sidebar-item.active {
    color: #1e40af;
    font-weight: 500;
    border-left-color: #1e40af;
    background: #eff6ff;
}

/* ── Main Content ── */
.main-content {
    flex: 1;
    padding: 32px;
    overflow-y: auto;
}

/* ── Phase Header ── */
.phase-header {
    margin-bottom: 24px;
}

.phase-title {
    font-size: 26px !important;
    font-weight: 600 !important;
    color: #1a1d2e !important;
    margin: 0 0 4px 0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

.phase-subtitle {
    font-size: 13.5px !important;
    color: #6b7280 !important;
    margin: 0 !important;
}

/* ── Cards ── */
.card {
    background: #ffffff;
    border: 1px solid #e8eaf0;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
}

.card-title {
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px;
    color: #1a1d2e !important;
    margin: 0 0 16px 0 !important;
    text-transform: uppercase;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Gradio component overrides ── */
.gr-block, .gr-box { background: transparent !important; border: none !important; box-shadow: none !important; }

/* Inputs */
textarea, input[type="text"], input[type="number"] {
    border: 1px solid #e8eaf0 !important;
    border-radius: 8px !important;
    background: #fafafa !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    color: #1a1d2e !important;
    transition: border-color 0.15s !important;
}

textarea:focus, input:focus {
    border-color: #1e40af !important;
    background: #ffffff !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.08) !important;
}

/* Labels */
label span {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    color: #6b7280 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.6px !important;
}

/* Buttons */
.btn-primary {
    background: #1e3a8a !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    width: 100% !important;
    transition: background 0.15s !important;
}
.btn-primary:hover { background: #1e40af !important; }

.btn-secondary {
    background: #ffffff !important;
    color: #1a1d2e !important;
    border: 1px solid #e8eaf0 !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13.5px !important;
    font-weight: 400 !important;
    cursor: pointer !important;
    transition: border-color 0.15s !important;
}
.btn-secondary:hover { border-color: #1e40af !important; color: #1e40af !important; }

/* Gradio button elements */
button.primary {
    background: #1e3a8a !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    height: 44px !important;
    transition: background 0.15s !important;
}
button.primary:hover { background: #1e40af !important; }

button.secondary {
    background: #ffffff !important;
    color: #374151 !important;
    border: 1px solid #e8eaf0 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13.5px !important;
    height: 40px !important;
}

/* ── Tabs ── */
.tabs { background: transparent !important; border: none !important; }
.tab-nav { border-bottom: 1px solid #e8eaf0 !important; margin-bottom: 24px !important; }
.tab-nav button {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 10px 20px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 400 !important;
    color: #6b7280 !important;
    border-radius: 0 !important;
    margin-bottom: -1px !important;
}
.tab-nav button.selected {
    color: #1e40af !important;
    border-bottom-color: #1e40af !important;
    font-weight: 500 !important;
}

/* ── Metric cards ── */
.metric-card {
    background: #ffffff;
    border: 1px solid #e8eaf0;
    border-radius: 10px;
    padding: 18px 20px;
    text-align: left;
}

.metric-value {
    font-size: 32px !important;
    font-weight: 600 !important;
    color: #1a1d2e !important;
    line-height: 1 !important;
    margin: 4px 0 2px !important;
}

.metric-label {
    font-size: 11px !important;
    font-weight: 500 !important;
    color: #9ca3af !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}

/* ── Active Session badge ── */
.active-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 12px;
    font-weight: 500;
    color: #15803d;
}

/* ── Confidence Ring container ── */
.confidence-ring-wrapper {
    display: flex;
    justify-content: center;
    padding: 16px 0;
}

/* ── Progress bar ── */
.gr-slider input[type=range] { accent-color: #1e3a8a !important; }

/* ── Plots ── */
.gr-plot { border-radius: 8px !important; border: 1px solid #e8eaf0 !important; overflow: hidden !important; }

/* ── Coaching corner ── */
.coaching-card {
    background: #f8faff;
    border: 1px solid #dbeafe;
    border-radius: 10px;
    padding: 16px;
}

/* ── Word-level alignment chip ── */
.word-chip-green { color: #15803d; font-weight: 600; }
.word-chip-orange { color: #d97706; font-weight: 600; }
.word-chip-red { color: #dc2626; font-weight: 600; text-decoration: underline; text-decoration-style: wavy; }

/* ── Section labels ── */
.section-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #9ca3af;
    margin-bottom: 10px;
}

/* Number inputs clean */
input[type="number"] { text-align: center !important; }

/* Remove default gradio panel borders */
.gr-panel { border: none !important; box-shadow: none !important; background: transparent !important; }

/* Audio widget */
.gr-audio { border: 2px dashed #e8eaf0 !important; border-radius: 10px !important; background: #fafafa !important; }

/* Video widget */
.gr-video { border: 2px dashed #e8eaf0 !important; border-radius: 10px !important; background: #111827 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 3px; }

/* Remove Gradio's default padding on blocks */
.gradio-container > .main { padding: 0 !important; }
.contain { max-width: 100% !important; }
"""

# ============================================================================
# VISUALIZATION UTILITIES — clean, white-background plots
# ============================================================================

def _apply_clean_style(ax, fig):
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f8faff')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#e8eaf0')
    ax.spines['bottom'].set_color('#e8eaf0')
    ax.tick_params(colors='#6b7280', labelsize=10)
    ax.xaxis.label.set_color('#6b7280')
    ax.yaxis.label.set_color('#6b7280')
    ax.title.set_color('#1a1d2e')

def fig_to_pil(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100, facecolor='#ffffff')
    buf.seek(0)
    img = Image.open(buf).convert('RGB')
    plt.close(fig)
    return img

def create_waveform_plot(audio_path=None):
    fig, ax = plt.subplots(figsize=(8, 2.5))
    _apply_clean_style(ax, fig)
    if audio_path:
        x = np.linspace(0, 12, 300)
        np.random.seed(42)
        y = np.sin(2 * np.pi * 1.5 * x) * np.exp(-0.05 * x) + np.random.randn(300) * 0.15
        ax.fill_between(x, y, alpha=0.3, color='#1e40af')
        ax.plot(x, y, color='#1e40af', linewidth=1.2)
        ax.axhline(0, color='#e8eaf0', linewidth=0.8)
    else:
        ax.text(0.5, 0.5, 'Record or upload audio to see waveform',
                ha='center', va='center', color='#9ca3af', fontsize=12,
                transform=ax.transAxes)
    ax.set_yticks([])
    ax.set_xlabel('Time (seconds)', fontsize=10)
    ax.set_title('')
    fig.tight_layout(pad=1.5)
    return fig_to_pil(fig)

def create_vocal_energy_plot(vocal_dynamics):
    fig, ax = plt.subplots(figsize=(8, 3.5))
    _apply_clean_style(ax, fig)

    if not vocal_dynamics:
        ax.text(0.5, 0.5, 'Upload video to see vocal energy dynamics',
                ha='center', va='center', color='#9ca3af', fontsize=12,
                transform=ax.transAxes)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        fig.tight_layout(pad=1.5)
        return fig_to_pil(fig)

    sections_data = {}
    for item in vocal_dynamics:
        sections_data.setdefault(item.section, []).append(item.rms_energy)

    section_colors = {
        'INTRODUCTION': '#93c5fd',
        'CORE_ARGUMENT': '#1e40af',
        'CONCLUSION': '#60a5fa',
    }
    section_order = ['INTRODUCTION', 'CORE_ARGUMENT', 'CONCLUSION']
    x = 0
    x_ticks, x_labels = [], []
    section_starts = {}

    for section in section_order:
        if section not in sections_data:
            continue
        energies = sections_data[section]
        section_starts[section] = x + len(energies) / 2
        for energy in energies:
            ax.bar(x, energy, color=section_colors.get(section, '#1e40af'),
                   width=0.75, edgecolor='none')
            x += 1
        x += 0.8  # gap between sections

    ax.axhline(0.5, color='#e8eaf0', linewidth=1, linestyle='--')
    ax.set_ylim(0, 1)
    ax.set_xlim(-0.5, x)
    ax.set_xticks([section_starts[s] for s in section_order if s in section_starts])
    ax.set_xticklabels([s.replace('_', ' ').title() for s in section_order if s in section_starts],
                       fontsize=9, color='#9ca3af')
    ax.set_ylabel('Vocal Energy (RMS)', fontsize=10)
    ax.set_title('Vocal Energy Dynamics', fontsize=12, fontweight='600', color='#1a1d2e', pad=10)
    ax.text(1, 1.02, 'RNN/LSTM Sequence Analysis', transform=ax.transAxes,
            ha='right', va='bottom', fontsize=9, color='#1e40af', style='italic')
    fig.tight_layout(pad=1.5)
    return fig_to_pil(fig)

def create_emotion_timeline_plot(emotions):
    fig, ax = plt.subplots(figsize=(8, 3))
    _apply_clean_style(ax, fig)

    if not emotions:
        ax.text(0.5, 0.5, 'Upload video to see emotion distribution',
                ha='center', va='center', color='#9ca3af', fontsize=12,
                transform=ax.transAxes)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        fig.tight_layout(pad=1.5)
        return fig_to_pil(fig)

    emotion_counts = {}
    for e in emotions:
        name = e.emotion.value
        emotion_counts[name] = emotion_counts.get(name, 0) + 1

    palette = ['#1e40af', '#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe', '#eff6ff']
    sorted_items = sorted(emotion_counts.items(), key=lambda x: -x[1])
    names, counts = zip(*sorted_items) if sorted_items else ([], [])
    bars = ax.bar(names, counts, color=palette[:len(names)], edgecolor='none', width=0.6)

    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                str(count), ha='center', va='bottom', fontsize=10, color='#374151', fontweight='500')

    ax.set_ylabel('Frequency', fontsize=10)
    ax.set_title('Emotion Distribution', fontsize=12, fontweight='600', color='#1a1d2e', pad=10)
    ax.tick_params(axis='x', rotation=30)
    fig.tight_layout(pad=1.5)
    return fig_to_pil(fig)

def create_confidence_ring_plot(score: float = 0.0):
    """Circular progress ring for confidence score"""
    fig, ax = plt.subplots(figsize=(3, 3), subplot_kw=dict(aspect='equal'))
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    size = 0.28
    # Background ring
    wedge_bg = plt.matplotlib.patches.Wedge(
        (0.5, 0.5), 0.42, 0, 360, width=size,
        transform=ax.transAxes, facecolor='#e8eaf0', edgecolor='none'
    )
    ax.add_patch(wedge_bg)

    # Foreground ring
    if score > 0:
        wedge_fg = plt.matplotlib.patches.Wedge(
            (0.5, 0.5), 0.42, 90, 90 - score * 360, width=size,
            transform=ax.transAxes, facecolor='#15803d', edgecolor='none'
        )
        ax.add_patch(wedge_fg)

    ax.text(0.5, 0.55, f'{int(score * 100)}%', ha='center', va='center',
            fontsize=22, fontweight='600', color='#1a1d2e', transform=ax.transAxes)
    ax.text(0.5, 0.38, 'SCORE', ha='center', va='center',
            fontsize=9, color='#9ca3af', transform=ax.transAxes,
            fontfamily='DM Sans', fontweight='500')
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    fig.tight_layout(pad=0)
    return fig_to_pil(fig)

def create_alignment_html(word_alignments) -> str:
    html = "<div style='font-family: DM Sans, sans-serif; font-size: 28px; font-weight: 600; line-height: 1.6; padding: 12px 0;'>"
    for item in word_alignments:
        if item.confidence > 0.9:
            style = "color: #15803d;"
        elif item.confidence > 0.8:
            style = "color: #1a1d2e;"
        else:
            style = "color: #dc2626; text-decoration: underline wavy #dc2626;"
        html += f"<span style='{style} margin-right: 10px;'>{item.word}</span>"
    html += "</div>"
    return html

# ============================================================================
# SIDEBAR HTML
# ============================================================================

SIDEBAR_HTML = """
<div style="
    width: 220px;
    background: #ffffff;
    border-right: 1px solid #e8eaf0;
    min-height: 100vh;
    padding: 24px 0;
    font-family: 'DM Sans', sans-serif;
">
    <div style="padding: 8px 20px 4px; font-size: 10px; font-weight: 600;
                letter-spacing: 1.2px; text-transform: uppercase; color: #9ca3af; margin-bottom: 4px;">
        Faculty Context
    </div>
    <div style="padding: 4px 20px 12px; font-size: 10px; color: #bbb; letter-spacing: 0.5px;
                text-transform: uppercase;">Institutional View</div>

    <div style="padding: 10px 20px; font-size: 13.5px; color: #1e40af; font-weight: 500;
                border-left: 3px solid #1e40af; background: #eff6ff; display: flex;
                align-items: center; gap: 8px;">
        <span>&#9998;</span> Academic Overview
    </div>
    <div style="padding: 10px 20px; font-size: 13.5px; color: #6b7280; display: flex;
                align-items: center; gap: 8px; border-left: 3px solid transparent;">
        <span>&#128101;</span> Faculty Portal
    </div>
    <div style="padding: 10px 20px; font-size: 13.5px; color: #6b7280; display: flex;
                align-items: center; gap: 8px; border-left: 3px solid transparent;">
        <span>&#128200;</span> Student Progress
    </div>
    <div style="padding: 10px 20px; font-size: 13.5px; color: #6b7280; display: flex;
                align-items: center; gap: 8px; border-left: 3px solid transparent;">
        <span>&#128218;</span> Curriculum Insights
    </div>

    <div style="position: absolute; bottom: 32px; left: 0; right: 0; padding: 0 16px;">
        <button style="width: 100%; background: #1e3a8a; color: #fff; border: none;
                       border-radius: 8px; padding: 11px 0; font-family: 'DM Sans', sans-serif;
                       font-size: 13.5px; font-weight: 500; cursor: pointer;">
            Generate Report
        </button>
    </div>
</div>
"""

NAVBAR_HTML = """
<div style="
    background: #ffffff;
    border-bottom: 1px solid #e8eaf0;
    padding: 0 32px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: 'DM Sans', sans-serif;
">
    <span style="font-family: 'DM Serif Display', serif; font-size: 22px; color: #1a1d2e; letter-spacing: -0.3px;">
        PersonaPath
    </span>
    <div style="display: flex; gap: 24px; align-items: center;">
        <span style="font-size: 14px; color: #1a1d2e; font-weight: 500; border-bottom: 2px solid #1e40af; padding-bottom: 4px;">Phase 1</span>
        <span style="font-size: 14px; color: #6b7280;">Phase 2</span>
        <span style="color: #9ca3af; font-size: 18px; cursor: pointer;">&#128276;</span>
        <span style="color: #9ca3af; font-size: 18px; cursor: pointer;">&#9881;</span>
        <div style="width: 32px; height: 32px; background: #1e3a8a; border-radius: 50%;
                    display: flex; align-items: center; justify-content: center;
                    color: white; font-size: 14px; font-weight: 600; cursor: pointer;">P</div>
    </div>
</div>
"""

# ============================================================================
# EVENT HANDLERS
# ============================================================================

def handle_phase1_process(audio_file, passage_text):
    if audio_file is None:
        return (
            "Please upload or record audio to begin.",
            0, 0, 0,
            "0 of 4 sessions completed today",
            "<p style='font-family: DM Sans, sans-serif; color:#9ca3af; font-size:14px;'>Awaiting audio input...</p>",
            create_waveform_plot(None)
        )
    try:
        result: Phase1Result = CONFIG.phase1_backend.process_audio(audio_file, passage_text)
        alignment_html = create_alignment_html(result.word_alignments)
        waveform = create_waveform_plot(audio_file)
        return (
            result.feedback,
            result.words_per_minute,
            result.hesitations,
            result.session_progress * 100,
            f"{int(result.session_progress * 4)} of 4 sessions completed today",
            alignment_html,
            waveform
        )
    except Exception as e:
        return (
            f"Error: {str(e)}", 0, 0, 0, "Error",
            f"<p style='color:#dc2626;'>Error: {str(e)}</p>",
            create_waveform_plot(None)
        )

def handle_phase2_process(video_file):
    if video_file is None:
        return (
            create_confidence_ring_plot(0),
            0, 0, 0,
            "",
            0, 0,
            "Ready for analysis",
            0,
            create_vocal_energy_plot([]),
            create_emotion_timeline_plot([])
        )
    try:
        result: Phase2Result = CONFIG.phase2_backend.process_video(video_file)
        ring = create_confidence_ring_plot(result.confidence_score)
        insights_text = "\n\n".join(result.insights)
        energy_plot = create_vocal_energy_plot(result.vocal_energy_dynamics)
        emotion_plot = create_emotion_timeline_plot(result.emotion_predictions)
        return (
            ring,
            result.communication_metrics.filter_words["um"],
            result.communication_metrics.filter_words["uh"],
            result.communication_metrics.filter_words["like"],
            insights_text,
            result.communication_metrics.pitch_variance_percent,
            result.communication_metrics.speaking_pace_wpm,
            "Analysis Complete",
            85,
            energy_plot,
            emotion_plot
        )
    except Exception as e:
        return (
            create_confidence_ring_plot(0),
            0, 0, 0,
            f"Error: {str(e)}",
            0, 0,
            f"Error: {str(e)}",
            0,
            create_vocal_energy_plot([]),
            create_emotion_timeline_plot([])
        )

# ============================================================================
# APP
# ============================================================================

def create_app() -> gr.Blocks:
    with gr.Blocks(
        title="PersonaPath",
        theme=gr.themes.Base(
            primary_hue=gr.themes.colors.blue,
            font=[gr.themes.GoogleFont("DM Sans"), "sans-serif"],
        ),
        css=CUSTOM_CSS
    ) as app:

        # Navbar
        gr.HTML(NAVBAR_HTML)

        # Main layout: sidebar + content
        with gr.Row(equal_height=True):
            # Sidebar
            gr.HTML(SIDEBAR_HTML)

            # Main content
            with gr.Column(scale=1, elem_classes=["main-content"]):

                with gr.Tabs() as tabs:

                    # ── PHASE 1 ──────────────────────────────────────────
                    with gr.TabItem("Phase 1: Literacy Coach"):

                        gr.HTML("""
                        <div style="margin-bottom: 24px;">
                            <h1 style="font-family: DM Sans, sans-serif; font-size: 26px; font-weight: 600;
                                       color: #1a1d2e; margin: 0 0 4px;">Phase 1: Literacy Coach</h1>
                            <p style="font-family: DM Sans, sans-serif; font-size: 13.5px; color: #6b7280; margin: 0;">
                                Speech-aligned literacy assessment with real-time feedback.</p>
                        </div>
                        """)

                        with gr.Row(equal_height=False):
                            # Left column
                            with gr.Column(scale=3):
                                # Reading passage card
                                gr.HTML('<div style="font-family: DM Sans, sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #9ca3af; margin-bottom: 8px;">Reading Passage</div>')

                                with gr.Group(elem_classes=["card"]):
                                    passage = gr.Textbox(
                                        value="The elephant sat quietly by the river bank",
                                        label="",
                                        lines=2,
                                        interactive=True,
                                        placeholder="Enter reading passage..."
                                    )
                                    gr.HTML("""
                                    <div style="display: flex; align-items: center; gap: 6px; margin-top: 8px;">
                                        <span style="width: 8px; height: 8px; background: #3b82f6; border-radius: 50%; display: inline-block;"></span>
                                        <span style="font-family: DM Sans, sans-serif; font-size: 11px; color: #6b7280;
                                                     letter-spacing: 0.5px; text-transform: uppercase;">
                                            Transformer-based Alignment (WAV2VEC 2.0)
                                        </span>
                                        <span style="margin-left: auto; background: #eff6ff; color: #1e40af; font-size: 10px;
                                                     padding: 2px 8px; border-radius: 4px; font-weight: 500;">LEVEL: PRIMARY</span>
                                    </div>
                                    """)

                                # Recording card
                                gr.HTML('<div style="font-family: DM Sans, sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #9ca3af; margin: 20px 0 8px;">Recording</div>')
                                with gr.Group(elem_classes=["card"]):
                                    audio = gr.Audio(
                                        label="",
                                        type="filepath",
                                        sources=["microphone", "upload"]
                                    )

                                # Waveform
                                gr.HTML('<div style="font-family: DM Sans, sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #9ca3af; margin: 20px 0 8px;">Waveform</div>')
                                with gr.Group(elem_classes=["card"]):
                                    waveform_plot = gr.Image(label="", show_label=False, interactive=False)

                            # Right column
                            with gr.Column(scale=2):
                                # Coaching Corner
                                gr.HTML("""
                                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                                    <div style="width: 36px; height: 36px; border-radius: 50%; background: #1e3a8a;
                                                display: flex; align-items: center; justify-content: center;
                                                color: white; font-size: 14px; font-weight: 600;">C</div>
                                    <div>
                                        <div style="font-family: DM Sans, sans-serif; font-size: 14px; font-weight: 600; color: #1a1d2e;">Claude's Coaching Corner</div>
                                        <div style="font-family: DM Sans, sans-serif; font-size: 11px; color: #9ca3af;">Active Feedback</div>
                                    </div>
                                </div>
                                """)

                                with gr.Group(elem_classes=["card"]):
                                    coaching_feedback = gr.Textbox(
                                        label="",
                                        lines=4,
                                        interactive=False,
                                        placeholder="Feedback will appear here after processing..."
                                    )

                                # Metrics
                                gr.HTML('<div style="font-family: DM Sans, sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #9ca3af; margin: 20px 0 12px;">Metrics</div>')
                                with gr.Row():
                                    with gr.Group(elem_classes=["card"]):
                                        wpm_metric = gr.Number(label="Words Per Minute", value=0, interactive=False)
                                    with gr.Group(elem_classes=["card"]):
                                        hesitation_metric = gr.Number(label="Hesitations", value=0, interactive=False)

                                # Progress
                                gr.HTML('<div style="font-family: DM Sans, sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #9ca3af; margin: 20px 0 12px;">Daily Progress</div>')
                                with gr.Group(elem_classes=["card"]):
                                    progress_slider = gr.Slider(minimum=0, maximum=100, value=0, label="", interactive=False)
                                    progress_text = gr.Textbox(
                                        value="0 of 4 sessions completed today",
                                        label="",
                                        interactive=False,
                                        show_label=False
                                    )

                                # Word alignment
                                gr.HTML('<div style="font-family: DM Sans, sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #9ca3af; margin: 20px 0 12px;">Word-Level Alignment</div>')
                                with gr.Group(elem_classes=["card"]):
                                    alignment_html = gr.HTML(
                                        value="<p style='font-family: DM Sans, sans-serif; color: #9ca3af; font-size: 14px;'>Awaiting audio processing...</p>"
                                    )

                        with gr.Row():
                            process_btn1 = gr.Button("Process Audio & Generate Feedback", variant="primary", size="lg")
                        with gr.Row():
                            gr.Button("Generate Report", variant="secondary")

                        process_btn1.click(
                            fn=handle_phase1_process,
                            inputs=[audio, passage],
                            outputs=[coaching_feedback, wpm_metric, hesitation_metric,
                                     progress_slider, progress_text, alignment_html, waveform_plot],
                            api_name=False
                        )

                    # ── PHASE 2 ──────────────────────────────────────────
                    with gr.TabItem("Phase 2: Presentation Pro"):

                        with gr.Row():
                            with gr.Column(scale=5):
                                gr.HTML("""
                                <div style="margin-bottom: 24px;">
                                    <h1 style="font-family: DM Sans, sans-serif; font-size: 26px; font-weight: 600;
                                               color: #1a1d2e; margin: 0 0 4px;">Phase 2: Presentation Pro</h1>
                                    <p style="font-family: DM Sans, sans-serif; font-size: 13.5px; color: #6b7280; margin: 0;">
                                        Advanced AI performance analysis for higher-level communication skills.</p>
                                </div>
                                """)
                            with gr.Column(scale=1):
                                gr.HTML("""
                                <div style="text-align: right; padding-top: 8px;">
                                    <span style="display: inline-flex; align-items: center; gap: 6px;
                                                 background: #f0fdf4; border: 1px solid #bbf7d0;
                                                 border-radius: 20px; padding: 5px 14px;
                                                 font-family: DM Sans, sans-serif; font-size: 12px;
                                                 font-weight: 500; color: #15803d;">
                                        <span style="width: 7px; height: 7px; background: #15803d;
                                                     border-radius: 50; display: inline-block;"></span>
                                        ACTIVE SESSION
                                    </span>
                                </div>
                                """)

                        with gr.Row(equal_height=False):
                            # Left: video + charts
                            with gr.Column(scale=3):
                                gr.HTML('<div style="font-family: DM Sans, sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #9ca3af; margin-bottom: 8px;">Video Player</div>')
                                with gr.Group(elem_classes=["card"]):
                                    video = gr.Video(label="", format="mp4")

                                # Progress
                                gr.HTML('<div style="font-family: DM Sans, sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #9ca3af; margin: 20px 0 8px;">Analysis Progress</div>')
                                with gr.Group(elem_classes=["card"]):
                                    progress_bar = gr.Slider(minimum=0, maximum=100, value=0, label="", interactive=False)
                                    with gr.Row():
                                        analysis_status = gr.Textbox(
                                            value="FRAME EXTRACTION & MODEL INFERENCE",
                                            label="",
                                            interactive=False,
                                            show_label=False
                                        )

                                # Charts
                                gr.HTML('<div style="font-family: DM Sans, sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #9ca3af; margin: 20px 0 8px;">Vocal Energy Dynamics</div>')
                                with gr.Group(elem_classes=["card"]):
                                    energy_plot = gr.Image(label="", show_label=False, interactive=False)

                                gr.HTML('<div style="font-family: DM Sans, sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #9ca3af; margin: 20px 0 8px;">Emotion Distribution</div>')
                                with gr.Group(elem_classes=["card"]):
                                    emotion_plot = gr.Image(label="", show_label=False, interactive=False)

                            # Right: metrics
                            with gr.Column(scale=2):
                                # Confidence ring
                                gr.HTML('<div style="font-family: DM Sans, sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #9ca3af; margin-bottom: 12px;">Confidence Ring (CNN)</div>')
                                with gr.Group(elem_classes=["card"]):
                                    confidence_ring = gr.Image(label="", show_label=False, interactive=False, height=200)
                                    gr.HTML('<div style="text-align: center; font-family: DM Sans, sans-serif; font-size: 11px; color: #9ca3af; margin-top: 8px; letter-spacing: 0.5px;">CNN Inference (MobileNetV2)</div>')

                                # Filler words
                                gr.HTML('<div style="font-family: DM Sans, sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #9ca3af; margin: 20px 0 12px;">Filler Word Counter</div>')
                                with gr.Row():
                                    with gr.Group(elem_classes=["card"]):
                                        um_count = gr.Number(label="Um", value=0, interactive=False)
                                    with gr.Group(elem_classes=["card"]):
                                        uh_count = gr.Number(label="Uh", value=0, interactive=False)
                                    with gr.Group(elem_classes=["card"]):
                                        like_count = gr.Number(label="Like", value=0, interactive=False)

                                # Insights
                                gr.HTML('<div style="font-family: DM Sans, sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #9ca3af; margin: 20px 0 12px;">Presentation Insights</div>')
                                with gr.Group(elem_classes=["card"]):
                                    insights = gr.Textbox(
                                        label="",
                                        lines=6,
                                        interactive=False,
                                        placeholder="Insights will appear after analysis..."
                                    )

                                # Speaking metrics
                                gr.HTML('<div style="font-family: DM Sans, sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #9ca3af; margin: 20px 0 12px;">Speaking Metrics</div>')
                                with gr.Row():
                                    with gr.Group(elem_classes=["card"]):
                                        pitch_var = gr.Number(label="Pitch Variance (%)", value=0, interactive=False)
                                    with gr.Group(elem_classes=["card"]):
                                        pace_wpm = gr.Number(label="Speaking Pace (WPM)", value=0, interactive=False)

                        with gr.Row():
                            process_btn2 = gr.Button("Analyze Presentation", variant="primary", size="lg")
                        with gr.Row():
                            gr.Button("Generate Report", variant="secondary")

                        process_btn2.click(
                            fn=handle_phase2_process,
                            inputs=[video],
                            outputs=[
                                confidence_ring,
                                um_count, uh_count, like_count,
                                insights,
                                pitch_var, pace_wpm,
                                analysis_status,
                                progress_bar,
                                energy_plot,
                                emotion_plot
                            ],
                            api_name=False
                        )

    return app


if __name__ == "__main__":
    app = create_app()
    preferred_port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    host = os.getenv("GRADIO_SERVER_NAME", "127.0.0.1")
    print("Starting PersonaPath Dashboard...")
    print(f"Access at: http://{host}:{preferred_port}")
    try:
        app.launch(
            share=False,
            server_name=host,
            server_port=preferred_port,
            show_error=True
        )
    except OSError as exc:
        if "Cannot find empty port" not in str(exc):
            raise
        print("Requested port is busy; retrying on an auto-selected free port...")
        app.launch(
            share=False,
            server_name=host,
            server_port=None,
            show_error=True
        )
    except ValueError as exc:
        if "localhost is not accessible" not in str(exc):
            raise
        print("Localhost check failed; retrying with share=True...")
        app.launch(
            share=True,
            server_name="0.0.0.0",
            server_port=preferred_port,
            show_error=True
        )
