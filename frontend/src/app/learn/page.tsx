'use client';
import React, { useState, useRef, useEffect } from 'react';

export default function Phase1() {
  const [isRecording, setIsRecording] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [results, setResults] = useState<any>(null);
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const audioPlayerRef = useRef<HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);

  const defaultPassage = "One sunny evening I went to the park with my friends. We played games ran around and laughed together. The cool breeze felt nice and the sky looked very beautiful. After playing we sat under a big tree and talked happily. It was a wonderful day and I felt very happy.";
  
  const [passage, setPassage] = useState(defaultPassage);

  const toggleRecording = async () => {
    if (isRecording) {
      // Stop recording
      mediaRecorderRef.current?.stop();
      setIsRecording(false);
    } else {
      // Start recording
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;
        audioChunksRef.current = [];

        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunksRef.current.push(event.data);
          }
        };

        mediaRecorder.onstop = () => {
          const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
          setAudioBlob(blob);
        };

        mediaRecorder.start();
        setIsRecording(true);
        setResults(null);
        setAudioBlob(null);
      } catch (err) {
        console.error("Error accessing mic:", err);
        alert("Microphone access denied.");
      }
    }
  };

  const togglePlayback = () => {
    if (!audioBlob || !audioPlayerRef.current) return;
    if (isPlaying) {
      audioPlayerRef.current.pause();
      setIsPlaying(false);
    } else {
      audioPlayerRef.current.src = URL.createObjectURL(audioBlob);
      audioPlayerRef.current.play();
      setIsPlaying(true);
      audioPlayerRef.current.onended = () => setIsPlaying(false);
    }
  };

  const handleAnalyze = async () => {
    if (!audioBlob) {
      alert("Please record yourself reading the passage first by clicking the microphone icon!");
      return;
    }
    
    setIsAnalyzing(true);
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.webm');
    formData.append('reference_text', passage);

    try {
      const res = await fetch('http://localhost:8000/api/analyze_phase1', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setResults(data);
    } catch (error) {
      console.error("Analysis failed:", error);
      alert("Failed to connect to backend. Is FastAPI running?");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const renderPassage = () => {
    if (results && results.word_scores) {
      return results.word_scores.map((ws: any, idx: number) => {
        let color = "text-gray-400";
        let underline = "";
        if (ws.score === 'green') color = "text-emerald-600 font-bold";
        if (ws.score === 'red') { color = "text-red-500 font-bold"; underline = "underline decoration-red-300 decoration-wavy underline-offset-4"; }
        if (ws.score === 'grey') { color = "text-orange-400 font-bold"; underline = "underline decoration-orange-300 decoration-wavy underline-offset-4"; }
        return <span key={idx} className={`${color} ${underline}`}>{ws.word} </span>;
      });
    }

    const words = passage.split(' ');
    return words.map((w, i) => {
      return <span key={i} className="text-gray-800">{w} </span>;
    });
  };

  return (
    <div className="h-screen flex flex-col bg-[#F8F9FA] font-sans overflow-hidden text-gray-800">
      <audio ref={audioPlayerRef} className="hidden" />
      
      {/* Top Header */}
      <header className="flex-shrink-0 flex justify-between items-center px-8 py-3 bg-white border-b border-gray-100">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-indigo-900">school</span>
          <h1 className="text-xl font-bold text-indigo-900">PersonaPath</h1>
        </div>
        
        <nav className="flex gap-6 text-sm font-semibold text-gray-400">
          <a href="/learn" className="text-indigo-900 border-b-2 border-indigo-900 pb-1">Phase 1</a>
          <a href="/analyze" className="hover:text-gray-800 transition-colors">Phase 2</a>
        </nav>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-emerald-50 text-emerald-600 px-3 py-1 rounded-full text-xs font-bold border border-emerald-100">
            <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
            ACTIVE SESSION
          </div>
          <div className="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-700 font-bold">
            P
          </div>
        </div>
      </header>

      {/* Main Layout */}
      <main className="flex-1 w-full max-w-[1500px] mx-auto p-4 flex gap-4 min-h-0">
        
        {/* LEFT COLUMN (Light Theme) */}
        <div className="w-[350px] flex-shrink-0 flex flex-col gap-4">
          
          {/* Passage Selection Card */}
          <div className="bg-white rounded-xl p-4 flex-shrink-0 shadow-[0_2px_10px_rgba(0,0,0,0.03)] border border-gray-200">
            <label className="text-gray-500 text-[10px] font-bold uppercase tracking-wider mb-1.5 block">Select a passage</label>
            <div className="relative mb-3">
              <select className="w-full bg-[#F4F7FB] text-gray-700 border border-gray-200 rounded-lg px-3 py-2 text-[12px] font-medium focus:outline-none appearance-none">
                <option>Advanced - Full Story (Hard)</option>
              </select>
              <span className="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none text-sm">expand_more</span>
            </div>

            <label className="text-gray-500 text-[10px] font-bold uppercase tracking-wider mb-1.5 block">Passage text (read this aloud)</label>
            <div className="bg-[#F4F7FB] p-3 rounded-lg border border-gray-200 text-gray-600 font-medium text-[12px] leading-relaxed mb-3 h-[80px] overflow-y-auto">
              {passage}
            </div>

            <div className="flex items-center gap-2 mt-1">
              <input type="checkbox" className="w-3.5 h-3.5 rounded bg-gray-50 border-gray-300 accent-indigo-600 cursor-pointer" />
              <span className="text-gray-500 text-[11px] font-medium">Use custom passage instead</span>
            </div>
          </div>

          {/* Audio Recorder Card */}
          <div className="bg-white rounded-xl p-4 flex-1 flex flex-col justify-between shadow-[0_2px_10px_rgba(0,0,0,0.03)] border border-gray-200">
            
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-indigo-600 text-[18px]">mic_none</span>
                <span className="text-[#1A365D] text-[11px] font-bold uppercase tracking-wider">READ THE PASSAGE ALOUD</span>
              </div>
              <span className="material-symbols-outlined text-gray-400 cursor-pointer text-lg hover:text-gray-600 transition-colors">more_horiz</span>
            </div>

            {/* Audio Waveform */}
            <div className="w-full flex-1 flex items-center justify-center gap-[3px] mb-2 min-h-[60px]">
              {[20,30,45,35,50,75,40,60,30,45,70,50,40,70,90,55,30,45,85,60,40,75,85,95,75,45,65,40,30,45,70,90,50,75,30,45,20].map((h, i) => (
                <div key={i} className={`w-[3px] rounded-full transition-colors ${i >= 15 && i <= 21 ? 'bg-[#1A365D]' : 'bg-gray-200'}`} style={{ height: `${h}%` }}></div>
              ))}
            </div>

            <div className="flex justify-between text-gray-400 font-medium text-[10px] mb-4 px-1">
              <span>0:08</span>
              <span>0:21</span>
            </div>

            {/* Controls */}
            <div className="flex items-center justify-between mb-5 px-2">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-gray-400 text-[18px] cursor-pointer hover:text-indigo-600 transition-colors">volume_up</span>
                <span className="text-gray-400 font-bold text-[9px] border border-gray-300 bg-gray-50 px-1 py-0.5 rounded cursor-pointer hover:text-indigo-600 transition-colors">1x</span>
              </div>
              <div className="flex items-center gap-4">
                <span className="material-symbols-outlined text-gray-400 text-[20px] cursor-pointer hover:text-indigo-600 transition-colors">fast_rewind</span>
                <button onClick={togglePlayback} className="w-10 h-10 rounded-full bg-indigo-50 flex items-center justify-center text-indigo-600 cursor-pointer hover:scale-105 transition-transform hover:bg-indigo-100">
                  <span className="material-symbols-outlined text-[24px]">
                    {isPlaying ? 'pause' : 'play_arrow'}
                  </span>
                </button>
                <span className="material-symbols-outlined text-gray-400 text-[20px] cursor-pointer hover:text-indigo-600 transition-colors">fast_forward</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="material-symbols-outlined text-gray-400 text-[18px] cursor-pointer hover:text-indigo-600 transition-colors">replay</span>
                <span 
                  onClick={toggleRecording} 
                  className={`material-symbols-outlined text-[18px] cursor-pointer transition-transform hover:scale-110 ${isRecording ? 'text-red-500 animate-pulse' : 'text-indigo-600'}`}
                >
                  {isRecording ? 'stop_circle' : 'mic'}
                </span>
              </div>
            </div>

            {/* Main Action Button */}
            <button 
              onClick={handleAnalyze}
              disabled={isAnalyzing}
              className={`w-full py-2.5 rounded-lg text-white text-sm font-bold shadow-md transition-colors ${isAnalyzing ? 'bg-indigo-400 cursor-wait' : 'bg-[#1A365D] hover:bg-indigo-900'}`}
            >
              {isAnalyzing ? "Analyzing Audio..." : "Analyze Pronunciation"}
            </button>
            <p className="text-gray-400 font-medium text-[9px] mt-3 text-center leading-relaxed">
              Tips: Speak clearly at a natural pace • Quiet environment works best • Max 2 minutes
            </p>
          </div>
        </div>

        {/* RIGHT COLUMN (Light / App UI) */}
        <div className="flex-1 bg-white rounded-xl shadow-[0_2px_10px_rgba(0,0,0,0.03)] border border-gray-200 flex flex-col overflow-hidden">
          
          {/* Blue Header Banner */}
          <div className="bg-[#1A365D] text-white px-5 py-3 flex justify-between items-center flex-shrink-0">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center">
                <span className="material-symbols-outlined text-sm">auto_stories</span>
              </div>
              <div>
                <h2 className="font-bold text-sm">PersonaPath - Literacy Coach</h2>
                <p className="text-blue-200 text-[10px] font-medium">Phase 1 - Reading Analysis</p>
              </div>
            </div>
            <div className="bg-white/10 border border-white/20 px-3 py-1 rounded-full text-[10px] font-semibold backdrop-blur-sm">
              Active Feedback
            </div>
          </div>

          <div className="flex-1 p-4 flex flex-col gap-4 min-h-0 overflow-y-auto">
            
            {/* Top Row */}
            <div className="flex flex-1 gap-4 min-h-0">
              
              {/* Reading Passage */}
              <div className="flex-[2] bg-white rounded-lg border border-gray-200 flex flex-col overflow-hidden">
                <div className="px-4 py-3 border-b border-gray-100 flex justify-between items-center bg-[#FDFDFD]">
                  <h3 className="font-bold text-gray-800 text-xs">Reading Passage</h3>
                  <span className="bg-blue-50 text-blue-600 text-[9px] font-bold px-2 py-0.5 rounded uppercase tracking-wider">LABEL: PRIMARY</span>
                </div>
                
                <div className="p-5 overflow-y-auto flex-1 text-2xl leading-loose tracking-wide">
                  {renderPassage()}
                </div>

                <div className="px-4 py-3 bg-gray-50 border-t border-gray-100 flex justify-between items-center">
                  <p className="text-[9px] text-gray-400 uppercase font-bold tracking-wider">TRANSFORMER-BASED ALIGNMENT (WAV2VEC 2.0)</p>
                  
                  {/* Legend */}
                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-1.5">
                      <div className="w-2.5 h-2.5 rounded-full bg-emerald-500"></div>
                      <span className="text-[10px] font-bold text-gray-500 uppercase">Correct</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <div className="w-2.5 h-2.5 rounded-full bg-orange-400"></div>
                      <span className="text-[10px] font-bold text-gray-500 uppercase">Close</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <div className="w-2.5 h-2.5 rounded-full bg-red-500"></div>
                      <span className="text-[10px] font-bold text-gray-500 uppercase">Needs work</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Stats & Coaching */}
              <div className="flex-1 flex flex-col gap-4">
                {/* Claude Coaching */}
                <div className="bg-white rounded-lg p-4 border border-gray-200">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center">
                      <span className="material-symbols-outlined text-purple-600 text-sm">smart_toy</span>
                    </div>
                    <div>
                      <h4 className="font-bold text-gray-800 text-[11px]">Claude Coaching Corner</h4>
                      <p className="text-emerald-600 text-[9px] font-bold uppercase tracking-wide">Active Feedback</p>
                    </div>
                  </div>
                  <p className="text-[11px] text-gray-600 font-medium italic leading-relaxed">
                    "{results && results.tip ? results.tip : "Record your reading passage and click 'Analyze Pronunciation' to get personalized feedback here!"}"
                  </p>
                </div>

                {/* Metrics Grid */}
                <div className="flex gap-4">
                  <div className="flex-1 bg-white rounded-lg p-4 border border-gray-200 flex flex-col items-center relative">
                    <span className="absolute top-3 left-3 text-[9px] font-bold text-gray-400 uppercase tracking-wide">WORDS / MIN</span>
                    {results && <span className="absolute top-3 right-3 bg-emerald-100 text-emerald-700 text-[9px] font-bold px-1.5 py-0.5 rounded-full">Up</span>}
                    <div className="mt-8 text-4xl font-black text-emerald-600">{results ? results.wpm : "--"}</div>
                    <p className="text-[10px] text-gray-400 font-medium mt-2">{results ? "On track!" : "Waiting..."}</p>
                  </div>
                  <div className="flex-1 bg-white rounded-lg p-4 border border-gray-200 flex flex-col items-center relative">
                    <span className="absolute top-3 left-3 text-[9px] font-bold text-gray-400 uppercase tracking-wide">HESITATIONS</span>
                    {results && <span className="absolute top-3 right-3 bg-emerald-100 text-emerald-700 text-[9px] font-bold px-1.5 py-0.5 rounded-full">Low</span>}
                    <div className="mt-8 text-4xl font-black text-emerald-600">{results ? results.hesitations : "--"}</div>
                    <p className="text-[10px] text-gray-400 font-medium mt-2">{results ? "Great flow!" : "Waiting..."}</p>
                  </div>
                </div>

                {/* Accuracy Bar */}
                <div className="bg-white rounded-lg p-4 border border-gray-200 mt-auto">
                  <div className="flex justify-between items-end mb-2">
                    <span className="text-[11px] font-bold text-gray-600 uppercase tracking-wide">Pronunciation Accuracy</span>
                    <span className="text-[#1A365D] font-bold text-sm">{results && results.word_scores ? Math.round((results.word_scores.filter((w:any)=>w.score==='green').length / results.word_scores.length)*100) : "--"}%</span>
                  </div>
                  <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div className="h-full bg-[#1A365D] rounded-full" style={{width: `${results && results.word_scores ? Math.round((results.word_scores.filter((w:any)=>w.score==='green').length / results.word_scores.length)*100) : 0}%`}}></div>
                  </div>
                  <p className="text-[9px] text-gray-400 font-bold mt-1.5 uppercase tracking-widest">{results ? "Analysis Complete" : "Pending Recording"}</p>
                </div>
              </div>

            </div>

            {/* Bottom Row */}
            <div className="flex gap-4 h-[120px] flex-shrink-0">
              {/* Word Breakdown */}
              <div className="flex-[4] bg-white rounded-lg p-4 border border-gray-200 flex flex-col">
                <h4 className="font-bold text-gray-600 text-[10px] uppercase tracking-wider mb-3">Word Breakdown</h4>
                <div className="flex gap-3 flex-1">
                  <div className="flex-1 bg-emerald-50 rounded-lg flex flex-col items-center justify-center border border-emerald-100">
                    <span className="text-xl font-black text-emerald-600">{results ? results.word_scores?.filter((w:any)=>w.score==='green').length : "-"}</span>
                    <span className="text-[9px] font-bold text-emerald-600/70 uppercase mt-0.5">Correct</span>
                  </div>
                  <div className="flex-1 bg-yellow-50 rounded-lg flex flex-col items-center justify-center border border-yellow-100">
                    <span className="text-xl font-black text-orange-400">{results ? results.word_scores?.filter((w:any)=>w.score==='grey').length : "-"}</span>
                    <span className="text-[9px] font-bold text-orange-400/70 uppercase mt-0.5">Close</span>
                  </div>
                  <div className="flex-1 bg-red-50 rounded-lg flex flex-col items-center justify-center border border-red-100">
                    <span className="text-xl font-black text-red-500">{results ? results.word_scores?.filter((w:any)=>w.score==='red').length : "-"}</span>
                    <span className="text-[9px] font-bold text-red-500/70 uppercase mt-0.5">Missed</span>
                  </div>
                </div>
              </div>

              {/* What We Heard */}
              <div className="flex-[6] bg-[#F4F7FB] rounded-lg p-4 border border-gray-200 overflow-y-auto">
                <h4 className="font-bold text-gray-500 text-[9px] uppercase tracking-widest mb-2">WHAT WE HEARD</h4>
                <p className="text-[12px] font-medium text-gray-600 italic leading-relaxed">
                  {results ? `"${results.transcription}"` : "Waiting for audio analysis..."}
                </p>
              </div>
            </div>

          </div>
        </div>
      </main>
    </div>
  );
}
