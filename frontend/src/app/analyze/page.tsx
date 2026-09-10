'use client';
import React, { useState, useRef, useEffect } from 'react';

export default function Phase2() {
  const [isRecording, setIsRecording] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState<any>(null);
  
  const videoRef = useRef<HTMLVideoElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const videoChunksRef = useRef<Blob[]>([]);

  useEffect(() => {
    // Start camera preview immediately on load
    const startPreview = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        if (videoRef.current && !videoRef.current.srcObject) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error("Camera access denied on load:", err);
      }
    };
    startPreview();
  }, []);

  const toggleRecording = async () => {
    if (isRecording) {
      // Stop recording
      mediaRecorderRef.current?.stop();
      if (videoRef.current && videoRef.current.srcObject) {
        const stream = videoRef.current.srcObject as MediaStream;
        stream.getTracks().forEach(track => track.stop());
      }
      setIsRecording(false);
      setIsAnalyzing(true);
    } else {
      // Start recording
      try {
        let stream = videoRef.current?.srcObject as MediaStream;
        if (!stream) {
          stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
          }
        }
        
        const mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm' });
        mediaRecorderRef.current = mediaRecorder;
        videoChunksRef.current = [];

        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            videoChunksRef.current.push(event.data);
          }
        };

        mediaRecorder.onstop = async () => {
          const videoBlob = new Blob(videoChunksRef.current, { type: 'video/webm' });
          const formData = new FormData();
          formData.append('video', videoBlob, 'presentation.webm');

          try {
            const res = await fetch('http://localhost:8000/api/analyze', {
              method: 'POST',
              body: formData,
            });
            const data = await res.json();
            
            if (res.ok && !data.error) {
              setResults(data);
            } else {
              alert("Analysis failed: " + (data.detail || data.error || "Unknown error"));
              setResults(null);
            }
          } catch (error) {
            console.error("Analysis failed:", error);
            alert("Failed to connect to backend. Is FastAPI running?");
          } finally {
            setIsAnalyzing(false);
          }
        };

        mediaRecorder.start();
        setIsRecording(true);
        setResults(null);
      } catch (err) {
        console.error("Error accessing camera/mic:", err);
        alert("Camera/Microphone access denied.");
      }
    }
  };

  const circumference = 2 * Math.PI * 40;
  const conf = results?.adjusted_confidence ?? 0;
  const score = results?.adjusted_confidence ?? "--";
  const strokeDashoffset = results ? circumference - (conf / 100) * circumference : circumference;

  return (
    <div className="h-screen bg-[#FDFDFD] font-sans text-gray-900 flex flex-col overflow-hidden">
      
      {/* Top Header */}
      <header className="flex-shrink-0 flex justify-between items-center px-8 py-3 bg-white border-b border-gray-100">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-indigo-900">school</span>
          <h1 className="text-xl font-bold text-indigo-900">PersonaPath</h1>
        </div>
        
        <nav className="flex gap-6 text-sm font-semibold text-gray-400">
          <a href="/learn" className="hover:text-gray-800 transition-colors">Phase 1</a>
          <a href="/analyze" className="text-indigo-900 border-b-2 border-indigo-900 pb-1">Phase 2</a>
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

      {/* Title */}
      <div className="flex-shrink-0 text-center py-4 bg-white">
        <h2 className="text-2xl font-bold text-gray-800 mb-1">Phase 2: Communication Coach</h2>
        <p className="text-gray-500 text-xs">Evaluates confidence, expression, and delivery using voice and facial cues.</p>
      </div>

      {/* Main Layout */}
      <main className="flex-1 w-full max-w-[1500px] mx-auto px-6 pb-6 grid gap-6 grid-cols-10 grid-rows-[minmax(0,1fr)_160px] min-h-0">
        
        {/* Top Left: Video */}
        <div className="col-span-6 bg-black rounded-xl overflow-hidden shadow-sm relative group h-full min-h-0">
            {results && results.processed_video_url ? (
               <video 
                 src={`http://localhost:8000${results.processed_video_url}`} 
                 controls 
                 className="absolute inset-0 w-full h-full object-cover" 
               />
            ) : (
                <video 
                  ref={videoRef} 
                  autoPlay 
                  muted 
                  playsInline 
                  className="absolute inset-0 w-full h-full object-cover" 
                />
            )}

            {/* Record Button */}
            {!results && (
              <div className="absolute bottom-10 left-1/2 -translate-x-1/2 z-10">
                <button 
                  onClick={toggleRecording}
                  className={`w-12 h-12 rounded-full flex items-center justify-center text-white shadow-lg transition-transform hover:scale-105 ${isRecording ? 'bg-red-600 animate-pulse' : 'bg-indigo-600'}`}
                >
                  <span className="material-symbols-outlined text-2xl">{isRecording ? 'stop' : 'videocam'}</span>
                </button>
              </div>
            )}
            
        </div>
        {/* Top Right: Metrics */}
        <div className="col-span-4 grid grid-rows-[auto_minmax(0,1fr)] gap-3 min-h-0 h-full">
            
            {/* Analysis Progress */}
            <div className="bg-white rounded-xl p-5 shadow-[0_2px_10px_rgba(0,0,0,0.04)] border border-gray-200 flex-shrink-0">
              <div className="flex justify-between items-end mb-3">
                <span className="text-[11px] font-bold text-gray-700">Analysis Complete</span>
                <span className="text-[#1A365D] font-bold text-xs">{isAnalyzing ? "Processing..." : results ? "100%" : "0%"}</span>
              </div>
              <div className="w-full h-2.5 bg-gray-100 rounded-full overflow-hidden">
                <div className={`h-full bg-[#1A365D] rounded-full transition-all ${isAnalyzing ? 'w-1/2 animate-pulse' : results ? 'w-full' : 'w-0'}`}></div>
              </div>
            </div>

            {/* Scores Single Card */}
            <div className="bg-white rounded-xl p-5 shadow-[0_2px_10px_rgba(0,0,0,0.04)] border border-gray-200 flex flex-col min-h-0 h-full">
              
              {/* Top Section: Confidence & Fillers */}
              <div className="flex flex-1 mb-3">
                {/* Confidence Score (Left) */}
                <div className="flex-1 border-r border-gray-100 pr-5 flex flex-col">
                  <h4 className="text-[11px] font-bold text-gray-700 mb-2">Confidence Score</h4>
                  
                  <div className="flex-1 flex flex-col items-center justify-center">
                    <div className="relative w-20 h-20 flex items-center justify-center mb-0">
                      <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="40" stroke="#F3F4F6" strokeWidth="12" fill="none" />
                        <circle 
                          cx="50" cy="50" r="40" 
                          stroke="#1A365D" strokeWidth="12" fill="none" strokeLinecap="round"
                          strokeDasharray={circumference}
                          strokeDashoffset={strokeDashoffset}
                          className="transition-all duration-1000 ease-out"
                        />
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className="text-xl font-black text-[#1A365D]">{score}{results ? '%' : ''}</span>
                      </div>
                    </div>
                    <div className="w-full bg-[#F8FAFC] rounded uppercase text-center py-1.5 text-[8px] font-bold text-gray-400 tracking-widest -mt-2 z-10 relative">
                      MobileNetV2
                    </div>
                  </div>
                </div>

                {/* Filler Words (Right) */}
                <div className="flex-1 pl-5 flex flex-col">
                  <h4 className="text-[11px] font-bold text-gray-700 mb-2">Filler Words</h4>
                  
                  <div className="flex flex-col gap-3 flex-1 justify-center">
                    <div className="flex justify-between items-center bg-[#F4F7FB] px-4 py-3 rounded-lg">
                      <span className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">UM</span>
                      <span className="font-bold text-[#1A365D] text-sm">{results?.filler_counts?.um ?? "-"}</span>
                    </div>
                    <div className="flex justify-between items-center bg-[#F4F7FB] px-4 py-3 rounded-lg">
                      <span className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">UH</span>
                      <span className="font-bold text-[#1A365D] text-sm">{results?.filler_counts?.uh ?? "-"}</span>
                    </div>
                    <div className="flex justify-between items-center bg-[#FCF8F8] px-4 py-3 rounded-lg">
                      <span className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">LIKE</span>
                      <span className="font-bold text-[#B91C1C] text-sm">{results?.filler_counts?.like ?? "-"}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Bottom Section: PACE, SILENCE, PITCH, EMOTION */}
              <div className="border-t border-gray-100 pt-3 mb-1 flex justify-between">
                <div className="flex flex-col">
                  <span className="text-[9px] text-gray-500 font-bold uppercase mb-1 tracking-wider">PACE</span>
                  <span className="text-[12px] font-bold text-[#1A365D]">{results ? results.wpm : "--"} wpm</span>
                </div>
                <div className="flex flex-col">
                  <span className="text-[9px] text-gray-500 font-bold uppercase mb-1 tracking-wider">SILENCE</span>
                  <span className="text-[12px] font-bold text-[#1A365D]">{results ? results.silence_ratio : "--"}%</span>
                </div>
                <div className="flex flex-col">
                  <span className="text-[9px] text-gray-500 font-bold uppercase mb-1 tracking-wider">PITCH</span>
                  <span className="text-[12px] font-bold text-[#1A365D]">{results ? results.pitch_std : "--"} Hz</span>
                </div>
                <div className="flex flex-col">
                  <span className="text-[9px] text-gray-500 font-bold uppercase mb-1 tracking-wider">EMOTION</span>
                  <span className="text-[12px] font-bold text-[#1A365D]">{results ? results.dominant_emotion : "--"}</span>
                </div>
              </div>
            </div>
        </div>

        {/* Bottom Left: Vocal Energy */}
        <div className="col-span-6 bg-white rounded-xl p-5 shadow-[0_2px_10px_rgba(0,0,0,0.04)] border border-gray-200 flex flex-col h-full min-h-0">
            <div className="flex justify-between items-center mb-3">
              <h4 className="text-xs font-bold text-gray-700">Vocal Energy Dynamics</h4>
              <span className="text-[8px] bg-blue-50 text-blue-600 font-bold px-2 py-0.5 rounded uppercase tracking-wider">RNN/LSTM SEQUENCE ANALYSIS</span>
            </div>
            
            <div className="flex-1 w-full flex items-end gap-1 px-1 mb-1">
              {results && results.energy_contour ? (
                 results.energy_contour.map((energy: number, idx: number) => (
                   <div key={idx} className="flex-1 bg-[#1A365D] hover:bg-indigo-700 transition-colors" style={{ height: `${Math.max(10, energy * 100)}%` }}></div>
                 ))
              ) : (
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0].map((h, i) => (
                  <div key={i} className="flex-1 bg-gray-100" style={{ height: `100%` }}></div>
                ))
              )}
            </div>
            
            <div className="flex justify-between text-[8px] text-gray-400 font-bold uppercase tracking-wider px-2 border-t border-gray-100 pt-1">
               <span>INTRODUCTION</span>
               <span>CORE ARGUMENT</span>
               <span>CONCLUSION</span>
            </div>
        </div>

        {/* Bottom Right: Presentation Insights */}
        <div className="col-span-4 bg-[#102359] rounded-xl p-5 text-white flex flex-col shadow-lg overflow-hidden h-full min-h-0">
            <h4 className="text-[12px] font-bold mb-3">Presentation Insights</h4>
            
            <div className="flex flex-col flex-1 min-h-0">
              <div className="bg-[#1D326C] rounded-lg p-3.5 flex gap-3 items-start flex-1 overflow-y-auto">
                <span className="text-[14px] mt-0.5">🌟</span>
                <p className="text-[12px] text-blue-50 font-medium leading-relaxed">
                  {results?.coaching?.length > 0 ? results.coaching.join(" ") : "Record your presentation to receive AI coaching feedback here."}
                </p>
              </div>
            </div>
        </div>

      </main>
    </div>
  );
}
