import { motion } from 'framer-motion';
import { Mail, MapPin, Phone, Instagram, Send } from 'lucide-react';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';

export default function Contact() {
  return (
    <div className="grid-bg py-24 px-4">
      <div className="max-w-5xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold mb-4"><span className="gradient-text">Kontakt</span></h1>
        </motion.div>
        <div className="grid md:grid-cols-2 gap-12">
          <div>
            <h2 className="text-2xl font-bold mb-6">Napisz do nas</h2>
            <form className="space-y-4" onSubmit={e => e.preventDefault()}>
              <div className="grid grid-cols-2 gap-4"><Input label="Imie" required /><Input label="Nazwisko" required /></div>
              <Input label="Email" type="email" required />
              <Input label="Temat" />
              <div className="space-y-1"><label className="block text-sm font-medium text-[var(--color-text-secondary)]">Wiadomosc</label><textarea rows={5} className="w-full px-4 py-2.5 bg-[var(--color-dark-bg)] border border-[var(--color-dark-border)] rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[var(--color-neon-green)] focus:ring-opacity-50" required /></div>
              <Button type="submit" size="lg" className="w-full"><Send className="w-4 h-4 mr-2" /> Wyslij</Button>
            </form>
          </div>
          <div>
            <h2 className="text-2xl font-bold mb-6">Dane kontaktowe</h2>
            <div className="space-y-4">
              {[{ icon: Mail, l: 'Email', v: 'hello@blacklight-collective.pl' }, { icon: Phone, l: 'Telefon', v: '+48 123 456 789' }, { icon: MapPin, l: 'Lokalizacja', v: 'Wroclaw, Polska' }, { icon: Instagram, l: 'Instagram', v: '@blacklight.collective' }].map(({ icon: Icon, l, v }) => (
                <div key={l} className="flex items-start gap-4 p-4 rounded-xl bg-[var(--color-dark-card)] border border-[var(--color-dark-border)]">
                  <div className="w-10 h-10 rounded-lg bg-[var(--color-dark-bg)] flex items-center justify-center"><Icon className="w-5 h-5 text-[var(--color-neon-green)]" /></div>
                  <div><div className="text-sm text-[var(--color-text-secondary)]">{l}</div><div className="font-medium">{v}</div></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
