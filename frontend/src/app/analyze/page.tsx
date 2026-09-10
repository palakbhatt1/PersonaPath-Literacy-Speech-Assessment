'use client';
import React, { useState, useRef } from 'react';

export default function Phase2() {
  return (
    <div className="flex-1 w-full h-full">
      
{/*  Top Navigation Bar  */}
<header className="bg-white dark:bg-slate-900 font-['Lexend'] font-medium text-blue-800 dark:text-blue-400 docked full-width top-0 border-b border-slate-200 dark:border-slate-800 flat no shadows flex justify-between items-center w-full px-6 py-4 max-w-full mx-auto fixed z-50">
<div className="text-2xl font-black text-blue-800 dark:text-blue-400">PersonaPath</div>
<nav className="flex gap-8">
<a className="text-slate-500 dark:text-slate-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors pb-1" href="#">Phase 1</a>
<a className="text-blue-800 dark:text-blue-400 border-b-2 border-blue-800 dark:border-blue-400 pb-1 hover:text-blue-700 dark:hover:text-blue-300 transition-colors" href="#">Phase 2</a>
</nav>
<div className="flex items-center gap-4">
<button className="scale-95 active:transition-transform text-slate-500 material-symbols-outlined" data-icon="notifications">notifications</button>
<button className="scale-95 active:transition-transform text-slate-500 material-symbols-outlined" data-icon="settings">settings</button>
<div className="w-8 h-8 rounded-full overflow-hidden border border-slate-200">
<img alt="User Avatar" data-alt="professional portrait of an educator in a clean modern office setting" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBI8bHbKdT2Cgc43EJDBieUp26aYrlk_2Re6oB7PEJyXIco85CGH0pZflwGpgpsj3dyNywIUOOTuxXquiqYII1Ce4eOvOu0CC3FR26vNjAjKrdwbsAYoimGin9QPHHR_XkdIEI4VHgZ09b_wjQCGOgRI2jaGbLkqxQWOPjy2GQbFvwVgOK2bZuzLdK2coP9N4p035nfTbqwXSobT5ZA2gllIxGEQJ0z0heFaoju3I4wCb1S8BeoWAEMfCpAbTykZszskzhWRm48y1Y"/>
</div>
</div>
</header>
{/*  Side Navigation  */}
<aside className="bg-slate-50 dark:bg-slate-950 font-['Lexend'] text-sm text-blue-800 dark:text-blue-400 docked left-0 h-full w-64 border-r border-slate-200 dark:border-slate-800 flat no shadows fixed left-0 top-0 h-screen flex flex-col p-4 z-40 mt-[72px]">
<div className="mb-8 px-2">
<h2 className="text-lg font-bold text-blue-800 dark:text-blue-400">Faculty Context</h2>
<p className="text-xs text-slate-500">Institutional View</p>
</div>
<nav className="space-y-1 flex-1">
<a className="flex items-center gap-3 px-3 py-2 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800 transition-all duration-200 ease-in-out rounded-lg" href="#">
<span className="material-symbols-outlined" data-icon="school">school</span>
                Academic Overview
            </a>
<a className="flex items-center gap-3 px-3 py-2 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800 transition-all duration-200 ease-in-out rounded-lg" href="#">
<span className="material-symbols-outlined" data-icon="groups">groups</span>
                Faculty Portal
            </a>
<a className="flex items-center gap-3 px-3 py-2 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 font-bold rounded-lg transition-all duration-200 ease-in-out" href="#">
<span className="material-symbols-outlined" data-icon="trending_up">trending_up</span>
                Student Progress
            </a>
<a className="flex items-center gap-3 px-3 py-2 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800 transition-all duration-200 ease-in-out rounded-lg" href="#">
<span className="material-symbols-outlined" data-icon="auto_stories">auto_stories</span>
                Curriculum Insights
            </a>
</nav>
<button className="mt-auto w-full bg-primary text-on-primary py-3 rounded-xl font-bold transition-all duration-200 hover:bg-primary-container">
            Generate Report
        </button>
</aside>
{/*  Main Content Canvas  */}
<main className="ml-64 pt-[88px] p-8 max-w-[1400px]">
<div className="flex justify-between items-end mb-8">
<div>
<h1 className="font-display-learning text-display-learning text-on-background mb-2">Phase 2: Presentation Pro</h1>
<p className="text-on-surface-variant font-body-coaching opacity-70">Advanced AI performance analysis for higher-level communication skills.</p>
</div>
<div className="bg-surface-container-high rounded-full px-4 py-2 flex items-center gap-2">
<span className="w-2 h-2 rounded-full bg-secondary"></span>
<span className="text-data-header font-data-header text-secondary uppercase">Active Session</span>
</div>
</div>
{/*  Dashboard Grid  */}
<div className="grid grid-cols-12 gap-6">
{/*  Video Upload Component  */}
<section className="col-span-12 lg:col-span-8 bg-white border border-slate-200 rounded-xl overflow-hidden relative group">
<div className="aspect-video bg-on-background relative flex items-center justify-center">
<img alt="Video Placeholder" className="absolute inset-0 w-full h-full object-cover opacity-60" data-alt="over-the-shoulder view of a laptop displaying a presentation recording with colorful data overlays and waveforms" src="https://lh3.googleusercontent.com/aida-public/AB6AXuB-DT_wt8Wm3VdToqkxajxKPsuDv_iIsiU31NAkkC384rI1hGbiGiPVYAgG9XfEzxJ5kL_id1nXqBFnD-NzSXutuOCdSlvB13V6wBD0XPLdwJnAUXthxxDr_1Ep4LWVceZ84LE7cXDZJaqHuolMp6PRVWHAbwqtul0f4rU9tcj_GiwTlHgKPJH_Dho376e-NAuiWBxKwA30QrffYysbtyDr8Bt8zv1BOe3cJTIwz_d1G_TJhK3d4lTwDj0yBdNaPAd52OidlaNesUg"/>
<div className="relative z-10 flex flex-col items-center">
<div className="w-20 h-20 bg-primary/90 text-white rounded-full flex items-center justify-center cursor-pointer hover:scale-105 transition-transform">
<span className="material-symbols-outlined scale-150" data-icon="play_arrow" style={{ fontVariationSettings: "'FILL' 1" }}>play_arrow</span>
</div>
<p className="mt-4 text-white font-medium">Replaying Presentation Clip (00:30)</p>
</div>
</div>
{/*  Analysis Progress Bar  */}
<div className="p-6 bg-surface-container-low border-t border-slate-200">
<div className="flex justify-between items-center mb-3">
<span className="text-data-header font-data-header text-on-surface">Analysis Progress</span>
<span className="text-data-header font-data-header text-primary">85% Complete</span>
</div>
<div className="w-full h-3 bg-surface-container-highest rounded-full overflow-hidden">
<div className="h-full bg-primary rounded-full transition-all duration-1000" style={{ width: '85%' }}></div>
</div>
<div className="flex items-center gap-2 mt-3">
<span className="text-tech-tag font-tech-tag text-slate-500 bg-slate-200 px-2 py-0.5 rounded uppercase">Frame Extraction &amp; Model Inference</span>
<span className="text-data-value font-data-value text-slate-600">Currently processing gesture frequency...</span>
</div>
</div>
</section>
{/*  Multi-Modal Score Dashboard (Sidebar in Grid)  */}
<aside className="col-span-12 lg:col-span-4 flex flex-col gap-6">
{/*  Confidence Ring  */}
<div className="bg-white border border-slate-200 rounded-xl p-6 flex flex-col items-center">
<h3 className="text-data-header font-data-header text-on-surface mb-6 w-full text-left">Confidence Ring (CNN)</h3>
<div className="relative w-40 h-40">
<svg className="w-full h-full gauge-ring" viewBox="0 0 100 100">
<circle className="text-surface-container" cx="50" cy="50" fill="transparent" r="40" stroke="currentColor" strokeWidth="10"></circle>
<circle className="text-secondary" cx="50" cy="50" fill="transparent" r="40" stroke="currentColor" strokeDasharray="251.2" strokeDashoffset="55.26" strokeLinecap="round" strokeWidth="10"></circle>
</svg>
<div className="absolute inset-0 flex flex-col items-center justify-center">
<span className="text-3xl font-black text-on-surface">78%</span>
<span className="text-[10px] uppercase font-bold text-slate-400">Score</span>
</div>
</div>
<div className="mt-6 w-full">
<div className="flex items-center justify-center gap-2">
<span className="text-tech-tag font-tech-tag bg-slate-100 text-slate-600 px-2 py-1 rounded">CNN Inference (MobileNetV2)</span>
</div>
</div>
</div>
{/*  Filler Word Counter  */}
<div className="bg-white border border-slate-200 rounded-xl p-6">
<h3 className="text-data-header font-data-header text-on-surface mb-4">Filler Word Counter</h3>
<div className="grid grid-cols-3 gap-3">
<div className="bg-surface-container-low p-4 rounded-lg text-center border border-slate-100">
<div className="text-2xl font-black text-primary">2</div>
<div className="text-[11px] font-bold text-slate-500 uppercase">Um</div>
</div>
<div className="bg-surface-container-low p-4 rounded-lg text-center border border-slate-100">
<div className="text-2xl font-black text-primary">1</div>
<div className="text-[11px] font-bold text-slate-500 uppercase">Uh</div>
</div>
<div className="bg-surface-container-low p-4 rounded-lg text-center border border-slate-100">
<div className="text-2xl font-black text-error">4</div>
<div className="text-[11px] font-bold text-slate-500 uppercase">Like</div>
</div>
</div>
</div>
</aside>
{/*  Vocal Energy Chart (Wide)  */}
<section className="col-span-12 lg:col-span-8 bg-white border border-slate-200 rounded-xl p-6">
<div className="flex justify-between items-center mb-6">
<h3 className="text-data-header font-data-header text-on-surface">Vocal Energy Dynamics</h3>
<span className="text-tech-tag font-tech-tag bg-blue-50 text-primary px-2 py-1 rounded">RNN/LSTM Sequence Analysis</span>
</div>
<div className="h-48 flex items-end gap-1 px-2 relative">
{/*  Fake Line Chart Background  */}
<div className="absolute bottom-0 left-0 right-0 h-32 border-b border-slate-100 border-dashed"></div>
<div className="absolute bottom-16 left-0 right-0 h-16 border-b border-slate-100 border-dashed"></div>
{/*  Bars/Waveform for Energy  */}
<div className="flex-1 bg-surface-container-high h-12 rounded-t-sm"></div>
<div className="flex-1 bg-primary h-24 rounded-t-sm"></div>
<div className="flex-1 bg-primary h-32 rounded-t-sm"></div>
<div className="flex-1 bg-primary h-28 rounded-t-sm"></div>
<div className="flex-1 bg-primary h-16 rounded-t-sm"></div>
<div className="flex-1 bg-primary h-36 rounded-t-sm"></div>
<div className="flex-1 bg-primary h-40 rounded-t-sm"></div>
<div className="flex-1 bg-secondary h-44 rounded-t-sm"></div>
<div className="flex-1 bg-primary h-32 rounded-t-sm"></div>
<div className="flex-1 bg-primary h-20 rounded-t-sm"></div>
<div className="flex-1 bg-primary h-24 rounded-t-sm"></div>
<div className="flex-1 bg-primary h-12 rounded-t-sm"></div>
<div className="flex-1 bg-primary h-28 rounded-t-sm"></div>
<div className="flex-1 bg-primary h-32 rounded-t-sm"></div>
<div className="flex-1 bg-primary h-44 rounded-t-sm"></div>
<div className="flex-1 bg-primary h-36 rounded-t-sm"></div>
<div className="flex-1 bg-primary h-24 rounded-t-sm"></div>
<div className="flex-1 bg-primary h-32 rounded-t-sm"></div>
<div className="flex-1 bg-primary h-20 rounded-t-sm"></div>
<div className="flex-1 bg-primary h-16 rounded-t-sm"></div>
</div>
<div className="flex justify-between mt-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">
<span>Introduction</span>
<span>Core Argument</span>
<span>Conclusion</span>
</div>
</section>
{/*  Comparative Feedback & Tips  */}
<section className="col-span-12 lg:col-span-4 bg-primary text-white rounded-xl p-6 flex flex-col justify-between">
<div>
<div className="flex items-center gap-2 mb-4">
<span className="material-symbols-outlined" data-icon="lightbulb" style={{ fontVariationSettings: "'FILL' 1" }}>lightbulb</span>
<h3 className="text-data-header font-data-header">Presentation Insights</h3>
</div>
<div className="space-y-4">
<div className="p-4 bg-white/10 rounded-lg backdrop-blur-sm border border-white/10">
<p className="text-sm font-medium mb-1">Pitch Variance</p>
<p className="text-xs opacity-80 leading-relaxed">Your pitch is 15% flatter than expert benchmarks during transitions. Try emphasizing your final words to retain audience focus.</p>
</div>
<div className="p-4 bg-white/10 rounded-lg backdrop-blur-sm border border-white/10">
<p className="text-sm font-medium mb-1">Pacing Tip</p>
<p className="text-xs opacity-80 leading-relaxed">Current pace: 142 wpm. Target: 130 wpm for maximum clarity. Slow down after presenting a key data point.</p>
</div>
</div>
</div>
<button className="mt-6 w-full py-3 bg-white text-primary rounded-lg font-bold text-sm hover:bg-surface-container-high transition-colors">
                    View Expert Comparison
                </button>
</section>
</div>
</main>
{/*  Contextual FAB (Restricted to Dashboard view)  */}
<button className="fixed bottom-8 right-8 bg-secondary text-on-secondary w-14 h-14 rounded-full flex items-center justify-center shadow-xl hover:scale-105 active:scale-95 transition-all z-50">
<span className="material-symbols-outlined" data-icon="add">add</span>
</button>

    </div>
  );
}
