/**
 * BLACK LIGHT Collective — Model Library Panel
 * Left-side panel in the Scene Builder that lists available 3D models
 * grouped by category with search filtering and one-click placement.
 */

import { useState, useEffect } from 'react';
import { useSceneBuilderStore } from '../../stores/sceneBuilderStore';
import { Package, ChevronDown, ChevronRight, Plus, Search } from 'lucide-react';
import type { Model3D, Model3DCategory } from '../../engine/types';

// ═══════════════════════════════════════════════════════
// Demo catalogue — used when the Django API is unavailable
// ═══════════════════════════════════════════════════════

const DEMO_MODELS: Model3D[] = [
  { id: 1, category: { id: 1, name: 'Obiekty UFO', slug: 'ufo', icon: '🛸', order: 1 }, name: 'UFO Ø2m', slug: 'ufo-2m', description: 'Mały obiekt UFO', model_file: '', model_file_url: '', thumbnail: null, bbox_width: 200, bbox_height: 80, bbox_depth: 200, weight: 15, max_instances: 5, price_per_unit: 500, power_consumption: 200, is_active: true },
  { id: 2, category: { id: 1, name: 'Obiekty UFO', slug: 'ufo', icon: '🛸', order: 1 }, name: 'UFO Ø4m', slug: 'ufo-4m', description: 'Średni obiekt UFO', model_file: '', model_file_url: '', thumbnail: null, bbox_width: 400, bbox_height: 120, bbox_depth: 400, weight: 45, max_instances: 3, price_per_unit: 1200, power_consumption: 500, is_active: true },
  { id: 3, category: { id: 1, name: 'Obiekty UFO', slug: 'ufo', icon: '🛸', order: 1 }, name: 'UFO Ø6m', slug: 'ufo-6m', description: 'Duży obiekt UFO', model_file: '', model_file_url: '', thumbnail: null, bbox_width: 600, bbox_height: 180, bbox_depth: 600, weight: 85, max_instances: 2, price_per_unit: 2500, power_consumption: 800, is_active: true },
  { id: 4, category: { id: 2, name: 'Las/Drzewa', slug: 'trees', icon: '🌲', order: 2 }, name: 'Drzewo LED 3m', slug: 'tree-3m', description: 'Świecące drzewo LED', model_file: '', model_file_url: '', thumbnail: null, bbox_width: 150, bbox_height: 300, bbox_depth: 150, weight: 25, max_instances: 20, price_per_unit: 300, power_consumption: 150, is_active: true },
  { id: 5, category: { id: 2, name: 'Las/Drzewa', slug: 'trees', icon: '🌲', order: 2 }, name: 'Drzewo LED 5m', slug: 'tree-5m', description: 'Duże świecące drzewo', model_file: '', model_file_url: '', thumbnail: null, bbox_width: 250, bbox_height: 500, bbox_depth: 250, weight: 50, max_instances: 10, price_per_unit: 600, power_consumption: 300, is_active: true },
  { id: 6, category: { id: 3, name: 'Lasery', slug: 'lasers', icon: '✨', order: 3 }, name: 'Laser RGB Compact', slug: 'laser-rgb', description: 'Kompaktowy laser RGB', model_file: '', model_file_url: '', thumbnail: null, bbox_width: 30, bbox_height: 20, bbox_depth: 30, weight: 5, max_instances: 20, price_per_unit: 200, power_consumption: 50, is_active: true },
  { id: 7, category: { id: 3, name: 'Lasery', slug: 'lasers', icon: '✨', order: 3 }, name: 'Laser 5W Show', slug: 'laser-5w', description: 'Laser show 5W', model_file: '', model_file_url: '', thumbnail: null, bbox_width: 40, bbox_height: 25, bbox_depth: 40, weight: 8, max_instances: 10, price_per_unit: 500, power_consumption: 200, is_active: true },
  { id: 8, category: { id: 4, name: 'LED', slug: 'led', icon: '💡', order: 4 }, name: 'Panel LED 1x1m', slug: 'led-panel', description: 'Panel LED 1x1m', model_file: '', model_file_url: '', thumbnail: null, bbox_width: 100, bbox_height: 100, bbox_depth: 10, weight: 8, max_instances: 50, price_per_unit: 150, power_consumption: 100, is_active: true },
  { id: 9, category: { id: 4, name: 'LED', slug: 'led', icon: '💡', order: 4 }, name: 'Pixel Tube 1m', slug: 'pixel-tube', description: 'LED pixel tube', model_file: '', model_file_url: '', thumbnail: null, bbox_width: 5, bbox_height: 100, bbox_depth: 5, weight: 2, max_instances: 100, price_per_unit: 50, power_consumption: 20, is_active: true },
  { id: 10, category: { id: 5, name: 'Konstrukcje', slug: 'constructions', icon: '🔧', order: 5 }, name: 'Truss 3m', slug: 'truss-3m', description: 'Kratownica 3m', model_file: '', model_file_url: '', thumbnail: null, bbox_width: 30, bbox_height: 30, bbox_depth: 300, weight: 35, max_instances: 20, price_per_unit: 200, power_consumption: 0, is_active: true },
  { id: 11, category: { id: 5, name: 'Konstrukcje', slug: 'constructions', icon: '🔧', order: 5 }, name: 'Arch 6m', slug: 'arch-6m', description: 'Łuk dekoracyjny 6m', model_file: '', model_file_url: '', thumbnail: null, bbox_width: 600, bbox_height: 400, bbox_depth: 30, weight: 80, max_instances: 5, price_per_unit: 800, power_consumption: 0, is_active: true },
  { id: 12, category: { id: 5, name: 'Konstrukcje', slug: 'constructions', icon: '🔧', order: 5 }, name: 'Totem 4m', slug: 'totem-4m', description: 'Totem dekoracyjny', model_file: '', model_file_url: '', thumbnail: null, bbox_width: 50, bbox_height: 400, bbox_depth: 50, weight: 40, max_instances: 10, price_per_unit: 400, power_consumption: 100, is_active: true },
  { id: 13, category: { id: 6, name: 'Efekty', slug: 'effects', icon: '💨', order: 6 }, name: 'Wytwornica mgły', slug: 'fog-machine', description: 'Wytwornica mgły', model_file: '', model_file_url: '', thumbnail: null, bbox_width: 40, bbox_height: 30, bbox_depth: 40, weight: 12, max_instances: 10, price_per_unit: 100, power_consumption: 1000, is_active: true },
  { id: 14, category: { id: 6, name: 'Efekty', slug: 'effects', icon: '💨', order: 6 }, name: 'CO2 Jet', slug: 'co2-jet', description: 'Wyrzutnia CO2', model_file: '', model_file_url: '', thumbnail: null, bbox_width: 20, bbox_height: 60, bbox_depth: 20, weight: 15, max_instances: 8, price_per_unit: 300, power_consumption: 50, is_active: true },
  { id: 15, category: { id: 6, name: 'Efekty', slug: 'effects', icon: '💨', order: 6 }, name: 'Confetti Cannon', slug: 'confetti', description: 'Wyrzutnia confetti', model_file: '', model_file_url: '', thumbnail: null, bbox_width: 15, bbox_height: 50, bbox_depth: 15, weight: 10, max_instances: 6, price_per_unit: 250, power_consumption: 30, is_active: true },
];

