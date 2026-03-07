import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { useConfiguratorStore } from '../store/configuratorStore';
import StageCanvas from '../components/configurator/StageCanvas';
import ComponentPicker from '../components/configurator/ComponentPicker';
import OrderSummary from '../components/configurator/OrderSummary';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import { useAuth } from '../hooks/useAuth';
import { Link } from 'react-router-dom';

export default function Configurator() {
  const { isAuthenticated } = useAuth();
  const { templates, categories, currentOrder, step, isLoading, fetchTemplates, fetchCategories, createOrder, addItem, removeItem, submitOrder, setStep } = useConfiguratorStore();
  useEffect(() => { fetchTemplates(); fetchCategories(); }, [fetchTemplates, fetchCategories]);

  if (!isAuthenticated) return <div className="grid-bg py-24 px-4 text-center"><h1 className="text-3xl font-bold mb-4">Konfigurator scen</h1><p className="text-[var(--color-text-secondary)] mb-8">Zaloguj sie aby rozpoczac</p><Link to="/login"><Button>Zaloguj</Button></Link></div>;

  return (
    <div className="grid-bg py-24 px-4">
      <div className="max-w-7xl mx-auto">
        <motion.h1 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-4xl font-bold text-center mb-4"><span className="gradient-text">Konfigurator scen</span></motion.h1>
        <div className="flex justify-center gap-4 mb-12">
          {['Szablon', 'Komponenty', 'Podsumowanie'].map((l, i) => (
            <div key={l} className={`flex items-center gap-2 text-sm ${i <= step ? 'text-[var(--color-neon-green)]' : 'text-[var(--color-text-secondary)]'}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${i <= step ? 'bg-[var(--color-neon-green)] text-black' : 'bg-[var(--color-dark-card)]'}`}>{i + 1}</div>
              <span className="hidden sm:inline">{l}</span>
            </div>
          ))}
        </div>
        {step === 0 && (
          <div className="max-w-2xl mx-auto">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
              {templates.map(t => <div key={t.id} className="p-4 rounded-xl bg-[var(--color-dark-card)] border border-[var(--color-dark-border)] cursor-pointer hover:neon-border"><img src={t.preview_image} alt={t.name} className="w-full h-32 object-cover rounded-lg mb-3" /><h3 className="font-medium">{t.name}</h3><p className="text-sm text-[var(--color-text-secondary)]">{t.base_price} PLN</p></div>)}
            </div>
            <form onSubmit={(e) => { e.preventDefault(); const f = new FormData(e.currentTarget); createOrder({ event_name: f.get('event_name') as string, event_date: f.get('event_date') as string, event_location: f.get('event_location') as string }); }} className="space-y-4">
              <Input name="event_name" label="Nazwa wydarzenia" required />
              <Input name="event_date" label="Data" type="date" required />
              <Input name="event_location" label="Lokalizacja" required />
              <Button type="submit" size="lg" className="w-full" isLoading={isLoading}>Rozpocznij</Button>
            </form>
          </div>
        )}
        {step === 1 && currentOrder && (
          <div className="grid lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2"><StageCanvas template={currentOrder.template} /><div className="mt-8"><ComponentPicker categories={categories} onAddItem={addItem} /></div></div>
            <div className="lg:col-span-1 sticky top-24"><OrderSummary order={currentOrder} onRemoveItem={removeItem} onSubmit={() => setStep(2)} isLoading={false} /><Button variant="outline" className="w-full mt-4" onClick={() => setStep(2)}>Dalej</Button></div>
          </div>
        )}
        {step === 2 && currentOrder && <div className="max-w-2xl mx-auto"><OrderSummary order={currentOrder} onRemoveItem={removeItem} onSubmit={submitOrder} isLoading={isLoading} /><Button variant="outline" className="w-full mt-4" onClick={() => setStep(1)}>Wroc</Button></div>}
      </div>
    </div>
  );
}
