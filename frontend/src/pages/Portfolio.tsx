import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { portfolioService } from '../services/portfolio';
import ProjectCard from '../components/portfolio/ProjectCard';
import Loader from '../components/ui/Loader';
import Button from '../components/ui/Button';

const cats = [{ v: '', l: 'Wszystkie' }, { v: 'main_stage', l: 'Main Stage' }, { v: 'side_stage', l: 'Side Stage' }, { v: 'art_installation', l: 'Instalacje' }, { v: 'lighting', l: 'Oswietlenie' }, { v: 'full_production', l: 'Produkcja' }];

export default function Portfolio() {
  const [cat, setCat] = useState('');
  const [page, setPage] = useState(1);
  const { data, isLoading } = useQuery({ queryKey: ['projects', cat, page], queryFn: () => portfolioService.getProjects({ category: cat || undefined, page }) });

  return (
    <div className="grid-bg py-24 px-4">
      <div className="max-w-7xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-4"><span className="gradient-text">Portfolio</span></h1>
        </motion.div>
        <div className="flex flex-wrap justify-center gap-2 mb-12">
          {cats.map(c => <button key={c.v} onClick={() => { setCat(c.v); setPage(1); }} className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${cat === c.v ? 'bg-[var(--color-neon-green)] text-black' : 'bg-[var(--color-dark-card)] text-[var(--color-text-secondary)] border border-[var(--color-dark-border)]'}`}>{c.l}</button>)}
        </div>
        {isLoading ? <Loader /> : (
          <><div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">{data?.results.map(p => <ProjectCard key={p.id} project={p} />)}</div>
          {data && (data.next || data.previous) && <div className="flex justify-center gap-4 mt-12"><Button variant="outline" disabled={!data.previous} onClick={() => setPage(p => p - 1)}>Poprzednia</Button><Button variant="outline" disabled={!data.next} onClick={() => setPage(p => p + 1)}>Nastepna</Button></div>}</>
        )}
      </div>
    </div>
  );
}
