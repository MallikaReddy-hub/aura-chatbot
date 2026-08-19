import React, { useState, useEffect, useRef } from 'react';
import {
  Wind,
  Play,
  Pause,
  RotateCcw,
  Volume2,
  VolumeX,
  Sparkles,
  Info,
  Heart
} from 'lucide-react';

const PATTERNS = {
  box: {
    name: '4-4-4-4 Box Breathing',
    subtitle: 'Used for stress relief, focus, and calming an overstimulated nervous system',
    phases: [
      { name: 'Inhale Slowly', duration: 4, instruction: 'Breathe in deeply through your nose' },
      { name: 'Hold Breath', duration: 4, instruction: 'Gently hold the breath in your chest' },
      { name: 'Exhale Smoothly', duration: 4, instruction: 'Release all air slowly through your mouth' },
      { name: 'Hold Empty', duration: 4, instruction: 'Rest gently before the next breath' }
    ]
  },
  relax: {
    name: '4-7-8 Relaxing Breath',
    subtitle: 'Dr. Andrew Weil technique for deep tranquility and sleep support',
    phases: [
      { name: 'Inhale', duration: 4, instruction: 'Inhale quietly through your nose' },
      { name: 'Hold Gently', duration: 7, instruction: 'Retain your breath without strain' },
      { name: 'Exhale Completely', duration: 8, instruction: 'Make a gentle whoosh sound as you exhale' }
    ]
  }
};

