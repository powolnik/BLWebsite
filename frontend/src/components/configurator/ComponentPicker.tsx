import type { ComponentCategory } from '../../types';
import Card from '../ui/Card';
import Button from '../ui/Button';

export default function ComponentPicker({ categories, onAddItem }: { categories: ComponentCategory[]; onAddItem: (id: number) => void }) {
  return (
    <div className="space-y-6">
      {categories.map(cat => (
        <div key={cat.id}>
          <h3 className="text-lg font-semibold mb-3">{cat.name}</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {cat.components.filter(c => c.is_available).map(comp => (
              <Card key={comp.id} className="p-3">
                <div className="flex gap-3">
                  <img src={comp.image} alt={comp.name} className="w-16 h-16 rounded-lg object-cover" />
                  <div className="flex-1 min-w-0">
                    <h4 className="font-medium text-sm truncate">{comp.name}</h4>
                    <p className="text-xs text-[var(--color-text-secondary)] line-clamp-1">{comp.description}</p>
                    <div className="flex items-center justify-between mt-2">
                      <span className="text-sm font-bold neon-text">{comp.price} PLN</span>
                      <Button size="sm" onClick={() => onAddItem(comp.id)}>Dodaj</Button>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
