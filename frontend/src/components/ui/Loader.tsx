export default function Loader({ text = 'Ladowanie...' }: { text?: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <div className="w-12 h-12 border-2 border-[var(--color-dark-border)] border-t-[var(--color-neon-green)] rounded-full animate-spin" />
      <p className="mt-4 text-sm text-[var(--color-text-secondary)]">{text}</p>
    </div>
  );
}