export default function BreathingExercise() {
  const [selectedMode, setSelectedMode] = useState('box');
  const [isActive, setIsActive] = useState(false);
  const [currentPhaseIndex, setCurrentPhaseIndex] = useState(0);
  const [secondsLeft, setSecondsLeft] = useState(4);
  const [completedCycles, setCompletedCycles] = useState(0);
  const [soundEnabled, setSoundEnabled] = useState(true);

  const audioCtxRef = useRef(null);

  const pattern = PATTERNS[selectedMode];
  const currentPhase = pattern.phases[currentPhaseIndex];

  // Play peaceful synth chime on phase transitions
  const playChime = (freq = 440) => {
    if (!soundEnabled) return;
    try {
      if (!audioCtxRef.current) {
        audioCtxRef.current = new (window.AudioContext || window.webkitAudioContext)();
      }
      const ctx = audioCtxRef.current;
      if (ctx.state === 'suspended') {
        ctx.resume();
      }
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, ctx.currentTime);
      gain.gain.setValueAtTime(0.08, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 1.2);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start();
      osc.stop(ctx.currentTime + 1.2);
    } catch (e) {
      console.log('Audio chime error:', e);
    }
  };

  useEffect(() => {
    let timer = null;
    if (isActive) {
      timer = setInterval(() => {
        setSecondsLeft((prev) => {
          if (prev <= 1) {
            // Transition to next phase
            const nextIndex = (currentPhaseIndex + 1) % pattern.phases.length;
            if (nextIndex === 0) {
              setCompletedCycles((c) => c + 1);
            }
            setCurrentPhaseIndex(nextIndex);
            playChime(nextIndex === 0 ? 523.25 : 440); // C5 on cycle completion
            return pattern.phases[nextIndex].duration;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [isActive, currentPhaseIndex, selectedMode, soundEnabled]);

  const handleReset = () => {
    setIsActive(false);
    setCurrentPhaseIndex(0);
    setSecondsLeft(pattern.phases[0].duration);
    setCompletedCycles(0);
  };

  const handleModeChange = (mode) => {
    setSelectedMode(mode);
    setIsActive(false);
    setCurrentPhaseIndex(0);
    setSecondsLeft(PATTERNS[mode].phases[0].duration);
  };

  // Determine circle scale based on phase
  const getScaleClass = () => {
    if (!isActive) return 'scale-100';
    const phaseName = currentPhase.name.toLowerCase();
    if (phaseName.includes('inhale')) return 'scale-125 transition-transform duration-[4000ms]';
    if (phaseName.includes('hold')) return 'scale-125';
    if (phaseName.includes('exhale')) return 'scale-90 transition-transform duration-[4000ms]';
    return 'scale-90';
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-8">
      {/* Header */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white flex items-center gap-2.5">
              <Wind className="w-6 h-6 text-teal-400" />
              Guided Mindfulness & Box Breathing
            </h1>
            <p className="text-xs text-slate-400 mt-1">
              Regulate your autonomic nervous system and lower cortisol levels through paced respiration.
            </p>
          </div>

          {/* Pattern Selector */}
          <div className="flex items-center gap-2 bg-slate-950 p-1.5 rounded-xl border border-slate-800 shrink-0">
            <button
              onClick={() => handleModeChange('box')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                selectedMode === 'box' ? 'bg-teal-600 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Box 4-4-4-4
            </button>
            <button
              onClick={() => handleModeChange('relax')}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                selectedMode === 'relax' ? 'bg-teal-600 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Relaxing 4-7-8
            </button>
          </div>
        </div>
      </div>

      {/* Main Breathing Visualizer Canvas */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 sm:p-12 shadow-2xl flex flex-col items-center justify-center relative overflow-hidden min-h-[420px]">
        {/* Soft Background Glow */}
        <div className="absolute w-72 h-72 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />

        {/* Audio Toggle */}
        <button
          onClick={() => setSoundEnabled(!soundEnabled)}
          className="absolute top-6 right-6 p-2 rounded-xl bg-slate-800 text-slate-400 hover:text-white border border-slate-700 transition"
          title={soundEnabled ? 'Mute tone chimes' : 'Enable tone chimes'}
        >
          {soundEnabled ? <Volume2 className="w-4 h-4 text-teal-400" /> : <VolumeX className="w-4 h-4" />}
        </button>

        {/* Breathing Animation Rings */}
        <div className="relative flex items-center justify-center my-6">
          {/* Outer Pulsing Aura */}
          <div
            className={`w-64 h-64 sm:w-72 sm:h-72 rounded-full bg-gradient-to-tr from-teal-500/20 via-indigo-500/20 to-teal-400/20 border border-teal-500/30 flex items-center justify-center shadow-2xl ${getScaleClass()}`}
          >
            {/* Inner Core Circle */}
            <div className="w-44 h-44 sm:w-48 sm:h-48 rounded-full bg-slate-950 border border-teal-500/60 flex flex-col items-center justify-center p-4 text-center shadow-inner">
              <span className="text-xs font-bold text-teal-400 uppercase tracking-widest mb-1">
                {isActive ? currentPhase.name : 'Ready'}
              </span>
              <span className="text-4xl sm:text-5xl font-black text-white my-1">
                {isActive ? secondsLeft : pattern.phases[0].duration}
              </span>
              <span className="text-[10px] text-slate-400">Seconds</span>
            </div>
          </div>
        </div>

        {/* Dynamic Instruction */}
        <p className="text-sm font-medium text-slate-200 text-center max-w-md mt-2 mb-6 h-6">
          {isActive ? currentPhase.instruction : 'Click "Begin Session" to start paced breathing.'}
        </p>

        {/* Controls */}
        <div className="flex items-center gap-4">
          <button
            onClick={() => setIsActive(!isActive)}
            className="flex items-center gap-2 bg-teal-600 hover:bg-teal-500 text-white font-bold text-sm py-3 px-8 rounded-2xl shadow-xl shadow-teal-950/60 transition hover:scale-105"
          >
            {isActive ? (
              <>
                <Pause className="w-4 h-4" /> Pause
              </>
            ) : (
              <>
                <Play className="w-4 h-4" /> Begin Session
              </>
            )}
          </button>

          <button
            onClick={handleReset}
            className="p-3 rounded-2xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
            title="Reset"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>

        {/* Stats footer */}
        <div className="mt-8 pt-6 border-t border-slate-800/80 w-full max-w-md flex justify-around text-center text-xs text-slate-400">
          <div>
            <span className="block font-bold text-white text-base">{completedCycles}</span>
            <span>Cycles Completed</span>
          </div>
          <div>
            <span className="block font-bold text-teal-400 text-base">{pattern.name.split(' ')[0]}</span>
            <span>Current Technique</span>
          </div>
        </div>
      </div>
    </div>
  );
}
