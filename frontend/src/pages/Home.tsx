import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { ArrowRight, Zap, Lightbulb, Music, Palette } from 'lucide-react';
import Button from '../components/ui/Button';

const features = [
  { icon: Lightbulb, title: 'Oswietlenie', desc: 'Profesjonalne systemy laserowe, LED i ruchome glowice' },
  { icon: Palette, title: 'Dekoracje', desc: 'Unikalne instalacje artystyczne i scenografia' },
  { icon: Music, title: 'Sceny', desc: 'Pelna produkcja scen festiwalowych od A do Z' },
  { icon: Zap, title: 'Efekty', desc: 'Pirotechnika sceniczna, CO2, konfetti, haze' },
];

export default function Home() {
  return (
    <div className="grid-bg">
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[var(--color-dark-bg)] to-[var(--color-dark-bg)]" />
        <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }} className="relative text-center px-4 max-w-4xl">
          <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.3, type: 'spring' }} className="w-20 h-20 mx-auto mb-8 rounded-2xl bg-[var(--color-dark-card)] neon-border flex items-center justify-center">
            <Zap className="w-10 h-10 text-[var(--color-neon-green)]" />
          </motion.div>
          <h1 className="text-5xl md:text-7xl font-bold mb-6"><span className="gradient-text">BLACK LIGHT</span><br /><span className="text-2xl md:text-3xl font-light text-[var(--color-text-secondary)]">Collective</span></h1>
          <p className="text-lg md:text-xl text-[var(--color-text-secondary)] mb-8 max-w-2xl mx-auto">Tworzymy niezapomniane sceny na festiwalach muzyki elektronicznej. Oswietlenie, dekoracje, efekty specjalne.</p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/configurator"><Button size="lg">Skonfiguruj scene <ArrowRight className="ml-2 w-5 h-5" /></Button></Link>
            <Link to="/portfolio"><Button variant="outline" size="lg">Zobacz realizacje</Button></Link>
          </div>
        </motion.div>
      </section>
      <section className="py-24 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-16">Co <span className="gradient-text">robimy</span></h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map(({ icon: Icon, title, desc }, i) => (
              <motion.div key={title} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.1 }}
                className="text-center p-6 rounded-xl bg-[var(--color-dark-card)] border border-[var(--color-dark-border)] hover:neon-border transition-all">
                <div className="w-14 h-14 mx-auto mb-4 rounded-xl bg-[var(--color-dark-bg)] flex items-center justify-center"><Icon className="w-7 h-7 text-[var(--color-neon-green)]" /></div>
                <h3 className="font-semibold text-lg mb-2">{title}</h3>
                <p className="text-sm text-[var(--color-text-secondary)]">{desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
      <section className="py-24 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="p-12 rounded-2xl neon-border bg-[var(--color-dark-card)]">
            <h2 className="text-3xl font-bold mb-4">Masz wizje? My ja zrealizujemy.</h2>
            <p className="text-[var(--color-text-secondary)] mb-8">Uzyj naszego konfiguratora scen lub skontaktuj sie bezposrednio.</p>
            <Link to="/contact"><Button size="lg">Skontaktuj sie</Button></Link>
          </div>
        </div>
      </section>
    </div>
  );
}