/**
 * Model Library — left sidebar in the Scene Builder.
 * Renders an expandable, searchable tree of 3D model categories.
 * Clicking a model places it at the centre of the grid.
 */
export default function ModelLibrary() {
  const { availableModels, setAvailableModels, addModelToScene, engine } = useSceneBuilderStore();
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set(['ufo', 'led']));
  const [searchQuery, setSearchQuery] = useState('');

  // Seed demo models on first mount (replace with API call later)
  useEffect(() => {
    if (availableModels.length === 0) {
      setAvailableModels(DEMO_MODELS);
    }
  }, []);

  const models = availableModels.length > 0 ? availableModels : DEMO_MODELS;

  // Group models by category slug for the tree view
  const categories = new Map<string, { category: Model3DCategory; models: Model3D[] }>();
  for (const model of models) {
    const key = model.category.slug;
    if (!categories.has(key)) {
      categories.set(key, { category: model.category, models: [] });
    }
    categories.get(key)!.models.push(model);
  }

  /** Toggle a category's expanded/collapsed state */
  const toggleCategory = (slug: string) => {
    const next = new Set(expandedCategories);
    if (next.has(slug)) next.delete(slug);
    else next.add(slug);
    setExpandedCategories(next);
  };

  /** Place a model at the centre of the grid (Y at half-height so it sits on ground) */
  const handleAddModel = (model: Model3D) => {
    const cx = engine.getGridWidth() / 2;
    const cy = model.bbox_height / 2;
    const cz = engine.getGridDepth() / 2;
    addModelToScene(model, cx, cy, cz);
  };

  // Filter categories and models by search query
  const filteredCategories = Array.from(categories.values()).filter(cat => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return cat.category.name.toLowerCase().includes(q) ||
           cat.models.some(m => m.name.toLowerCase().includes(q));
  });

  return (
    <div className="w-72 bg-[#0d0d1a] border-r border-[#1a1a3e] flex flex-col h-full">
      {/* Header */}
      <div className="p-3 border-b border-[#1a1a3e]">
        <h2 className="text-sm font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-2">
          <Package size={16} />
          Biblioteka modeli
        </h2>
        {/* Search input */}
        <div className="mt-2 relative">
          <Search size={14} className="absolute left-2 top-1/2 -translate-y-1/2 text-gray-500" />
          <input
            type="text"
            placeholder="Szukaj..."
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            className="w-full bg-[#1a1a2e] border border-[#2a2a4e] rounded px-7 py-1.5 text-xs text-gray-300 placeholder:text-gray-600 focus:outline-none focus:border-cyan-500/50"
          />
        </div>
      </div>

      {/* Scrollable model list */}
      <div className="flex-1 overflow-y-auto">
        {filteredCategories.map(({ category, models: catModels }) => {
          const isExpanded = expandedCategories.has(category.slug);
          const filtered = searchQuery
            ? catModels.filter(m => m.name.toLowerCase().includes(searchQuery.toLowerCase()))
            : catModels;

          return (
            <div key={category.slug}>
              {/* Category header toggle */}
              <button
                onClick={() => toggleCategory(category.slug)}
                className="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-300 hover:bg-[#1a1a2e] transition-colors"
              >
                <span>{category.icon}</span>
                <span className="flex-1 text-left font-medium">{category.name}</span>
                <span className="text-xs text-gray-500">{filtered.length}</span>
                {isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
              </button>

              {/* Expanded model items */}
              {isExpanded && (
                <div className="pb-1">
                  {filtered.map(model => (
                    <button
                      key={model.id}
                      onClick={() => handleAddModel(model)}
                      className="w-full flex items-center gap-2 px-4 py-2 text-left hover:bg-[#16213e] transition-colors group"
                    >
                      {/* Thumbnail or category icon fallback */}
                      <div className="w-8 h-8 bg-[#1a1a3e] rounded flex items-center justify-center text-lg group-hover:bg-cyan-500/20">
                        {model.thumbnail ? (
                          <img src={model.thumbnail} alt="" className="w-full h-full object-cover rounded" />
                        ) : (
                          <span className="text-xs">{category.icon}</span>
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="text-xs font-medium text-gray-300 truncate">{model.name}</div>
                        <div className="text-[10px] text-gray-500">
                          {model.bbox_width}×{model.bbox_height}×{model.bbox_depth}cm · {model.weight}kg
                        </div>
                      </div>
                      <Plus size={14} className="text-gray-600 group-hover:text-cyan-400 transition-colors" />
                    </button>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
