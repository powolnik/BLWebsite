import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { portfolioService } from '../services/portfolio';
import TeamCard from '../components/portfolio/TeamCard';
import Loader from '../components/ui/Loader';

export default function About() {
  const { data: team, isLoading } = useQuery({ queryKey: ['team'], queryFn: portfolioService.getTeam });
  return (
    <div className="grid-bg py-24 px-4">
      <div className="max-w-6xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">O <span className="gradient-text">BLACK LIGHT</span></h1>
          <p className="text-lg text-[var(--color-text-secondary)] max-w-2xl mx-auto">Jestesmy kolektywem kreatywnych umyslow, polaczonych pasja do muzyki elektronicznej.</p>
        </motion.div>
        <div className="grid md:grid-cols-2 gap-12 mb-24">
          <div><h2 className="text-2xl font-bold mb-4">Nasza historia</h2><p className="text-[var(--color-text-secondary)]">BLACK LIGHT Collective powstalo z potrzeby tworzenia przestrzeni laczacych technologie z sztuka. Od 2020 roku projektujemy sceny i instalacje swietlne na festiwalach w calej Polsce.</p></div>
          <div className="grid grid-cols-2 gap-4">
            {[{ n: '50+', l: 'Zrealizowanych scen' }, { n: '25+', l: 'Festiwali' }, { n: '12', l: 'Czlonkow' }, { n: '500K+', l: 'Uczestnikow' }].map(s => (
              <div key={s.l} className="p-6 rounded-xl bg-[var(--color-dark-card)] border border-[var(--color-dark-border)] text-center">
                <div className="text-3xl font-bold neon-text mb-1">{s.n}</div><div className="text-xs text-[var(--color-text-secondary)]">{s.l}</div>
              </div>
            ))}
          </div>
        </div>
        <h2 className="text-3xl font-bold text-center mb-12">Nasz <span className="gradient-text">zespol</span></h2>
        {isLoading ? <Loader /> : <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">{team?.map(m => <TeamCard key={m.id} member={m} />)}</div>}
      </div>
    </div>
  );
}
