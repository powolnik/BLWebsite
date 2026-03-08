import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { ArrowLeft, Calendar, Play } from 'lucide-react';
import { portfolioService } from '../services/portfolio';
import Loader from '../components/ui/Loader';

export default function PortfolioDetail() {
  const { slug } = useParams<{ slug: string }>();
  const { data: p, isLoading } = useQuery({ queryKey: ['project', slug], queryFn: () => portfolioService.getProject(slug!), enabled: !!slug });
  if (isLoading) return <Loader />;
  if (!p) return <div className="py-24 text-center">Nie znaleziono</div>;
  return (
    <div className="grid-bg py-24 px-4">
      <div className="max-w-5xl mx-auto">
        <Link to="/portfolio" className="inline-flex items-center gap-2 text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-neon-green)] mb-8"><ArrowLeft className="w-4 h-4" /> Portfolio</Link>
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="text-4xl font-bold mb-4">{p.title}</h1>
          <div className="flex flex-wrap gap-4 text-sm text-[var(--color-text-secondary)] mb-8">
            {p.festival && <span className="neon-text">{p.festival.name}</span>}
            <span className="flex items-center gap-1"><Calendar className="w-4 h-4" /> {p.date}</span>
          </div>
        </motion.div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-12">
          {p.images.map(img => <img key={img.id} src={img.image} alt={img.caption || p.title} className={`w-full rounded-xl ${img.is_cover ? 'md:col-span-2' : ''}`} />)}
        </div>
        <div className="text-[var(--color-text-secondary)] whitespace-pre-line mb-12">{p.description}</div>
        {p.video_url && <a href={p.video_url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 btn-neon mb-12"><Play className="w-5 h-5" /> Wideo</a>}
        {p.technologies && <div className="p-6 rounded-xl bg-[var(--color-dark-card)] border border-[var(--color-dark-border)] mb-12"><h3 className="font-semibold mb-2">Sprzet i technologie</h3><p className="text-sm text-[var(--color-text-secondary)]">{p.technologies}</p></div>}
      </div>
    </div>
  );
}
