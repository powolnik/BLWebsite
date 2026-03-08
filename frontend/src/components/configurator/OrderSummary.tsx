import type { SceneOrder } from '../../types';
import { Trash2 } from 'lucide-react';
import Button from '../ui/Button';

export default function OrderSummary({ order, onRemoveItem, onSubmit, isLoading }: { order: SceneOrder; onRemoveItem: (id: number) => void; onSubmit: () => void; isLoading: boolean }) {
  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">Podsumowanie</h3>
      <div className="space-y-2 text-sm">
        <div className="flex justify-between text-[var(--color-text-secondary)]"><span>Wydarzenie:</span><span className="text-white">{order.event_name}</span></div>
        <div className="flex justify-between text-[var(--color-text-secondary)]"><span>Data:</span><span className="text-white">{order.event_date}</span></div>
      </div>
      <div className="border-t border-[var(--color-dark-border)] pt-4">
        <h4 className="font-medium mb-2">Komponenty ({order.items.length})</h4>
        <div className="space-y-2 max-h-60 overflow-y-auto">
          {order.items.map(item => (
            <div key={item.id} className="flex items-center justify-between p-2 bg-[var(--color-dark-bg)] rounded-lg">
              <div className="flex-1 min-w-0"><span className="text-sm font-medium">{item.component_name}</span><span className="text-xs text-[var(--color-text-secondary)] ml-2">x{item.quantity}</span></div>
              <div className="flex items-center gap-2"><span className="text-sm neon-text">{item.subtotal} PLN</span><button onClick={() => onRemoveItem(item.id)} className="p-1 hover:text-[var(--color-neon-pink)]"><Trash2 className="w-3 h-3" /></button></div>
            </div>
          ))}
        </div>
      </div>
      <div className="border-t border-[var(--color-dark-border)] pt-4">
        <div className="flex justify-between text-lg font-bold"><span>RAZEM:</span><span className="neon-text">{order.total_price} PLN</span></div>
      </div>
      {order.status === 'draft' && <Button variant="neon" size="lg" className="w-full" onClick={onSubmit} isLoading={isLoading} disabled={order.items.length === 0}>Zloz zamowienie</Button>}
    </div>
  );
}
