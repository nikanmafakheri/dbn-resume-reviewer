import { useState } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import { LanguageProvider } from './context/LanguageContext';
import { Header } from './components/layout/Header';
import { Footer } from './components/layout/Footer';
import { UploadSection } from './components/features/UploadSection';
import { AnalysisResults } from './components/features/AnalysisResults';
import { StandardSection } from './components/features/StandardSection';
import { HowItWorks } from './components/features/HowItWorks';
import { API_BASE_URL } from './lib/api';

function App() {
  const [analysisId, setAnalysisId] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const handleFile = async (file: File) => {
    setIsUploading(true);
    setUploadError(null);

    try {
      // 1. Upload
      const formData = new FormData();
      formData.append('file', file);
      const uploadRes = await fetch(`${API_BASE_URL}/resumes/upload`, {
        method: 'POST',
        body: formData,
      });
      if (!uploadRes.ok) throw new Error('Upload failed');
      const resume = await uploadRes.json();

      // 2. Trigger analysis
      const analyzeRes = await fetch(`${API_BASE_URL}/resumes/${resume.id}/analyze`, {
        method: 'POST',
      });
      if (!analyzeRes.ok) throw new Error('Analysis trigger failed');
      const analysis = await analyzeRes.json();

      setAnalysisId(analysis.id);
      // Scroll results into view once analysis starts
      requestAnimationFrame(() => {
        document.getElementById('results')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    } catch (err) {
      setUploadError(err instanceof Error ? err.message : 'Something went wrong');
    } finally {
      setIsUploading(false);
    }
  };

  const handleRetry = () => {
    setAnalysisId(null);
  };

  const handleReset = () => {
    setAnalysisId(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <ThemeProvider>
      <LanguageProvider>
        <div id="top" className="relative min-h-screen overflow-x-clip bg-[var(--background)] text-[var(--text-primary)] transition-colors">
          <Header />
          <main className="hero-glow">
            <UploadSection
              onFileSelected={handleFile}
              isUploading={isUploading}
              error={uploadError}
            />
            <HowItWorks />
            <AnalysisResults analysisId={analysisId} onRetry={handleRetry} onReset={handleReset} />
            <StandardSection />
          </main>
          <Footer />
        </div>
      </LanguageProvider>
    </ThemeProvider>
  );
}

export default App;
