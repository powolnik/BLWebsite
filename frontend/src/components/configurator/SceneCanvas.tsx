import { useConfiguratorStore } from '../../store/configuratorStore';
import ModuleIcon from './ModuleIcon';

export default function SceneCanvas() {
  const { sceneItems, selectedTemplate, totalPower, totalWeight, itemCount } = useConfiguratorStore();

  const pw = totalPower();
  const wt = totalWeight();
  const ic = itemCount();

  return (
    <div className="h-full flex flex-col">
      {/* Canvas area */}
      <div className="flex-1 relative bg-[var(--color-dark-bg)] rounded-xl border border-[var(--color-dark-border)] overflow-hidden"
           style={{
             backgroundImage: 'radial-gradient(circle, rgba(255,255,255,0.03) 1px, transparent 1px)',
             backgroundSize: '20px 20px',
           }}>

        {/* Stage label */}
        <div className="absolute top-3 left-3 text-xs text-[var(--color-text-secondary)] font-mono uppercase tracking-wider">
          {selectedTemplate ? `📐 ${selectedTemplate.name} (${selectedTemplate.width}×${selectedTemplate.depth}m)` : '📐 Scena'}
        </div>

        {/* Stats bar */}
        <div className="absolute top-3 right-3 flex gap-3 text-xs font-mono">
          <span className="text-[var(--color-text-secondary)]">🎯 {ic} modułów</span>
          <span className="text-yellow-400">⚡ {pw.toLocaleString()}W</span>
          <span className="text-blue-400">⚖️ {wt.toFixed(0)}kg</span>
        </div>

        {/* Stage area outline */}
        <div className="absolute inset-8 top-12 border border-dashed border-white/10 rounded-lg flex items-center justify-center">
          {sceneItems.length === 0 ? (
            <div className="text-center text-[var(--color-text-secondary)]">
              <div className="text-4xl mb-2 opacity-30">🎭</div>
              <p className="text-sm">Kliknij moduł po lewej, aby dodać go do sceny</p>
              <p className="text-xs mt-1 opacity-50">Twórz swoją unikalną scenę z modułów Synapse</p>
            </div>
          ) : (
            <div className="w-full h-full p-4 flex flex-wrap content-center justify-center gap-3">
              {sceneItems.map((item) => (
                <div
                  key={item.id}
                  className="relative group flex flex-col items-center justify-center rounded-xl p-3 transition-all hover:scale-105"
                  style={{
                    backgroundColor: `${item.component.color}12`,
                    border: `1px solid ${item.component.color}40`,
                    boxShadow: `0 0 20px ${item.component.color}15`,
                    minWidth: `${Math.max(80, parseFloat(item.component.width_m) * 20)}px`,
                    minHeight: '80px',
                  }}
                >
                  <ModuleIcon
                    iconName={item.component.icon_name}
                    color={item.component.color}
                    size={32}
                  />
                  <span className="text-xs font-medium mt-1 text-white/80">{item.component.name}</span>
                  {item.quantity > 1 && (
                    <span
                      className="absolute -top-2 -right-2 w-5 h-5 rounded-full text-xs font-bold flex items-center justify-center text-black"
                      style={{ backgroundColor: item.component.color }}
                    >
                      {item.quantity}
                    </span>
                  )}
                  {/* Glow ring */}
                  <div
                    className="absolute inset-0 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none"
                    style={{ boxShadow: `0 0 30px ${item.component.color}30, inset 0 0 20px ${item.component.color}10` }}
                  />
                </div>
              ))}
            </div>
          )}
        </div>

        {/* DJ booth indicator */}
        <div className="absolute bottom-3 left-1/2 -translate-x-1/2 px-4 py-1 rounded-full bg-white/5 border border-white/10 text-xs text-[var(--color-text-secondary)] font-mono">
          🎧 DJ BOOTH
        </div>
      </div>
    </div>
  );
}
