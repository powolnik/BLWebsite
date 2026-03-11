/**
 * BLACK LIGHT Collective — Scene Builder Page
 * Full-screen 3D scene builder with a three-column layout:
 *   Left:   Model Library (asset picker)
 *   Centre: 3D Canvas (React Three Fiber)
 *   Right:  Properties Panel (transforms, physics, actions)
 *
 * Includes a top bar with grid info and a toggleable help overlay.
 */

import { useState } from 'react';
import ModelLibrary from '../components/scenebuilder/ModelLibrary';
import SceneCanvas from '../components/scenebuilder/SceneCanvas';
import PropertiesPanel from '../components/scenebuilder/PropertiesPanel';
import { useSceneBuilderStore } from '../stores/sceneBuilderStore';
import { Box, Keyboard } from 'lucide-react';

/** Scene Builder page — occupies the full viewport below the navbar */
export default function SceneBuilder() {
  const { engine } = useSceneBuilderStore();
  const [showHelp, setShowHelp] = useState(false);

  return (
    <div className="h-[calc(100vh-64px)] flex flex-col bg-[#0a0a14]">
      {/* Top bar */}
      <div className="h-10 bg-[#0d0d1a] border-b border-[#1a1a3e] flex items-center px-4 gap-4 shrink-0">
        <div className="flex items-center gap-2 text-cyan-400">
          <Box size={16} />
          <span className="text-sm font-bold tracking-wider">3D SCENE BUILDER</span>
        </div>
        <div className="text-[10px] text-gray-500">
          BLACK LIGHT Collective · Grid: {engine.getGridWidth()/100}m × {engine.getGridHeight()/100}m × {engine.getGridDepth()/100}m · 1cm precision
        </div>
        <div className="ml-auto">
          <button
            onClick={() => setShowHelp(!showHelp)}
            className="text-xs text-gray-500 hover:text-cyan-400 flex items-center gap-1"
          >
            <Keyboard size={12} /> Pomoc
          </button>
        </div>
      </div>

      {/* Help overlay */}
      {showHelp && (
        <div className="absolute inset-0 z-50 bg-black/80 flex items-center justify-center" onClick={() => setShowHelp(false)}>
          <div className="bg-[#0d0d1a] border border-[#1a1a3e] rounded-lg p-6 max-w-md" onClick={e => e.stopPropagation()}>
            <h3 className="text-cyan-400 font-bold mb-4">🎮 Sterowanie</h3>
            <div className="space-y-2 text-sm text-gray-300">
              <p>🖱️ <strong>LPM + przeciągnij</strong> — obracaj kamerę</p>
              <p>🖱️ <strong>PPM + przeciągnij</strong> — przesuwaj kamerę</p>
              <p>🔄 <strong>Scroll</strong> — zoom</p>
              <p>👆 <strong>Klik na obiekt</strong> — zaznacz</p>
              <p>📦 <strong>Klik na model w bibliotece</strong> — dodaj na scenę</p>
              <p>🗑️ <strong>Delete</strong> — usuń zaznaczony obiekt</p>
            </div>
            <button onClick={() => setShowHelp(false)} className="mt-4 w-full py-2 bg-cyan-500/20 text-cyan-400 rounded text-sm">
              Zamknij
            </button>
          </div>
        </div>
      )}

      {/* Main three-column layout */}
      <div className="flex-1 flex overflow-hidden">
        <ModelLibrary />
        <div className="flex-1 relative">
          <SceneCanvas />
        </div>
        <PropertiesPanel />
      </div>
    </div>
  );
}
