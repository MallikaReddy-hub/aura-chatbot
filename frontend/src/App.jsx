import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import ChatView from './components/ChatView';
import AssessmentView from './components/AssessmentView';
import MoodTrackerView from './components/MoodTrackerView';
import BreathingExercise from './components/BreathingExercise';
import ResourcesView from './components/ResourcesView';
import CrisisModal from './components/CrisisModal';
import SettingsModal from './components/SettingsModal';

export default function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [isCrisisOpen, setIsCrisisOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [sessionId, setSessionId] = useState('user_session_1');

  useEffect(() => {
    // Load stored API key and session
    const savedKey = localStorage.getItem('aura_gemini_api_key');
    if (savedKey) setApiKey(savedKey);

    let storedSession = localStorage.getItem('aura_session_id');
    if (!storedSession) {
      storedSession = 'user_' + Math.random().toString(36).substring(2, 9);
      localStorage.setItem('aura_session_id', storedSession);
    }
    setSessionId(storedSession);
  }, []);

  const handleSaveApiKey = (newKey) => {
    setApiKey(newKey);
    localStorage.setItem('aura_gemini_api_key', newKey);
  };

  const handleClearHistory = () => {
    const newSession = 'user_' + Math.random().toString(36).substring(2, 9);
    localStorage.setItem('aura_session_id', newSession);
    setSessionId(newSession);
    window.location.reload();
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col antialiased">
      {/* Top Navigation */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenCrisis={() => setIsCrisisOpen(true)}
        onOpenSettings={() => setIsSettingsOpen(true)}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6">
        {activeTab === 'chat' && (
          <ChatView
            apiKey={apiKey}
            sessionId={sessionId}
            onOpenCrisis={() => setIsCrisisOpen(true)}
          />
        )}

        {activeTab === 'assessments' && (
          <AssessmentView
            sessionId={sessionId}
            onOpenCrisis={() => setIsCrisisOpen(true)}
          />
        )}

        {activeTab === 'moods' && (
          <MoodTrackerView sessionId={sessionId} />
        )}

        {activeTab === 'breathing' && (
          <BreathingExercise />
        )}

        {activeTab === 'resources' && (
          <ResourcesView onOpenCrisis={() => setIsCrisisOpen(true)} />
        )}
      </main>

      {/* Modals */}
      <CrisisModal
        isOpen={isCrisisOpen}
        onClose={() => setIsCrisisOpen(false)}
      />

      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        apiKey={apiKey}
        onSaveApiKey={handleSaveApiKey}
        onClearHistory={handleClearHistory}
      />
    </div>
  );
}
