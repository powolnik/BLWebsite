import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, X, ShoppingCart, User, Zap } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import { useCartStore } from '../../store/cartStore';

const links = [
  { path: '/', label: 'Home' }, { path: '/about', label: 'O nas' },
  { path: '/portfolio', label: 'Portfolio' }, { path: '/configurator', label: 'Konfigurator' },
  { path: '/shop', label: 'Sklep' }, { path: '/contact', label: 'Kontakt' },
];

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const loc = useLocation();
  const { isAuthenticated, logout } = useAuth();
  const cart = useCartStore(s => s.cart);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 glass">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
        <Link to="/" className="flex items-center gap-2">
          <Zap className="w-6 h-6 text-[var(--color-neon-green)]" />
          <span className="text-xl font-bold gradient-text">SYNAPSE</span>
        </Link>
        <div className="hidden md:flex items-center gap-6">
          {links.map(l => (
            <Link key={l.path} to={l.path} className={`text-sm font-medium transition-colors hover:text-[var(--color-neon-green)] ${loc.pathname === l.path ? 'neon-text' : 'text-[var(--color-text-secondary)]'}`}>{l.label}</Link>
          ))}
        </div>
        <div className="hidden md:flex items-center gap-4">
          <Link to="/cart" className="relative p-2 hover:text-[var(--color-neon-green)]">
            <ShoppingCart className="w-5 h-5" />
            {cart && cart.item_count > 0 && <span className="absolute -top-1 -right-1 bg-[var(--color-neon-green)] text-black text-xs w-5 h-5 rounded-full flex items-center justify-center font-bold">{cart.item_count}</span>}
          </Link>
          {isAuthenticated ? (
            <button onClick={logout} className="text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-neon-pink)]">Wyloguj</button>
          ) : (
            <Link to="/login" className="btn-neon text-sm py-2 px-4">Zaloguj</Link>
          )}
        </div>
        <button onClick={() => setOpen(!open)} className="md:hidden p-2">{open ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}</button>
      </div>
      <AnimatePresence>
        {open && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }} className="md:hidden glass border-t border-[var(--color-dark-border)]">
            <div className="px-4 py-3 space-y-2">
              {links.map(l => <Link key={l.path} to={l.path} onClick={() => setOpen(false)} className={`block py-2 text-sm ${loc.pathname === l.path ? 'neon-text' : 'text-[var(--color-text-secondary)]'}`}>{l.label}</Link>)}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}
