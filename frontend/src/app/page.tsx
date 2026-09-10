import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 gap-8">
      <h1 className="text-4xl font-display font-black text-primary">PersonaPath</h1>
      <p className="text-lg text-slate-600 max-w-lg text-center">
        A dual-persona web application for literacy speech assessment. Choose your experience below.
      </p>
      
      <div className="flex gap-4">
        <Link 
          href="/learn"
          className="px-6 py-3 bg-white text-primary font-bold rounded-xl shadow-sm border border-slate-200 hover:bg-slate-50 transition"
        >
          Phase 1: Literacy Coach
        </Link>
        <Link 
          href="/analyze"
          className="px-6 py-3 bg-primary text-white font-bold rounded-xl shadow-md hover:bg-primary-container transition"
        >
          Phase 2: Presentation Pro
        </Link>
      </div>
    </div>
  );
}
