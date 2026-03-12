/**
 * BLACK LIGHT Collective — Footer
 * Site-wide footer with three columns:
 *   - Brand description
 *   - Navigation links
 *   - Contact information (email, location, Instagram)
 */

import { Link } from 'react-router-dom';
import { Zap, Instagram, Mail, MapPin } from 'lucide-react';

/** Footer — rendered at the bottom of every page via the Layout component */
export default function Footer() {
  return (
    <footer className="border-t border-[var(--color-dark-border)] bg-[var(--color-dark-surface)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Brand column */}
          <div>
            <div className="flex items-center gap-2 mb-4"><Zap className="w-6 h-6 text-[var(--color-neon-green)]" /><span className="text-xl font-bold gradient-text">BLACK LIGHT</span></div>
            <p className="text-sm text-[var(--color-text-secondary)]">Kolektyw tworzacy niezapomniane sceny na festiwalach muzyki elektronicznej.</p>
          </div>

          {/* Navigation column */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider mb-4">Nawigacja</h3>
            <ul className="space-y-2">
              {[['/', 'Home'], ['/portfolio', 'Portfolio'], ['/scene-builder', 'Scene Builder'], ['/shop', 'Sklep'], ['/contact', 'Kontakt']].map(([p, l]) => (
                <li key={p}><Link to={p} className="text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-neon-green)]">{l}</Link></li>
              ))}
            </ul>
          </div>

          {/* Contact column */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider mb-4">Kontakt</h3>
            <ul className="space-y-2 text-sm text-[var(--color-text-secondary)]">
              <li className="flex items-center gap-2"><Mail className="w-4 h-4" /> hello@blacklight-collective.pl</li>
              <li className="flex items-center gap-2"><MapPin className="w-4 h-4" /> Wroclaw, Polska</li>
              <li className="flex items-center gap-2"><Instagram className="w-4 h-4" /> @blacklight.collective</li>
            </ul>
          </div>
        </div>

        {/* Copyright */}
        <div className="mt-8 pt-8 border-t border-[var(--color-dark-border)] text-center text-sm text-[var(--color-text-secondary)]">&copy; {new Date().getFullYear()} BLACK LIGHT Collective</div>
      </div>
    </footer>
  );
}
