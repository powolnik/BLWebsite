import { type ReactNode } from 'react';
import { motion } from 'framer-motion';
import { clsx } from 'clsx';

export default function Card({ children, className, hover = true }: { children: ReactNode; className?: string; hover?: boolean }) {
  return (
    <motion.div whileHover={hover ? { y: -4, scale: 1.01 } : undefined} transition={{ duration: 0.2 }}
      className={clsx('rounded-xl bg-[var(--color-dark-card)] border border-[var(--color-dark-border)] overflow-hidden', className)}>
      {children}
    </motion.div>
  );
}
