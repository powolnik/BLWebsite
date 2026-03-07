import { Link } from 'react-router-dom';
import { ShoppingCart } from 'lucide-react';
import type { ProductListItem } from '../../types';
import Card from '../ui/Card';
import Button from '../ui/Button';

export default function ProductCard({ product, onAddToCart }: { product: ProductListItem; onAddToCart: (id: number) => void }) {
  return (
    <Card className="group flex flex-col">
      <Link to={`/shop/${product.slug}`}>
        <div className="aspect-square bg-[var(--color-dark-bg)] overflow-hidden relative">
          {product.primary_image ? <img src={product.primary_image} alt={product.name} className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" /> : <div className="w-full h-full flex items-center justify-center text-[var(--color-text-secondary)]">Brak</div>}
          {product.compare_price && <span className="absolute top-3 left-3 px-2 py-1 text-xs font-bold bg-[var(--color-neon-pink)] text-white rounded">SALE</span>}
        </div>
      </Link>
      <div className="p-4 flex flex-col flex-1">
        <p className="text-xs text-[var(--color-neon-cyan)] mb-1">{product.category_name}</p>
        <Link to={`/shop/${product.slug}`}><h3 className="font-semibold mb-1 group-hover:text-[var(--color-neon-green)] line-clamp-2">{product.name}</h3></Link>
        <p className="text-xs text-[var(--color-text-secondary)] line-clamp-2 mb-3 flex-1">{product.short_description}</p>
        <div className="flex items-center justify-between">
          <div><span className="text-lg font-bold neon-text">{product.price} PLN</span>{product.compare_price && <span className="text-xs text-[var(--color-text-secondary)] line-through ml-2">{product.compare_price} PLN</span>}</div>
          <Button size="sm" onClick={(e) => { e.preventDefault(); onAddToCart(product.id); }} disabled={!product.is_in_stock}><ShoppingCart className="w-4 h-4" /></Button>
        </div>
      </div>
    </Card>
  );
}
