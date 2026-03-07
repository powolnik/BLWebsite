import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { ArrowLeft, ShoppingCart } from 'lucide-react';
import { shopService } from '../services/shop';
import { useCart } from '../hooks/useCart';
import Button from '../components/ui/Button';
import Loader from '../components/ui/Loader';

export default function ProductDetail() {
  const { slug } = useParams<{ slug: string }>();
  const { addToCart } = useCart();
  const { data: p, isLoading } = useQuery({ queryKey: ['product', slug], queryFn: () => shopService.getProduct(slug!), enabled: !!slug });
  if (isLoading) return <Loader />;
  if (!p) return <div className="py-24 text-center">Nie znaleziono</div>;
  return (
    <div className="grid-bg py-24 px-4">
      <div className="max-w-5xl mx-auto">
        <Link to="/shop" className="inline-flex items-center gap-2 text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-neon-green)] mb-8"><ArrowLeft className="w-4 h-4" /> Sklep</Link>
        <div className="grid md:grid-cols-2 gap-12">
          <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} className="space-y-4">{p.images.map(img => <img key={img.id} src={img.image} alt={img.alt_text || p.name} className="w-full rounded-xl" />)}</motion.div>
          <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}>
            <p className="text-sm text-[var(--color-neon-cyan)] mb-2">{p.category.name}</p>
            <h1 className="text-3xl font-bold mb-4">{p.name}</h1>
            <div className="flex items-baseline gap-3 mb-6"><span className="text-3xl font-bold neon-text">{p.price} PLN</span>{p.compare_price && <span className="text-lg text-[var(--color-text-secondary)] line-through">{p.compare_price} PLN</span>}</div>
            <p className="text-[var(--color-text-secondary)] mb-8">{p.description}</p>
            <Button size="lg" className="w-full" disabled={!p.is_in_stock} onClick={() => addToCart(p.id)}><ShoppingCart className="w-5 h-5 mr-2" /> Dodaj do koszyka</Button>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
