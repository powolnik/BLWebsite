import { useState } from 'react';
import { useConfiguratorStore } from '../../store/configuratorStore';
import { configuratorService } from '../../services/configurator';
import { useAuth } from '../../hooks/useAuth';
import ModuleIcon from './ModuleIcon';
import Button from '../ui/Button';
import { Trash2, Minus, Plus, Send, Zap, Weight, DollarSign } from 'lucide-react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';

export default function SceneSummary() {
  const {
    sceneItems, selectedTemplate, templates,
    removeModule, updateQuantity, clearScene, selectTemplate,
    totalPrice, totalPower, totalWeight, itemCount,
  } = useConfiguratorStore();
  const { isAuthenticated } = useAuth();

  const [showForm, setShowForm] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    event_name: '', event_date: '', event_location: '', notes: '',
  });

  const price = totalPrice();
  const power = totalPower();
  const weight = totalWeight();
  const count = itemCount();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await configuratorService.submitOrder({
        template: selectedTemplate?.id,
        ...formData,
        items: sceneItems.map(i => ({
          component_id: i.component.id,
          quantity: i.quantity,
        })),
        scene_data: {
          items: sceneItems.map(i => ({
            component_id: i.component.id,
            component_name: i.component.name,
            quantity: i.quantity,
          })),
        },
      });
      toast.success('Zamówienie złożone! Skontaktujemy się wkrótce.');
      setShowForm(false);
      clearScene();
    } catch {
      toast.error('Błąd składania zamówienia');
    }
    setSubmitting(false);
  };

  return (
    <div className="h-full flex flex-col bg-[var(--color-dark-card)] rounded-xl border border-[var(--color-dark-border)] overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 border-b border-[var(--color-dark-border)] shrink-0">
        <h3 className="font-semibold text-sm">Twoja scena</h3>
      </div>

      {/* Template selector */}
      <div className="px-4 py-2 border-b border-[var(--color-dark-border)] shrink-0">
        <label className="text-xs text-[var(--color-text-secondary)] mb-1 block">Szablon sceny</label>
        <select
          value={selectedTemplate?.id || ''}
          onChange={(e) => {
            const t = templates.find(t => t.id === Number(e.target.value));
            selectTemplate(t || null);
          }}
          className="w-full bg-[var(--color-dark-bg)] border border-[var(--color-dark-border)] rounded-lg px-3 py-1.5 text-sm text-white"
        >
          <option value="">— Bez szablonu —</option>
          {templates.map(t => (
            <option key={t.id} value={t.id}>{t.name} (+{parseFloat(t.base_price).toLocaleString()} PLN)</option>
          ))}
        </select>
      </div>

      {/* Items list */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {sceneItems.length === 0 ? (
          <div className="text-center py-8 text-[var(--color-text-secondary)]">
            <p className="text-sm">Brak modułów</p>
            <p className="text-xs mt-1 opacity-50">Dodaj moduły z panelu po lewej</p>
          </div>
        ) : (
          sceneItems.map(item => (
            <div key={item.id} className="flex items-center gap-2 p-2 rounded-lg bg-[var(--color-dark-bg)] border border-[var(--color-dark-border)]">
              <ModuleIcon iconName={item.component.icon_name} color={item.component.color} size={20} />
              <div className="flex-1 min-w-0">
                <span className="text-xs font-medium text-white truncate block">{item.component.name}</span>
                <span className="text-xs" style={{ color: item.component.color }}>
                  {(parseFloat(item.component.price) * item.quantity).toLocaleString('pl-PL')} PLN
                </span>
              </div>
              {/* Quantity controls */}
              <div className="flex items-center gap-1">
                <button onClick={() => updateQuantity(item.id, item.quantity - 1)}
                        className="w-5 h-5 rounded flex items-center justify-center bg-white/5 hover:bg-white/10 text-white/60">
                  <Minus className="w-3 h-3" />
                </button>
                <span className="text-xs font-mono w-5 text-center">{item.quantity}</span>
                <button onClick={() => updateQuantity(item.id, item.quantity + 1)}
                        className="w-5 h-5 rounded flex items-center justify-center bg-white/5 hover:bg-white/10 text-white/60">
                  <Plus className="w-3 h-3" />
                </button>
              </div>
              <button onClick={() => removeModule(item.id)}
                      className="p-1 text-white/30 hover:text-red-400 transition-colors">
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            </div>
          ))
        )}
      </div>

      {/* Stats + Total */}
      <div className="border-t border-[var(--color-dark-border)] p-3 space-y-2 shrink-0">
        {count > 0 && (
          <div className="grid grid-cols-3 gap-2 text-center">
            <div className="bg-[var(--color-dark-bg)] rounded-lg p-2">
              <Zap className="w-3.5 h-3.5 text-yellow-400 mx-auto mb-0.5" />
              <div className="text-xs font-mono text-yellow-400">{power.toLocaleString()}W</div>
            </div>
            <div className="bg-[var(--color-dark-bg)] rounded-lg p-2">
              <Weight className="w-3.5 h-3.5 text-blue-400 mx-auto mb-0.5" />
              <div className="text-xs font-mono text-blue-400">{weight.toFixed(0)}kg</div>
            </div>
            <div className="bg-[var(--color-dark-bg)] rounded-lg p-2">
              <DollarSign className="w-3.5 h-3.5 text-[var(--color-neon-green)] mx-auto mb-0.5" />
              <div className="text-xs font-mono text-[var(--color-neon-green)]">{count} szt.</div>
            </div>
          </div>
        )}

        {/* Price */}
        <div className="flex justify-between items-center text-sm">
          <span className="text-[var(--color-text-secondary)]">Razem:</span>
          <span className="text-lg font-bold neon-text">{price.toLocaleString('pl-PL')} PLN</span>
        </div>

        {/* Actions */}
        <div className="space-y-2">
          {!showForm ? (
            <>
              {isAuthenticated ? (
                <Button
                  variant="neon"
                  size="sm"
                  className="w-full"
                  disabled={count === 0}
                  onClick={() => setShowForm(true)}
                >
                  <Send className="w-4 h-4 mr-2" />
                  Złóż zamówienie
                </Button>
              ) : (
                <Link to="/login" className="block">
                  <Button variant="neon" size="sm" className="w-full" disabled={count === 0}>
                    Zaloguj się aby zamówić
                  </Button>
                </Link>
              )}
              {count > 0 && (
                <Button variant="outline" size="sm" className="w-full" onClick={clearScene}>
                  Wyczyść scenę
                </Button>
              )}
            </>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-2">
              <input
                type="text" required placeholder="Nazwa wydarzenia"
                value={formData.event_name}
                onChange={e => setFormData({...formData, event_name: e.target.value})}
                className="w-full bg-[var(--color-dark-bg)] border border-[var(--color-dark-border)] rounded-lg px-3 py-1.5 text-sm text-white placeholder:text-white/30"
              />
              <input
                type="date" required
                value={formData.event_date}
                onChange={e => setFormData({...formData, event_date: e.target.value})}
                className="w-full bg-[var(--color-dark-bg)] border border-[var(--color-dark-border)] rounded-lg px-3 py-1.5 text-sm text-white"
              />
              <input
                type="text" required placeholder="Lokalizacja"
                value={formData.event_location}
                onChange={e => setFormData({...formData, event_location: e.target.value})}
                className="w-full bg-[var(--color-dark-bg)] border border-[var(--color-dark-border)] rounded-lg px-3 py-1.5 text-sm text-white placeholder:text-white/30"
              />
              <textarea
                placeholder="Dodatkowe uwagi (opcjonalne)"
                value={formData.notes}
                onChange={e => setFormData({...formData, notes: e.target.value})}
                className="w-full bg-[var(--color-dark-bg)] border border-[var(--color-dark-border)] rounded-lg px-3 py-1.5 text-sm text-white placeholder:text-white/30 h-16 resize-none"
              />
              <Button type="submit" variant="neon" size="sm" className="w-full" isLoading={submitting}>
                Wyślij zamówienie
              </Button>
              <Button type="button" variant="outline" size="sm" className="w-full" onClick={() => setShowForm(false)}>
                Anuluj
              </Button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
