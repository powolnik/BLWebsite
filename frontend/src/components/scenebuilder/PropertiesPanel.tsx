/**
 * BLACK LIGHT Collective — Properties Panel
 * Right-side panel in the Scene Builder showing:
 * - Transform tool selector (translate / rotate / scale)
 * - Grid, collision, and physics toggles
 * - Grid dimensions and shape controls
 * - Selected object properties (position, rotation, scale)
 * - Scene-wide physics stats (weight, CoM, balance, stability)
 * - Export / clear actions
 */

import { useSceneBuilderStore } from '../../stores/sceneBuilderStore';
import {
  Move, RotateCcw, Maximize2, Trash2, AlertTriangle,
  Activity, Grid3x3,
  Download, RefreshCw
} from 'lucide-react';
import clsx from 'clsx';

/**
 * PropertiesPanel — right sidebar displaying object properties,
 * scene physics, and action buttons.
 */
export default function PropertiesPanel() {
  const {
    selectedObjectId, sceneObjects, availableModels, collisions, physics,
    transformMode, showGrid, showCollisions, showPhysics, gridCellDisplay,
    moveSceneObject, rotateSceneObject, scaleSceneObject, removeSceneObject,
    setTransformMode, toggleGrid, toggleCollisions, togglePhysics, setGridCellDisplay,
    clearScene, getSceneJSON, engine,
    resizeGrid, gridShape, setGridShape
  } = useSceneBuilderStore();

  // Resolve selected object and its model metadata
  const selectedObj = selectedObjectId ? sceneObjects.get(selectedObjectId) : null;
  const selectedModel = selectedObj ? availableModels.find(m => m.id === selectedObj.modelId) : null;
  const objCollisions = selectedObjectId ? collisions.get(selectedObjectId) : undefined;

  // ── Property change handlers ──────────────────────

  /** Update a single position axis (cm) on the selected object */
  const handlePosChange = (axis: 'x' | 'y' | 'z', value: string) => {
    if (!selectedObj) return;
    const v = parseFloat(value) || 0;
    const pos = { ...selectedObj.position, [axis]: v };
    moveSceneObject(selectedObj.id, pos.x, pos.y, pos.z);
  };

  /** Update a single rotation axis (degrees) on the selected object */
  const handleRotChange = (axis: 'x' | 'y' | 'z', value: string) => {
    if (!selectedObj) return;
    const v = parseFloat(value) || 0;
    const rot = { ...selectedObj.rotation, [axis]: v };
    rotateSceneObject(selectedObj.id, rot.x, rot.y, rot.z);
  };

  /** Update a single scale axis on the selected object */
  const handleScaleChange = (axis: 'x' | 'y' | 'z', value: string) => {
    if (!selectedObj) return;
    const v = parseFloat(value) || 1;
    const scl = { ...selectedObj.scale, [axis]: v };
    scaleSceneObject(selectedObj.id, scl.x, scl.y, scl.z);
  };

  /** Download the scene as a JSON file */
  const handleExport = () => {
    const json = getSceneJSON();
    const blob = new Blob([JSON.stringify(json, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'scene.bl3d.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  /** Reusable numeric input row for transform properties */
  const InputRow = ({ label, value, onChange }: { label: string; value: number; onChange: (v: string) => void }) => (
    <div className="flex items-center gap-2">
      <span className="text-[10px] text-gray-500 w-3 font-mono">{label}</span>
      <input
        type="number"
        value={Math.round(value * 10) / 10}
        onChange={e => onChange(e.target.value)}
        className="flex-1 bg-[#1a1a2e] border border-[#2a2a4e] rounded px-2 py-1 text-xs text-gray-300 w-full focus:outline-none focus:border-cyan-500/50"
        step={label === 'X' || label === 'Y' || label === 'Z' ? 1 : 0.1}
      />
    </div>
  );

  return (
    <div className="w-72 bg-[#0d0d1a] border-l border-[#1a1a3e] flex flex-col h-full overflow-y-auto">
      {/* ── Transform tool selector ────────────────────── */}
      <div className="p-3 border-b border-[#1a1a3e]">
        <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Narzędzia</h3>
        <div className="flex gap-1">
          {([
            { mode: 'translate' as const, icon: Move, label: 'Przesuń' },
            { mode: 'rotate' as const, icon: RotateCcw, label: 'Obróć' },
            { mode: 'scale' as const, icon: Maximize2, label: 'Skaluj' },
          ]).map(({ mode, icon: Icon, label }) => (
            <button
              key={mode}
              onClick={() => setTransformMode(mode)}
              className={clsx(
                'flex-1 flex items-center justify-center gap-1 py-1.5 rounded text-xs transition-colors',
                transformMode === mode
                  ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                  : 'bg-[#1a1a2e] text-gray-400 border border-transparent hover:border-[#2a2a4e]'
              )}
              title={label}
            >
              <Icon size={14} />
            </button>
          ))}
        </div>

        {/* ── Visibility toggles ──────────────────────── */}
        <div className="flex gap-1 mt-2">
          <button onClick={toggleGrid} className={clsx('flex-1 py-1 rounded text-[10px]', showGrid ? 'bg-[#16213e] text-cyan-400' : 'bg-[#1a1a2e] text-gray-600')}>
            <Grid3x3 size={12} className="inline mr-1" />Siatka
          </button>
          <button onClick={toggleCollisions} className={clsx('flex-1 py-1 rounded text-[10px]', showCollisions ? 'bg-[#16213e] text-red-400' : 'bg-[#1a1a2e] text-gray-600')}>
            <AlertTriangle size={12} className="inline mr-1" />Kolizje
          </button>
          <button onClick={togglePhysics} className={clsx('flex-1 py-1 rounded text-[10px]', showPhysics ? 'bg-[#16213e] text-green-400' : 'bg-[#1a1a2e] text-gray-600')}>
            <Activity size={12} className="inline mr-1" />Fizyka
          </button>
        </div>

        {/* ── Grid cell size selector ─────────────────── */}
        <div className="mt-2 flex items-center gap-2">
          <span className="text-[10px] text-gray-500">Siatka co:</span>
          <select
            value={gridCellDisplay}
            onChange={e => setGridCellDisplay(Number(e.target.value))}
            className="flex-1 bg-[#1a1a2e] border border-[#2a2a4e] rounded px-2 py-1 text-xs text-gray-300"
          >
            <option value={10}>10cm</option>
            <option value={50}>50cm</option>
            <option value={100}>1m</option>
            <option value={200}>2m</option>
            <option value={500}>5m</option>
          </select>
        </div>
      </div>

      {/* ── Grid dimensions & shape ──────────────────── */}
      <div className="p-3 border-b border-[#1a1a3e]">
        <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">📐 Wymiary siatki</h3>

        {/* Shape selector */}
        <div className="flex gap-1 mb-2">
          {(['rectangle', 'square', 'circle'] as const).map(shape => (
            <button
              key={shape}
              onClick={() => {
                setGridShape(shape);
                const w = engine.getGridWidth() / 100;
                const h = engine.getGridHeight() / 100;
                const d = engine.getGridDepth() / 100;
                if (shape === 'square') resizeGrid(w, h, w);
                else if (shape === 'circle') resizeGrid(Math.max(w, d), h, Math.max(w, d));
                else resizeGrid(w, h, d);
              }}
              className={clsx(
                'flex-1 py-1 rounded text-[10px] transition-colors',
                gridShape === shape ? 'bg-purple-500/20 text-purple-400 border border-purple-500/30' : 'bg-[#1a1a2e] text-gray-500'
              )}
            >
              {shape === 'rectangle' ? '▬ Prostokąt' : shape === 'square' ? '■ Kwadrat' : '● Koło'}
            </button>
          ))}
        </div>

        {/* Dimension inputs */}
        <div className="grid grid-cols-3 gap-1">
          <div>
            <span className="text-[10px] text-gray-500">Szer. (m)</span>
            <input
              type="number"
              value={engine.getGridWidth() / 100}
              min={5}
              max={100}
              step={1}
              onChange={e => {
                const v = Number(e.target.value) || 20;
                resizeGrid(v, engine.getGridHeight() / 100, gridShape === 'square' || gridShape === 'circle' ? v : engine.getGridDepth() / 100);
              }}
              className="w-full bg-[#1a1a2e] border border-[#2a2a4e] rounded px-2 py-1 text-xs text-gray-300 focus:outline-none focus:border-cyan-500/50"
            />
          </div>
          <div>
            <span className="text-[10px] text-gray-500">Wys. (m)</span>
            <input
              type="number"
              value={engine.getGridHeight() / 100}
              min={3}
              max={50}
              step={1}
              onChange={e => {
                const v = Number(e.target.value) || 10;
                resizeGrid(engine.getGridWidth() / 100, v, engine.getGridDepth() / 100);
              }}
              className="w-full bg-[#1a1a2e] border border-[#2a2a4e] rounded px-2 py-1 text-xs text-gray-300 focus:outline-none focus:border-cyan-500/50"
            />
          </div>
          <div>
            <span className="text-[10px] text-gray-500">Głęb. (m)</span>
            <input
              type="number"
              value={engine.getGridDepth() / 100}
              min={5}
              max={100}
              step={1}
              disabled={gridShape === 'square' || gridShape === 'circle'}
              onChange={e => {
                const v = Number(e.target.value) || 20;
                resizeGrid(engine.getGridWidth() / 100, engine.getGridHeight() / 100, v);
              }}
              className="w-full bg-[#1a1a2e] border border-[#2a2a4e] rounded px-2 py-1 text-xs text-gray-300 focus:outline-none focus:border-cyan-500/50 disabled:opacity-40"
            />
          </div>
        </div>
      </div>

      {/* ── Selected object properties ─────────────────── */}
      {selectedObj ? (
        <div className="p-3 border-b border-[#1a1a3e]">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-xs font-bold text-yellow-400 uppercase tracking-wider">
              {selectedModel?.name || `Object #${selectedObj.id}`}
            </h3>
            <button
              onClick={() => removeSceneObject(selectedObj.id)}
              className="p-1 rounded hover:bg-red-500/20 text-gray-400 hover:text-red-400 transition-colors"
            >
              <Trash2 size={14} />
            </button>
          </div>

          {/* Model metadata */}
          {selectedModel && (
            <div className="text-[10px] text-gray-500 mb-2">
              {selectedModel.category.icon} {selectedModel.category.name} · {selectedModel.weight}kg · ⚡{selectedModel.power_consumption}W
            </div>
          )}

          {/* Collision warning badge */}
          {objCollisions && objCollisions.length > 0 && (
            <div className="bg-red-500/10 border border-red-500/20 rounded px-2 py-1 mb-2 flex items-center gap-1">
              <AlertTriangle size={12} className="text-red-400" />
              <span className="text-[10px] text-red-400">Kolizja z {objCollisions.length} obiektami!</span>
            </div>
          )}

          {/* Position (cm) */}
          <div className="mb-2">
            <span className="text-[10px] text-gray-400 font-medium">Pozycja (cm)</span>
            <div className="grid grid-cols-3 gap-1 mt-1">
              <InputRow label="X" value={selectedObj.position.x} onChange={v => handlePosChange('x', v)} />
              <InputRow label="Y" value={selectedObj.position.y} onChange={v => handlePosChange('y', v)} />
              <InputRow label="Z" value={selectedObj.position.z} onChange={v => handlePosChange('z', v)} />
            </div>
          </div>

          {/* Rotation (degrees) */}
          <div className="mb-2">
            <span className="text-[10px] text-gray-400 font-medium">Rotacja (°)</span>
            <div className="grid grid-cols-3 gap-1 mt-1">
              <InputRow label="X" value={selectedObj.rotation.x} onChange={v => handleRotChange('x', v)} />
              <InputRow label="Y" value={selectedObj.rotation.y} onChange={v => handleRotChange('y', v)} />
              <InputRow label="Z" value={selectedObj.rotation.z} onChange={v => handleRotChange('z', v)} />
            </div>
          </div>

          {/* Scale */}
          <div className="mb-2">
            <span className="text-[10px] text-gray-400 font-medium">Skala</span>
            <div className="grid grid-cols-3 gap-1 mt-1">
              <InputRow label="X" value={selectedObj.scale.x} onChange={v => handleScaleChange('x', v)} />
              <InputRow label="Y" value={selectedObj.scale.y} onChange={v => handleScaleChange('y', v)} />
              <InputRow label="Z" value={selectedObj.scale.z} onChange={v => handleScaleChange('z', v)} />
            </div>
          </div>

          {/* Computed AABB info */}
          <div className="text-[10px] text-gray-500 bg-[#1a1a2e] rounded p-2">
            📐 AABB: {Math.round(selectedObj.bboxSize.x * selectedObj.scale.x)}×
            {Math.round(selectedObj.bboxSize.y * selectedObj.scale.y)}×
            {Math.round(selectedObj.bboxSize.z * selectedObj.scale.z)}cm
          </div>
        </div>
      ) : (
        <div className="p-3 border-b border-[#1a1a3e] text-center text-xs text-gray-500">
          Kliknij obiekt na scenie lub dodaj z biblioteki
        </div>
      )}

      {/* ── Scene physics summary ──────────────────────── */}
      <div className="p-3 border-b border-[#1a1a3e]">
        <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">⚖️ Fizyka sceny</h3>

        <div className="space-y-1.5 text-xs">
          <div className="flex justify-between">
            <span className="text-gray-500">Obiekty:</span>
            <span className="text-gray-300">{engine.getObjectCount()}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500">Masa całkowita:</span>
            <span className="text-gray-300">{physics.totalWeight.toFixed(1)} kg</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500">Środek masy:</span>
            <span className="text-gray-300 text-[10px]">
              ({Math.round(physics.centerOfMass.x)}, {Math.round(physics.centerOfMass.y)}, {Math.round(physics.centerOfMass.z)})
            </span>
          </div>
          {/* Balance score bar */}
          <div className="flex justify-between items-center">
            <span className="text-gray-500">Balans:</span>
            <div className="flex items-center gap-1">
              <div className="w-16 h-1.5 bg-[#1a1a2e] rounded-full overflow-hidden">
                <div
                  className={clsx('h-full rounded-full transition-all',
                    physics.balanceScore > 0.7 ? 'bg-green-500' :
                    physics.balanceScore > 0.4 ? 'bg-yellow-500' : 'bg-red-500'
                  )}
                  style={{ width: `${physics.balanceScore * 100}%` }}
                />
              </div>
              <span className="text-gray-300">{Math.round(physics.balanceScore * 100)}%</span>
            </div>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500">Stabilność:</span>
            <span className={physics.isStable ? 'text-green-400' : 'text-red-400'}>
              {physics.isStable ? '✅ Stabilna' : '⚠️ Niestabilna'}
            </span>
          </div>
          {physics.maxLoadPerArea > 0 && (
            <div className="flex justify-between">
              <span className="text-gray-500">Nacisk:</span>
              <span className="text-gray-300">{physics.maxLoadPerArea.toFixed(4)} kg/cm²</span>
            </div>
          )}
        </div>
      </div>

      {/* ── Action buttons ─────────────────────────────── */}
      <div className="p-3 space-y-2">
        <button
          onClick={handleExport}
          className="w-full flex items-center justify-center gap-2 py-2 bg-cyan-500/20 text-cyan-400 rounded text-xs hover:bg-cyan-500/30 transition-colors border border-cyan-500/20"
        >
          <Download size={14} /> Eksportuj scenę (JSON)
        </button>
        <button
          onClick={clearScene}
          className="w-full flex items-center justify-center gap-2 py-2 bg-red-500/10 text-red-400 rounded text-xs hover:bg-red-500/20 transition-colors border border-red-500/20"
        >
          <RefreshCw size={14} /> Wyczyść scenę
        </button>
      </div>

      {/* ── Scene info footer ──────────────────────────── */}
      <div className="p-3 mt-auto border-t border-[#1a1a3e] text-[10px] text-gray-600">
        Siatka: {engine.getGridWidth()/100}m × {engine.getGridHeight()/100}m × {engine.getGridDepth()/100}m
        <br />Rozdzielczość: {engine.getCellSize()}cm
        <br />Engine: TypeScript (WASM-ready)
      </div>
    </div>
  );
}
