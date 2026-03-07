import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { shopService } from '../services/shop';
import ProductCard from '../components/shop/ProductCard';
import { useCart } from '../hooks/useCart';
import Loader from '../components/ui/Loader';
import Input from '../components/ui/Input';

export default function Shop() {
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const { addToCart } = useCart();
  const { data, isLoading } = useQuery({ queryKey: ['products', search, page], queryFn: () => shopService.getProducts({ search: search || undefined, page }) });

  return (
    <div className="grid-bg py-24 px-4">
      <div className="max-w-7xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-4"><span className="gradient-text">Sklep</span></h1>
        </motion.div>
        <div className="max-w-md mx-auto mb-12"><Input placeholder="Szukaj produktow..." value={search} onChange={e => { setSearch(e.target.value); setPage(1); }} /></div>
        {isLoading ? <Loader /> : <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">{data?.results.map(p => <ProductCard key={p.id} product={p} onAddToCart={addToCart} />)}</div>}
      </div>
    </div>
  );
}
