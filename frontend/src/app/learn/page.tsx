'use client';
import React, { useState, useRef } from 'react';

export default function Phase1() {
  return (
    <div className="flex-1 w-full h-full">
      
{/*  Top Navigation Bar  */}
<header className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 flex justify-between items-center w-full px-6 py-4 max-w-full mx-auto fixed top-0 z-50">
<div className="text-2xl font-black text-blue-800 dark:text-blue-400 font-['Lexend']">PersonaPath</div>
<nav className="hidden md:flex gap-8">
<a className="text-blue-800 dark:text-blue-400 border-b-2 border-blue-800 dark:border-blue-400 pb-1 font-['Lexend'] font-medium transition-colors" href="#">Phase 1</a>
<a className="text-slate-500 dark:text-slate-400 hover:text-blue-700 dark:hover:text-blue-300 font-['Lexend'] font-medium transition-colors" href="#">Phase 2</a>
</nav>
<div className="flex items-center gap-4">
<span className="material-symbols-outlined text-slate-600 cursor-pointer hover:scale-95 transition-transform" data-icon="notifications">notifications</span>
<span className="material-symbols-outlined text-slate-600 cursor-pointer hover:scale-95 transition-transform" data-icon="settings">settings</span>
<span className="material-symbols-outlined text-blue-800 cursor-pointer hover:scale-95 transition-transform" data-icon="account_circle">account_circle</span>
</div>
</header>
<main className="pt-24 pb-12 px-gutter max-w-container-max mx-auto flex flex-col gap-lg">
{/*  Tab Switcher  */}
<div className="flex items-center gap-sm bg-surface-container-low p-1 rounded-xl w-fit mx-auto shadow-sm">
<button className="px-lg py-sm rounded-lg bg-white shadow-sm text-primary font-display-learning text-[16px] flex items-center gap-2">
<span className="material-symbols-outlined text-[20px]" data-icon="auto_stories">auto_stories</span>
                Phase 1: Literacy Coach
            </button>
<button className="px-lg py-sm rounded-lg text-outline font-display-learning text-[16px] hover:bg-surface-container-high transition-colors flex items-center gap-2">
<span className="material-symbols-outlined text-[20px]" data-icon="record_voice_over">record_voice_over</span>
                Phase 2: Presentation Pro
            </button>
</div>
{/*  Main Dashboard Grid  */}
<div className="grid grid-cols-12 gap-lg mt-md">
{/*  Left Column: Reading Interface  */}
<div className="col-span-12 lg:col-span-8 flex flex-col gap-lg">
{/*  Reference Text & Highlighter  */}
<div className="bg-white rounded-xl border border-outline-variant p-xl shadow-[0px_4px_20px_rgba(0,0,0,0.05)]">
<div className="flex items-center justify-between mb-lg">
<h2 className="font-display-learning text-on-surface">Reading Passage</h2>
<span className="text-tech-tag font-tech-tag px-sm py-1 bg-surface-container rounded-full text-outline-variant">LEVEL: PRIMARY</span>
</div>
<div className="p-lg bg-surface-container-low rounded-xl mb-md">
<p className="font-display-learning text-display-learning tracking-tight">
<span className="text-secondary">The</span>
<span className="text-secondary">elephant</span>
<span className="text-error underline decoration-wavy underline-offset-8">sat</span>
<span className="text-outline/40">quietly</span>
<span className="text-outline/40">by</span>
<span className="text-outline/40">the</span>
<span className="text-outline/40">river</span>
<span className="text-outline/40">bank</span>
</p>
</div>
<div className="flex items-center gap-2 mt-sm">
<span className="material-symbols-outlined text-[14px] text-primary" data-icon="neurology">neurology</span>
<span className="font-tech-tag text-tech-tag text-primary uppercase">Transformer-based Alignment (Wav2Vec 2.0)</span>
</div>
</div>
{/*  Audio Module (Gradio Style)  */}
<div className="bg-surface-container-lowest border border-outline-variant rounded-xl p-lg">
<div className="flex flex-col items-center justify-center border-2 border-dashed border-primary-container/20 rounded-xl py-xl bg-surface-container-low/30">
<div className="bg-primary p-md rounded-full text-white shadow-lg mb-md cursor-pointer hover:scale-105 transition-transform">
<span className="material-symbols-outlined text-[32px]" data-icon="mic" data-weight="fill">mic</span>
</div>
<p className="font-data-header text-primary mb-xs">Click to start recording</p>
<p className="text-data-value text-outline">or drag and drop your audio file here</p>
</div>
<div className="mt-md h-12 w-full bg-surface-container rounded-lg flex items-center px-md gap-4 overflow-hidden">
<div className="w-1 bg-secondary h-6 rounded-full opacity-30"></div>
<div className="w-1 bg-secondary h-10 rounded-full"></div>
<div className="w-1 bg-secondary h-8 rounded-full"></div>
<div className="w-1 bg-secondary h-4 rounded-full"></div>
<div className="w-1 bg-secondary h-9 rounded-full"></div>
<div className="w-1 bg-secondary h-6 rounded-full opacity-60"></div>
<div className="w-1 bg-secondary h-10 rounded-full"></div>
<div className="w-1 bg-secondary h-8 rounded-full"></div>
<div className="w-1 bg-secondary h-4 rounded-full"></div>
<div className="w-1 bg-secondary h-11 rounded-full"></div>
<div className="flex-grow"></div>
<span className="text-data-value text-secondary font-bold">00:04 / 00:12</span>
</div>
</div>
</div>
{/*  Right Column: Analytics & Coaching  */}
<div className="col-span-12 lg:col-span-4 flex flex-col gap-lg">
{/*  Coaching Corner  */}
<div className="relative">
<div className="flex items-center gap-md mb-sm">
<div className="w-12 h-12 rounded-full overflow-hidden border-2 border-primary-container shadow-sm">
<img alt="Friendly AI Tutor" className="w-full h-full object-cover" data-alt="close-up portrait of a friendly female teacher with a kind smile and glasses in a brightly lit modern office" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAAWzUqWsXKLr92Mj3oznXPFd9ia2E9uHyAiCBMLVJccuswAcDPAI235zUdaSGgHp3I-Z0T-V9pcFBIjoTXYV_C15W4jGAuTgok5HMx_TgavisAAogaMwPATxweMYiwvUYfpfW2FvJAYXf_7I0y7VDaDRUsTs9VPRGQb_Y2CYslp1X2lS3icQtEsRXnXmMd6rC9-8HNIX7dypD-b7l2oOq55XpXvnnS8RDNPq9qQHliJoJK7-Ob8yTUda00ciwoUaoxhttTR-CPy4I"/>
</div>
<div>
<p className="font-data-header text-primary">Claude's Coaching Corner</p>
<p className="text-tech-tag text-outline">Active Feedback</p>
</div>
</div>
<div className="bg-white p-lg rounded-xl shadow-[0px_4px_20px_rgba(0,0,0,0.05)] coaching-bubble-tail border border-slate-100">
<p className="text-body-coaching text-on-surface leading-relaxed">
                            "Great job on <span className="text-secondary font-bold">‘elephant’</span>! Let's try saying <span className="text-error font-bold">‘sat’</span> again slowly. You're doing amazing!"
                        </p>
</div>
</div>
{/*  Metric Cards  */}
<div className="grid grid-cols-2 gap-md">
{/*  WPM Card  */}
<div className="bg-white border border-outline-variant p-md rounded-xl flex flex-col justify-between">
<div className="flex justify-between items-start">
<span className="material-symbols-outlined text-secondary" data-icon="speed">speed</span>
<span className="bg-secondary-container text-on-secondary-container text-tech-tag px-2 py-0.5 rounded-full">+5</span>
</div>
<div className="mt-lg">
<p className="font-data-header text-outline text-[12px] uppercase">Words Per Min</p>
<p className="font-display-learning text-[40px] text-on-background leading-none">45</p>
</div>
</div>
{/*  Hesitation Card  */}
<div className="bg-white border border-outline-variant p-md rounded-xl flex flex-col justify-between">
<div className="flex justify-between items-start">
<span className="material-symbols-outlined text-error" data-icon="timer">timer</span>
<span className="bg-error-container text-on-error-container text-tech-tag px-2 py-0.5 rounded-full">-1</span>
</div>
<div className="mt-lg">
<p className="font-data-header text-outline text-[12px] uppercase">Hesitations</p>
<p className="font-display-learning text-[40px] text-on-background leading-none">2</p>
</div>
</div>
</div>
{/*  Progress Visual  */}
<div className="bg-surface-container-low rounded-xl p-lg border border-primary-container/10">
<div className="flex justify-between items-center mb-md">
<p className="font-data-header text-on-surface">Daily Progress</p>
<p className="text-data-value text-primary font-bold">75%</p>
</div>
<div className="w-full bg-white h-3 rounded-full overflow-hidden">
<div className="bg-primary h-full w-3/4 rounded-full"></div>
</div>
<p className="text-tech-tag text-outline mt-sm">3 of 4 sessions completed today</p>
</div>
{/*  Call to Action  */}
<button className="w-full py-lg bg-primary text-white rounded-xl font-display-learning text-[18px] shadow-lg hover:translate-y-[-2px] transition-all active:scale-95 flex items-center justify-center gap-3">
<span className="material-symbols-outlined" data-icon="bolt" data-weight="fill">bolt</span>
                    Try Next Passage
                </button>
</div>
</div>
</main>
{/*  Side Navigation Bar (Hidden on Mobile)  */}
<aside className="fixed left-0 top-0 h-screen w-64 bg-slate-50 dark:bg-slate-950 border-r border-slate-200 dark:border-slate-800 flex flex-col p-4 z-40 hidden md:flex">
<div className="mb-xl pt-4 px-2">
<h1 className="text-lg font-bold text-blue-800 dark:text-blue-400 font-['Lexend']">Faculty Context</h1>
<p className="text-xs text-slate-500 font-medium uppercase tracking-wider">Institutional View</p>
</div>
<nav className="flex flex-col gap-2 flex-grow">
<a className="flex items-center gap-3 p-3 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 font-bold rounded-lg transition-all duration-200 ease-in-out" href="#">
<span className="material-symbols-outlined" data-icon="school">school</span>
<span className="font-['Lexend'] text-sm">Academic Overview</span>
</a>
<a className="flex items-center gap-3 p-3 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800 rounded-lg transition-all duration-200 ease-in-out" href="#">
<span className="material-symbols-outlined" data-icon="groups">groups</span>
<span className="font-['Lexend'] text-sm">Faculty Portal</span>
</a>
<a className="flex items-center gap-3 p-3 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800 rounded-lg transition-all duration-200 ease-in-out" href="#">
<span className="material-symbols-outlined" data-icon="trending_up">trending_up</span>
<span className="font-['Lexend'] text-sm">Student Progress</span>
</a>
<a className="flex items-center gap-3 p-3 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800 rounded-lg transition-all duration-200 ease-in-out" href="#">
<span className="material-symbols-outlined" data-icon="auto_stories">auto_stories</span>
<span className="font-['Lexend'] text-sm">Curriculum Insights</span>
</a>
</nav>
<div className="pt-4 border-t border-slate-200 dark:border-slate-800">
<button className="w-full py-3 bg-blue-800 hover:bg-blue-700 text-white font-['Lexend'] text-sm rounded-lg transition-colors">
                Generate Report
            </button>
</div>
</aside>
{/*  Bottom Navigation for Mobile  */}
<nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-slate-200 flex justify-around py-3 px-2 z-50">
<div className="flex flex-col items-center gap-1 text-primary">
<span className="material-symbols-outlined" data-icon="home" data-weight="fill">home</span>
<span className="text-[10px] font-bold">Home</span>
</div>
<div className="flex flex-col items-center gap-1 text-outline">
<span className="material-symbols-outlined" data-icon="auto_stories">auto_stories</span>
<span className="text-[10px]">Coach</span>
</div>
<div className="flex flex-col items-center gap-1 text-outline">
<span className="material-symbols-outlined" data-icon="analytics">analytics</span>
<span className="text-[10px]">Stats</span>
</div>
<div className="flex flex-col items-center gap-1 text-outline">
<span className="material-symbols-outlined" data-icon="person">person</span>
<span className="text-[10px]">Profile</span>
</div>
</nav>

    </div>
  );
}
