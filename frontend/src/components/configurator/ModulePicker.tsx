import { useConfiguratorStore } from '../../store/configuratorStore';
import ModuleIcon from './ModuleIcon';
import { Plus } from 'lucide-react';

export default function ModulePicker() {
  const { categories, activeCategory, setActiveCategory, addModule } = useConfiguratorStore();

  const activeCat = categories.find(c => c.slug === activeCategory);

  return (
    <div className="h-full flex flex-col bg-[var(--color-dark-card)] rounded-xl border border-[var(--color-dark-border)] overflow-hidden">
      {/* Category tabs */}
      <div className="flex overflow-x-auto border-b border-[var(--color-dark-border)] p-2 gap-1 shrink-0">
        {categories.map(cat => (
          <button
            key={cat.slug}
            onClick={() => setActiveCategory(cat.slug)}
            className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-medium whitespace-nowrap transition-all ${
              activeCategory === cat.slug
                ? 'text-black'
                : 'text-[var(--color-text-secondary)] hover:text-white hover:bg-white/5'
            }`}
            style={activeCategory === cat.slug ? { backgroundColor: cat.color } : {}}
          >
            <span>{cat.icon}</span>
            <span>{cat.name}</span>
          </button>
        ))}
      </div>

      {/* Category description */}
      {activeCat && (
        <div className="px-4 py-2 text-xs text-[var(--color-text-secondary)] border-b border-[var(--color-dark-border)] shrink-0">
          {activeCat.description}
        </div>
      )}

      {/* Module list */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {activeCat?.components.filter(c => c.is_available).map(comp => (
          <div
            key={comp.id}
            className="group p-3 rounded-lg bg-[var(--color-dark-bg)] border border-[var(--color-dark-border)] hover:border-opacity-50 transition-all cursor-pointer"
            style={{ '--hover-color': comp.color } as React.CSSProperties}
            onClick={() => addModule(comp)}
          >
            <div className="flex items-start gap-3">
              <div className="shrink-0 w-10 h-10 rounded-lg flex items-center justify-center"
                   style={{ backgroundColor: `${comp.color}15` }}>
                <ModuleIcon iconName={comp.icon_name} color={comp.color} size={24} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <h4 className="font-medium text-sm text-white">{comp.name}</h4>
                  <button
                    className="shrink-0 w-6 h-6 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                    style={{ backgroundColor: comp.color, color: '#000' }}
                    onClick={(e) => { e.stopPropagation(); addModule(comp); }}
                  >
                    <Plus className="w-3.5 h-3.5" />
                  </button>
                </div>
                <p className="text-xs text-[var(--color-text-secondary)] mt-0.5 line-clamp-1">{comp.short_desc || comp.description}</p>
                <div className="flex items-center gap-3 mt-1.5 text-xs">
                  <span className="font-bold" style={{ color: comp.color }}>
                    {parseFloat(comp.price).toLocaleString('pl-PL')} PLN
                  </span>
                  {comp.power_consumption > 0 && (
                    <span className="text-[var(--color-text-secondary)]">⚡ {comp.power_consumption}W</span>
                  )}
                  <span className="text-[var(--color-text-secondary)]">⚖️ {comp.weight_kg}kg</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
