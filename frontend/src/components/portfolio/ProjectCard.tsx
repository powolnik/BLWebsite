import { Link } from 'react-router-dom';
import { Calendar } from 'lucide-react';
import type { ProjectListItem } from '../../types';
import Card from '../ui/Card';

const catLabels: Record<string, string> = { main_stage: 'Main Stage', side_stage: 'Side Stage', art_installation: 'Instalacja', lighting: 'Oswietlenie', full_production: 'Produkcja' };

export default function ProjectCard({ project }: { project: ProjectListItem }) {
  return (
    <Link to={`/portfolio/${project.slug}`}>
      <Card className="group">
        <div className="aspect-video bg-[var(--color-dark-bg)] overflow-hidden relative">
          {project.cover_image ? <img src={project.cover_image} alt={project.title} className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" /> : <div className="w-full h-full flex items-center justify-center text-[var(--color-text-secondary)]">Brak zdjecia</div>}
          <span className="absolute top-3 left-3 px-2 py-1 text-xs font-medium bg-[var(--color-neon-green)] text-black rounded">{catLabels[project.category] || project.category}</span>
        </div>
        <div className="p-4">
          <h3 className="text-lg font-semibold mb-1 group-hover:text-[var(--color-neon-green)] transition-colors">{project.title}</h3>
          {project.festival_name && <p className="text-sm text-[var(--color-neon-cyan)] mb-2">{project.festival_name}</p>}
          <p className="text-sm text-[var(--color-text-secondary)] line-clamp-2 mb-3">{project.short_description}</p>
          <span className="flex items-center gap-1 text-xs text-[var(--color-text-secondary)]"><Calendar className="w-3 h-3" /> {project.date}</span>
        </div>
      </Card>
    </Link>
  );
}
