import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import Button from '../components/ui/Button';

export default function NotFound() {
  return (
    <div className="grid-bg min-h-screen flex items-center justify-center px-4">
      <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="text-center">
        <h1 className="text-8xl font-bold neon-text mb-4">404</h1>
        <p className="text-xl text-[var(--color-text-secondary)] mb-8">Strona nie znaleziona</p>
        <Link to="/"><Button size="lg">Strona glowna</Button></Link>
      </motion.div>
    </div>
  );
}
