import { type ReactNode } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';

export default function Modal({ isOpen, onClose, title, children }: { isOpen: boolean; onClose: () => void; title?: string; children: ReactNode }) {
  return (
    <AnimatePresence>
      {isOpen && (<>
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={onClose} className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50" />
        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.95 }} className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-lg max-h-[85vh] overflow-auto rounded-xl bg-[var(--color-dark-card)] border border-[var(--color-dark-border)] p-6">
          <div className="flex items-center justify-between mb-4">
            {title && <h2 className="text-lg font-semibold">{title}</h2>}
            <button onClick={onClose} className="p-1 hover:text-[var(--color-neon-pink)]"><X className="w-5 h-5" /></button>
          </div>
          {children}
        </motion.div>
      </>)}
    </AnimatePresence>
  );
}
