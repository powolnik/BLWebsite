import type { SceneTemplate } from '../../types';

export default function StageCanvas({ template }: { template: SceneTemplate | null }) {
  return (
    <div className="aspect-video bg-[var(--color-dark-bg)] rounded-xl neon-border flex items-center justify-center">
      {template ? (
        <div className="text-center">
          <img src={template.preview_image} alt={template.name} className="max-h-64 mx-auto rounded-lg mb-4" />
          <h3 className="text-lg font-semibold">{template.name}</h3>
          <p className="text-sm text-[var(--color-text-secondary)]">{template.width}m x {template.depth}m x {template.height}m</p>
        </div>
      ) : <p className="text-[var(--color-text-secondary)]">Wybierz szablon sceny</p>}
    </div>
  );
}
